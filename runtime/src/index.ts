import { createServer } from "node:http";
import { buildEvidenceManifest, createArtifactTwin, processInput } from "./pipeline.js";
import type { PipelineInput } from "./contracts.js";

const port = Number(process.env.PORT ?? 8787);

const server = createServer((request, response) => {
  response.setHeader("content-type", "application/json; charset=utf-8");

  if (request.method === "GET" && request.url === "/health") {
    response.writeHead(200);
    response.end(JSON.stringify({ status: "ok", service: "akos-runtime", version: "0.3.0" }));
    return;
  }

  if (request.method === "POST" && request.url === "/execute") {
    const chunks: Buffer[] = [];
    request.on("data", (chunk: Buffer) => chunks.push(chunk));
    request.on("end", () => {
      try {
        const input = JSON.parse(Buffer.concat(chunks).toString("utf8")) as PipelineInput;
        const object = processInput(input);
        const payload = {
          object,
          manifestRoot: buildEvidenceManifest([object]),
          artifactTwin: object.disposition === "QUARANTINE" ? null : createArtifactTwin(object),
        };
        response.writeHead(200);
        response.end(JSON.stringify(payload));
      } catch (error) {
        response.writeHead(400);
        response.end(JSON.stringify({ error: error instanceof Error ? error.message : "invalid_request" }));
      }
    });
    return;
  }

  response.writeHead(404);
  response.end(JSON.stringify({ error: "not_found" }));
});

server.listen(port, "0.0.0.0", () => {
  console.log(JSON.stringify({ event: "akos_runtime_started", port, version: "0.3.0" }));
});
