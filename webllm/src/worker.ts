// Dedicated Web Worker that hosts the WebLLM engine.
// Use with CreateWebWorkerMLCEngine on the main thread:
//
//   import { CreateWebWorkerMLCEngine } from "@mlc-ai/web-llm";
//   const engine = await CreateWebWorkerMLCEngine(
//     new Worker(new URL("./worker.ts", import.meta.url), { type: "module" }),
//     "Llama-3.2-1B-Instruct-q4f32_1-MLC",
//   );

import { WebWorkerMLCEngineHandler } from "@mlc-ai/web-llm";

const handler = new WebWorkerMLCEngineHandler();
self.onmessage = (msg: MessageEvent) => handler.onmessage(msg);
