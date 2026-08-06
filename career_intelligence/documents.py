"""Dependency-free deterministic DOCX and PDF generation."""

from __future__ import annotations

import io
import textwrap
import zipfile
from xml.sax.saxutils import escape

_FIXED_ZIP_TIME = (2026, 8, 6, 0, 0, 0)
_DOCX_REQUIRED = {
    "[Content_Types].xml",
    "_rels/.rels",
    "docProps/app.xml",
    "docProps/core.xml",
    "word/_rels/document.xml.rels",
    "word/document.xml",
    "word/styles.xml",
}


def _zip_entry(name: str, payload: bytes) -> tuple[zipfile.ZipInfo, bytes]:
    info = zipfile.ZipInfo(name, _FIXED_ZIP_TIME)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o100644 << 16
    return info, payload


def _paragraph_xml(text: str, *, style: str | None = None) -> str:
    properties = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>' if style else ""
    if not text:
        return f"<w:p>{properties}</w:p>"
    return (
        f"<w:p>{properties}<w:r><w:t xml:space=\"preserve\">"
        f"{escape(text)}</w:t></w:r></w:p>"
    )


def render_docx(text: str, *, title: str, creator: str) -> bytes:
    """Create a compact valid DOCX with stable bytes for identical inputs."""

    paragraphs: list[str] = []
    section_names = {
        "PROFESSIONAL SUMMARY",
        "VERIFIED PROOF",
        "EXPERIENCE",
        "CAPABILITIES",
        "EDUCATION",
        "EVIDENCE BOUNDARY",
    }
    for index, line in enumerate(text.splitlines()):
        style = "Title" if index == 0 else "Heading1" if line in section_names else None
        paragraphs.append(_paragraph_xml(line, style=style))

    document = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        f"<w:body>{''.join(paragraphs)}"
        '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
        '<w:pgMar w:top="720" w:right="720" w:bottom="720" w:left="720" '
        'w:header="360" w:footer="360" w:gutter="0"/></w:sectPr></w:body></w:document>'
    ).encode("utf-8")
    styles = b'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial"/><w:sz w:val="20"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Title">
    <w:name w:val="Title"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/>
    <w:rPr><w:b/><w:sz w:val="34"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/>
    <w:rPr><w:b/><w:sz w:val="24"/></w:rPr>
  </w:style>
</w:styles>'''
    content_types = b'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>'''
    root_rels = b'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>'''
    document_rels = b'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>'''
    core = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/" '
        'xmlns:dcterms="http://purl.org/dc/terms/" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
        f"<dc:title>{escape(title)}</dc:title><dc:creator>{escape(creator)}</dc:creator>"
        '<cp:lastModifiedBy>AKOS Career Intelligence</cp:lastModifiedBy>'
        '<dcterms:created xsi:type="dcterms:W3CDTF">2026-08-06T00:00:00Z</dcterms:created>'
        '<dcterms:modified xsi:type="dcterms:W3CDTF">2026-08-06T00:00:00Z</dcterms:modified>'
        "</cp:coreProperties>"
    ).encode("utf-8")
    app = b'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>AKOS Career Intelligence</Application><AppVersion>1.0</AppVersion>
</Properties>'''
    entries = {
        "[Content_Types].xml": content_types,
        "_rels/.rels": root_rels,
        "docProps/app.xml": app,
        "docProps/core.xml": core,
        "word/_rels/document.xml.rels": document_rels,
        "word/document.xml": document,
        "word/styles.xml": styles,
    }
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name in sorted(entries):
            info, payload = _zip_entry(name, entries[name])
            archive.writestr(info, payload)
    return output.getvalue()


def _ascii_pdf_text(value: str) -> str:
    replacements = {
        "–": "-",
        "—": "-",
        "·": "|",
        "’": "'",
        "“": '"',
        "”": '"',
        "…": "...",
    }
    for source, target in replacements.items():
        value = value.replace(source, target)
    return value.encode("latin-1", "replace").decode("latin-1")


def _pdf_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def render_pdf(text: str, *, title: str, author: str) -> bytes:
    """Create a deterministic multipage text PDF using only the standard library."""

    lines: list[str] = []
    for source_line in text.splitlines():
        normalized = _ascii_pdf_text(source_line)
        if not normalized:
            lines.append("")
            continue
        prefix = "- " if normalized.startswith("- ") else ""
        body = normalized[2:] if prefix else normalized
        wrapped = textwrap.wrap(
            body,
            width=92 if not prefix else 88,
            break_long_words=False,
            break_on_hyphens=False,
        ) or [""]
        lines.extend([prefix + wrapped[0], *[("  " if prefix else "") + item for item in wrapped[1:]]])

    lines_per_page = 49
    pages = [lines[index : index + lines_per_page] for index in range(0, len(lines), lines_per_page)] or [[]]
    font_object = 3
    objects: dict[int, bytes] = {}
    page_ids = [4 + index * 2 for index in range(len(pages))]
    objects[1] = b"<< /Type /Catalog /Pages 2 0 R >>"
    kids = " ".join(f"{page_id} 0 R" for page_id in page_ids)
    objects[2] = f"<< /Type /Pages /Kids [{kids}] /Count {len(page_ids)} >>".encode("ascii")
    objects[font_object] = b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"

    for index, page_lines in enumerate(pages):
        page_id = page_ids[index]
        content_id = page_id + 1
        commands = ["BT", "/F1 9.5 Tf", "12.5 TL", "54 738 Td"]
        commands.extend(f"({_pdf_escape(line)}) Tj T*" for line in page_lines)
        commands.append("ET")
        stream = "\n".join(commands).encode("latin-1")
        objects[page_id] = (
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
            f"/Resources << /Font << /F1 {font_object} 0 R >> >> /Contents {content_id} 0 R >>"
        ).encode("ascii")
        objects[content_id] = (
            f"<< /Length {len(stream)} >>\nstream\n".encode("ascii")
            + stream
            + b"\nendstream"
        )

    info_id = max(objects) + 1
    safe_title = _pdf_escape(_ascii_pdf_text(title))
    safe_author = _pdf_escape(_ascii_pdf_text(author))
    objects[info_id] = (
        f"<< /Title ({safe_title}) /Author ({safe_author}) "
        "/Creator (AKOS Career Intelligence) /Producer (AKOS deterministic PDF) >>"
    ).encode("latin-1")

    output = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = {0: 0}
    for object_id in sorted(objects):
        offsets[object_id] = len(output)
        output.extend(f"{object_id} 0 obj\n".encode("ascii"))
        output.extend(objects[object_id])
        output.extend(b"\nendobj\n")
    xref_offset = len(output)
    max_id = max(objects)
    output.extend(f"xref\n0 {max_id + 1}\n".encode("ascii"))
    output.extend(b"0000000000 65535 f \n")
    for object_id in range(1, max_id + 1):
        output.extend(f"{offsets[object_id]:010d} 00000 n \n".encode("ascii"))
    output.extend(
        (
            f"trailer\n<< /Size {max_id + 1} /Root 1 0 R /Info {info_id} 0 R >>\n"
            f"startxref\n{xref_offset}\n%%EOF\n"
        ).encode("ascii")
    )
    return bytes(output)


def verify_docx(payload: bytes) -> tuple[bool, str]:
    try:
        with zipfile.ZipFile(io.BytesIO(payload)) as archive:
            names = set(archive.namelist())
            missing = sorted(_DOCX_REQUIRED - names)
            if missing:
                return False, f"missing DOCX members: {', '.join(missing)}"
            if archive.testzip() is not None:
                return False, "DOCX CRC failure"
    except (OSError, zipfile.BadZipFile) as exc:
        return False, f"invalid DOCX: {exc}"
    return True, ""


def verify_pdf(payload: bytes) -> tuple[bool, str]:
    if not payload.startswith(b"%PDF-1.4"):
        return False, "invalid PDF header"
    if not payload.rstrip().endswith(b"%%EOF"):
        return False, "invalid PDF trailer"
    if b"/Type /Page" not in payload or b"xref\n" not in payload:
        return False, "PDF structure incomplete"
    return True, ""
