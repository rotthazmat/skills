---
name: code-mcp
description: MCP server scaffolding and code generation following SOLID principles, separation of concerns, and DRY patterns. Use when creating, extending, scaffolding, or reviewing Model Context Protocol servers in any supported language.
user-invocable: true
argument-hint: "e.g. TypeScript MCP with weather tools"
---

# MCP Server Creation

---

## Step 1 — Select language

**Always ask the user which language they prefer before writing any code.** Show this menu every time:

| # | Language | Tier | Package manager |
|---|---|---|---|
| 1 | TypeScript / JavaScript | Tier 1 | npm / pnpm |
| 2 | Python | Tier 1 | uv / pip |
| 3 | C# | Tier 1 | NuGet |
| 4 | Go | Tier 1 | go mod |
| 5 | Java | Tier 2 | Maven / Gradle |
| 6 | Rust | Tier 2 | Cargo |
| 7 | Swift | Tier 3 | Swift Package Manager |
| 8 | Ruby | Tier 3 | Bundler |
| 9 | PHP | Tier 3 | Composer |

Default to **TypeScript** only if the user explicitly says they don't mind or skips the question.

After confirming language, ask:
- What should the server expose? (tools / resources / prompts)
- Does it need external APIs, database access, or file system access?

Load `references/languages.md` for language-specific setup, packages, and entry-point boilerplate.

---

## Step 2 — Project structure

Use this layout for every MCP server regardless of language (adapt casing/paths to language conventions):

```
<project>/
  src/
    index.ts            ← server entry: instantiate server, register all handlers, connect transport
    tools/
      <domain>.ts       ← one file per tool domain (weather, github, database…)
    resources/
      <domain>.ts       ← one file per resource domain
    prompts/
      <name>.ts         ← one file per prompt template
    lib/
      <service>.ts      ← pure business logic — zero MCP SDK imports
      types.ts          ← shared interfaces and Zod schemas
      errors.ts         ← custom error classes and shared error handler
  tests/
    unit/
      lib/              ← test lib/ services in isolation (no MCP)
    integration/
      tools/            ← test tool handlers end-to-end via MCP test client
  package.json
  tsconfig.json
```

Rules:
- `index.ts` wires registrations and transport only — no business logic, no API calls
- `lib/` has zero MCP SDK imports; it is pure domain code
- Each `tools/<domain>.ts` exports a single `register<Domain>Tools(server)` function
- Shared Zod schemas and types belong in `lib/types.ts` — never duplicated across files
- Each test file mirrors its source: `tests/unit/lib/weather-service.test.ts` → `src/lib/weather-service.ts`

---

## Step 3 — SOLID + DRY rules

### Single Responsibility
- One tool domain per file; the file owns schema + handler for that domain only
- Handlers transform data into MCP response format — they do not fetch or compute data

### Open/Closed
- Add new tools by creating new domain files and calling their `register*` function in `index.ts`
- Never modify an existing tool domain file to add unrelated functionality

### Interface Segregation
- Define narrow interfaces in `lib/types.ts` (e.g. `HttpClient`, `DbClient`)
- Pass those interfaces into services — never the whole server object

### Dependency Inversion
- Services accept interface dependencies, not concrete implementations
- Enables unit testing without real HTTP calls or database connections

### DRY
- Define every Zod schema once — in `lib/types.ts` or at the top of its tool file — never copy it
- Extract `toTextContent(text: string)` and `handleToolError(err: unknown)` helpers the moment they appear in more than one place
- Wrap handlers in a shared `wrapToolHandler(fn)` utility that catches and formats all errors uniformly

---

## Step 4 — Transport

| Context | Transport class |
|---|---|
| Claude Desktop / Claude Code (local) | `StdioServerTransport` |
| Remote / web server | `StreamableHTTPServerTransport` |
| Legacy remote | `SSEServerTransport` |

- Configure transport in `index.ts` only — never in tool or service files
- `await server.connect(transport)` must come **after** all `register*` calls

---

## Step 5 — Error handling

- Wrap every tool handler body in try/catch
- Return `{ isError: true, content: [{ type: "text", text: message }] }` on failure — never throw
- Define a shared `handleToolError(err: unknown): ToolResponse` in `lib/errors.ts`
- Use Zod `.describe(...)` on every input field — this is not optional, it improves model accuracy significantly

---

## Step 6 — Testing

Load `references/testing-guide.md` for full detail. Summary:

**Unit tests** — test `lib/` services with mocked dependencies; no MCP involved:
```ts
// tests/unit/lib/weather-service.test.ts
it('returns forecast for valid city', async () => {
  const svc = new WeatherService(mockHttpClient);
  const result = await svc.getForecast('London');
  expect(result.temperature).toBeTypeOf('number');
});
```

**Integration tests** — test tool handlers end-to-end using an in-memory MCP client:
```ts
// tests/integration/tools/weather.test.ts
it('fetch-forecast tool returns structured content', async () => {
  const { client } = await createTestServer();
  const result = await client.callTool({ name: 'fetch-forecast', arguments: { city: 'London' } });
  expect(result.isError).toBeFalsy();
});
```

**Inspector testing** — run `npx @modelcontextprotocol/inspector` for manual end-to-end verification before shipping.

Default test frameworks by language: TypeScript → Vitest, Python → pytest + anyio, Go → stdlib `testing`, Java → JUnit 5, Rust → built-in `#[test]`.

---

## Gotchas

- **`outputSchema` requires SDK ≥ 1.x** — check the installed version before using it; omit for older versions
- **Never write to stdout in handlers** — `StdioServerTransport` uses stdout for the protocol; use `server.sendLoggingMessage()` or stderr instead
- **All `register*` calls must complete before `server.connect()`** — async registrations that haven't resolved will be skipped
- **Zod `.describe()` on every input field** — without it the model guesses argument meaning and makes mistakes
- **Python: use `anyio.run()` not `asyncio.run()`** — the MCP Python SDK is transport-agnostic; `asyncio` alone may conflict with some transports

---

## Anti-patterns

| Anti-pattern | Why bad | Fix |
|---|---|---|
| Business logic in `index.ts` | Couples MCP wiring to domain logic | Move to `lib/` service |
| Duplicated Zod schemas | Schema drift — bugs fixed in one copy only | Single definition in `lib/types.ts` |
| One giant `tools.ts` file | Violates SRP, causes merge conflicts | Split by domain |
| `any` typed inputs | No runtime validation, silent failures | Always use Zod or language equivalent |
| Throwing from handlers | Crashes or hangs the MCP client | Return `{ isError: true }` |
| `console.log` in handlers | Corrupts stdio transport | Use `server.sendLoggingMessage()` |
| Unit tests that import the MCP SDK | Slow, coupled to transport | Unit-test `lib/` only; use MCP client in integration tests |

---

## Resources

- **`references/languages.md`** — install commands, packages, and entry-point boilerplate per language. Load when generating code for any language.
- **`references/typescript-patterns.md`** — TypeScript patterns: Zod schemas, tool registration, service layer, error utilities. Load when writing TypeScript MCP servers.
- **`references/testing-guide.md`** — unit + integration test setup per language, MCP Inspector usage, test utilities. Load when adding or reviewing tests.
- **`assets/ts-entry.ts`** — TypeScript `index.ts` template. Use as the base for the server entry file.
- **`assets/ts-tool.ts`** — TypeScript tool domain module template. Use when scaffolding a new tool file.
- **`assets/ts-test.ts`** — TypeScript test templates (unit + integration). Use when generating test files.
- **`evals/evals.json`** — test cases.
