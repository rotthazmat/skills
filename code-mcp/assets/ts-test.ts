// =============================================================================
// UNIT TEST TEMPLATE — src/lib/<service>.ts
// =============================================================================
// tests/unit/lib/example-service.test.ts

import { describe, it, expect, vi, beforeEach } from "vitest";
// import { ExampleService } from "../../../src/lib/example-service.js";
// import type { HttpClient } from "../../../src/lib/types.js";

// const mockHttp: HttpClient = {
//   get: vi.fn(),
//   post: vi.fn(),
// };

describe("ExampleService", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("processes valid input and returns expected output", async () => {
    // Arrange
    // vi.mocked(mockHttp.get).mockResolvedValue({ /* mock API response */ });
    // const svc = new ExampleService(mockHttp);

    // Act
    // const result = await svc.process("input");

    // Assert
    // expect(result).toEqual({ result: "expected" });
  });

  it("throws ServiceError on HTTP failure", async () => {
    // vi.mocked(mockHttp.get).mockRejectedValue(new Error("HTTP 500"));
    // const svc = new ExampleService(mockHttp);
    // await expect(svc.process("input")).rejects.toThrow("HTTP 500");
  });
});


// =============================================================================
// INTEGRATION TEST TEMPLATE — tools/<domain>.ts
// =============================================================================
// tests/integration/tools/example.test.ts

import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { InMemoryTransport } from "@modelcontextprotocol/sdk/inMemory.js";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
// import { registerExampleTools } from "../../../src/tools/example.js";

async function createTestServer() {
  const server = new McpServer({ name: "test", version: "0.0.0" });
  // registerExampleTools(server);

  const [clientTransport, serverTransport] = InMemoryTransport.createLinkedPair();
  const client = new Client({ name: "test-client", version: "0.0.0" }, {});

  await server.connect(serverTransport);
  await client.connect(clientTransport);

  return { client, server };
}

describe("example-tool integration", () => {
  let client: Client;

  beforeEach(async () => {
    ({ client } = await createTestServer());
  });

  afterEach(async () => {
    await client.close();
  });

  it("returns content for valid input", async () => {
    const result = await client.callTool({
      name: "example-tool",
      arguments: { query: "test" },
    });
    expect(result.isError).toBeFalsy();
    expect(result.content[0].type).toBe("text");
  });

  it("returns isError for invalid input", async () => {
    const result = await client.callTool({
      name: "example-tool",
      arguments: { query: "" },
    });
    expect(result.isError).toBe(true);
  });

  it("appears in tool list", async () => {
    const { tools } = await client.listTools();
    expect(tools.some((t) => t.name === "example-tool")).toBe(true);
  });
});
