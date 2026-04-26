import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
// import { registerExampleTools } from "./tools/example.js";
// import { registerExampleResources } from "./resources/example.js";
// import { registerExamplePrompts } from "./prompts/example.js";

const server = new McpServer({
  name: "my-server",
  version: "1.0.0",
});

// registerExampleTools(server);
// registerExampleResources(server);
// registerExamplePrompts(server);

const transport = new StdioServerTransport();
await server.connect(transport);
