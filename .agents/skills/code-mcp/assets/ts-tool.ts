import type { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { handleToolError } from "../lib/errors.js";
// import { ExampleService } from "../lib/example-service.js";

// Define schemas once — import from lib/types.ts if shared across files
const ExampleInputSchema = {
  query: z.string().describe("Description of what this argument represents"),
};

const ExampleOutputSchema = z.object({
  result: z.string(),
});

// const service = new ExampleService();

export function registerExampleTools(server: McpServer): void {
  server.registerTool(
    "example-tool",
    {
      description: "Brief description of what this tool does and when to use it",
      inputSchema: ExampleInputSchema,
      outputSchema: ExampleOutputSchema,
    },
    async ({ query }) => {
      try {
        // const result = await service.process(query);
        const result = { result: `Processed: ${query}` };

        return {
          content: [{ type: "text" as const, text: result.result }],
          structuredContent: result,
        };
      } catch (err) {
        return handleToolError(err);
      }
    }
  );
}
