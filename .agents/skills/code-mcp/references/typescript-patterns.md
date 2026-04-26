# TypeScript MCP Patterns

Detailed patterns for TypeScript MCP servers. Load when writing or reviewing TypeScript code.

---

## Zod schema patterns

Always define schemas once in `lib/types.ts` and import them into tool files:

```ts
// src/lib/types.ts
import { z } from "zod";

export const ForecastInputSchema = z.object({
  city: z.string().describe("City name (e.g. 'London', 'Tokyo')"),
  days: z.number().int().min(1).max(7).optional().default(3)
    .describe("Number of forecast days (1–7, default 3)"),
});

export const ForecastOutputSchema = z.object({
  city: z.string(),
  temperature: z.number(),
  condition: z.string(),
  days: z.array(z.object({
    date: z.string(),
    high: z.number(),
    low: z.number(),
  })),
});

export type ForecastInput = z.infer<typeof ForecastInputSchema>;
export type ForecastOutput = z.infer<typeof ForecastOutputSchema>;
```

---

## Service layer pattern

Services live in `lib/` and have zero MCP SDK imports:

```ts
// src/lib/weather-service.ts
import type { HttpClient } from "./types.js";
import type { ForecastOutput } from "./types.js";

export class WeatherService {
  constructor(private readonly http: HttpClient) {}

  async getForecast(city: string, days: number): Promise<ForecastOutput> {
    const data = await this.http.get(`/forecast?city=${city}&days=${days}`);
    return {
      city: data.name,
      temperature: data.main.temp,
      condition: data.weather[0].description,
      days: data.daily.slice(0, days).map((d: any) => ({
        date: d.dt_txt,
        high: d.temp.max,
        low: d.temp.min,
      })),
    };
  }
}
```

---

## Tool registration pattern

Each tool domain file exports one `register*` function:

```ts
// src/tools/weather.ts
import type { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { ForecastInputSchema, ForecastOutputSchema } from "../lib/types.js";
import { WeatherService } from "../lib/weather-service.js";
import { FetchHttpClient } from "../lib/http-client.js";
import { handleToolError } from "../lib/errors.js";

const service = new WeatherService(new FetchHttpClient());

export function registerWeatherTools(server: McpServer): void {
  server.registerTool(
    "get-forecast",
    {
      description: "Get weather forecast for a city",
      inputSchema: ForecastInputSchema,
      outputSchema: ForecastOutputSchema,
    },
    async ({ city, days }) => {
      try {
        const result = await service.getForecast(city, days);
        return {
          content: [{ type: "text", text: `${city}: ${result.temperature}°C, ${result.condition}` }],
          structuredContent: result,
        };
      } catch (err) {
        return handleToolError(err);
      }
    }
  );
}
```

---

## Error utility

```ts
// src/lib/errors.ts
export class ServiceError extends Error {
  constructor(message: string, public readonly cause?: unknown) {
    super(message);
    this.name = "ServiceError";
  }
}

export function handleToolError(err: unknown) {
  const message = err instanceof Error ? err.message : String(err);
  return {
    isError: true as const,
    content: [{ type: "text" as const, text: message }],
  };
}
```

---

## Shared content helpers

Extract these as soon as they appear more than once:

```ts
// src/lib/content.ts
export function toTextContent(text: string) {
  return { type: "text" as const, text };
}

export function toErrorContent(message: string) {
  return { isError: true as const, content: [toTextContent(message)] };
}
```

---

## HttpClient interface (Dependency Inversion)

```ts
// src/lib/types.ts (add to existing file)
export interface HttpClient {
  get<T>(path: string): Promise<T>;
  post<T>(path: string, body: unknown): Promise<T>;
}

// src/lib/http-client.ts
import type { HttpClient } from "./types.js";

export class FetchHttpClient implements HttpClient {
  constructor(private readonly baseUrl: string) {}

  async get<T>(path: string): Promise<T> {
    const res = await fetch(`${this.baseUrl}${path}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}: ${res.statusText}`);
    return res.json() as T;
  }

  async post<T>(path: string, body: unknown): Promise<T> {
    const res = await fetch(`${this.baseUrl}${path}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}: ${res.statusText}`);
    return res.json() as T;
  }
}
```

---

## Complete `index.ts` wiring example

```ts
// src/index.ts
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { registerWeatherTools } from "./tools/weather.js";
import { registerStocksTools } from "./tools/stocks.js";

const server = new McpServer({
  name: "my-server",
  version: "1.0.0",
});

registerWeatherTools(server);
registerStocksTools(server);

const transport = new StdioServerTransport();
await server.connect(transport);
```

---

## Resource registration pattern

```ts
// src/resources/docs.ts
import type { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";

export function registerDocsResources(server: McpServer): void {
  server.resource("api-docs", "file:///docs/api.md", async (uri) => ({
    contents: [{ uri: uri.href, text: await readFile(uri.pathname, "utf8") }],
  }));
}
```

---

## Prompt registration pattern

```ts
// src/prompts/summarize.ts
import type { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";

export function registerSummarizePrompts(server: McpServer): void {
  server.prompt(
    "summarize",
    { text: z.string().describe("Text to summarize") },
    ({ text }) => ({
      messages: [{
        role: "user",
        content: { type: "text", text: `Summarize the following:\n\n${text}` },
      }],
    })
  );
}
```
