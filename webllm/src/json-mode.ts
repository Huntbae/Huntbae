// JSON mode example — force the model to return a JSON object matching a schema.

import { CreateMLCEngine } from "@mlc-ai/web-llm";

const schema = {
  type: "object",
  properties: {
    title: { type: "string" },
    tags: { type: "array", items: { type: "string" } },
    rating: { type: "number", minimum: 0, maximum: 5 },
  },
  required: ["title", "tags", "rating"],
};

export async function extractMovieInfo(text: string) {
  const engine = await CreateMLCEngine("Llama-3.2-3B-Instruct-q4f32_1-MLC");
  const resp = await engine.chat.completions.create({
    messages: [
      { role: "system", content: "Extract movie info as JSON." },
      { role: "user", content: text },
    ],
    response_format: {
      type: "json_object",
      schema: JSON.stringify(schema),
    },
  });
  return JSON.parse(resp.choices[0].message.content ?? "{}");
}
