import { CreateMLCEngine, MLCEngine } from "@mlc-ai/web-llm";

const DEFAULT_MODEL = "Llama-3.2-1B-Instruct-q4f32_1-MLC";

const $ = (id: string) => document.getElementById(id) as HTMLElement;
const log = (msg: string) => { $("log").textContent += msg; };

let engine: MLCEngine | null = null;

async function loadModel(model: string): Promise<void> {
  log(`Loading ${model} ...\n`);
  engine = await CreateMLCEngine(model, {
    initProgressCallback: (p) => log(`  ${p.text}\n`),
  });
  log("\nReady.\n\n");
}

async function ask(prompt: string): Promise<void> {
  if (!engine) throw new Error("engine not loaded");
  log(`\n> ${prompt}\n`);
  const stream = await engine.chat.completions.create({
    messages: [
      { role: "system", content: "You are a concise assistant. Reply in Korean if asked in Korean." },
      { role: "user", content: prompt },
    ],
    stream: true,
    temperature: 0.7,
  });
  for await (const chunk of stream) {
    log(chunk.choices[0]?.delta?.content || "");
  }
  log("\n");
}

document.addEventListener("DOMContentLoaded", () => {
  ($("load") as HTMLButtonElement).onclick = () => loadModel(DEFAULT_MODEL);
  ($("ask") as HTMLButtonElement).onclick = () =>
    ask(($("prompt") as HTMLInputElement).value);
});
