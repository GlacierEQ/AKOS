import { createServer, type ServerResponse } from "node:http";
import { pathToFileURL } from "node:url";
import {
  buildEvidenceManifest,
  createArtifactTwin,
  parsePipelineInput,
  processInput,
} from "./pipeline.js";

const DEFAULT_PORT = 8787;
const MAX_BODY_BYTES = 1_048_576;

export const ACTIVE_PISTONS = [
  "M2_REDACTION_AND_SECRET_GUARD",
  "M3_NORMALIZATION_AND_DEDUP",
  "M4_VERIFICATION_AND_PROVENANCE",
  "M6_CONTRADICTION_GRAPH",
  "M7_EVIDENCE_MANIFEST",
  "M8_DOCUMENT_GENERATOR",
  "M11_HEALTH_AND_AUDIT",
] as const;

function writeJson(response: ServerResponse, statusCode: number, value: unknown): void {
  response.writeHead(statusCode, {
    "content-type": "application/json; charset=utf-8",
    "cache-control": "no-store",
    "x-content-type-options": "nosniff",
  });
  response.end(JSON.stringify(value));
}

export function createAkosServer() {
  return createServer((request, response) => {
    const pathname = new URL(request.url ?? "/", "http://akos.local").pathname;

    if (request.method === "GET" && pathname === "/health") {
      writeJson(response, 200, {
        status: "ok",
        service: "akos-runtime",
        version: "0.3.0",
        pistons: ACTIVE_PISTONS.length,
      });
      return;
    }

    if (request.method === "GET" && pathname === "/pistons") {
      writeJson(response, 200, { pistons: ACTIVE_PISTONS });
      return;
    }

    if (request.method === "POST" && pathname === "/execute") {
      const chunks: Buffer[] = [];
      let receivedBytes = 0;
      let rejected = false;

      request.on("data", (chunk: Buffer | string) => {
        if (rejected) return;
        const buffer = Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk);
        receivedBytes += buffer.byteLength;
        if (receivedBytes > MAX_BODY_BYTES) {
          rejected = true;
          writeJson(response, 413, { error: "payload_too_large", maxBytes: MAX_BODY_BYTES });
          request.destroy();
          return;
        }
        chunks.push(buffer);
      });

      request.on("end", () => {
        if (rejected || response.writableEnded) return;
        try {
          const parsed = JSON.parse(Buffer.concat(chunks).toString("utf8")) as unknown;
          const input = parsePipelineInput(parsed);
          const object = processInput(input);
          const artifactTwin = object.disposition === "QUARANTINE"
            ? null
            : createArtifactTwin(object, { courtFacing: input.courtFacing === true });

          writeJson(response, 200, {
            object,
            manifestRoot: buildEvidenceManifest([object]),
            artifactTwin,
          });
        } catch (error) {
          writeJson(response, 400, {
            error: error instanceof Error ? error.message : "invalid_request",
          });
        }
      });

      request.on("error", (error) => {
        if (!response.writableEnded) {
          writeJson(response, 400, { error: error.message });
        }
      });
      return;
    }

    writeJson(response, 404, { error: "not_found" });
  });
}

const entrypoint = process.argv[1];
if (entrypoint && import.meta.url === pathToFileURL(entrypoint).href) {
  const port = Number(process.env.PORT ?? DEFAULT_PORT);
  const server = createAkosServer();
  server.listen(port, "0.0.0.0", () => {
    console.log(JSON.stringify({ event: "akos_runtime_started", port, version: "0.3.0" }));
  });
}
