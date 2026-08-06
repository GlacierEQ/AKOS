# Career Intelligence Runtime

`akos-career` converts a versioned career-runtime projection of the verified Resume Master record into a complete, verified, network-independent career package. The original Resume Master source and its historical artifact identities remain unchanged.

```bash
akos-career validate
akos-career build --output artifacts/career-package --role "Principal AI Systems Engineer"
akos-career verify --output artifacts/career-package
```

The package contains ATS text, Markdown, semantic responsive HTML, CSS, JSON-LD, a deterministic target report, a generated DOCX, a generated multipage PDF, the canonical source projection, a hash manifest, and a build receipt.

DOCX and PDF files are generated with the Python standard library from the source projection. Identical source and target inputs produce identical files, manifests, and build identifiers. The verifier rejects invalid facts, malformed metadata, unsafe paths, missing files, size or hash drift, corrupted document structures, executable-script drift, tracker insertion, and receipt inconsistency.

Targeting may reorder or prioritize only existing source facts. It may not invent claims, employers, metrics, credentials, affiliations, production status, or outcomes.
