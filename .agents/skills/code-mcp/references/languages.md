# MCP Language Reference

Per-language setup, packages, and entry-point patterns. Load this file when generating code for a specific language.

---

## TypeScript / JavaScript (Tier 1)

**Install:**
```bash
npm install @modelcontextprotocol/sdk zod
npm install -D typescript @types/node vitest
```

**package.json essentials:**
```json
{
  "type": "module",
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js",
    "dev": "tsx src/index.ts",
    "test": "vitest"
  }
}
```

**tsconfig.json essentials:**
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "Node16",
    "moduleResolution": "Node16",
    "outDir": "dist",
    "strict": true
  }
}
```

**Entry point pattern:**
```ts
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { registerWeatherTools } from "./tools/weather.js";

const server = new McpServer({ name: "my-server", version: "1.0.0" });

registerWeatherTools(server);

const transport = new StdioServerTransport();
await server.connect(transport);
```

**Schema validation:** Zod (`z.string().describe("...")`)

---

## Python (Tier 1)

**Install:**
```bash
uv add mcp
# or
pip install mcp
```

**Entry point pattern:**
```python
from mcp.server.fastmcp import FastMCP
from .tools.weather import register_weather_tools

mcp = FastMCP("my-server")
register_weather_tools(mcp)

if __name__ == "__main__":
    mcp.run()
```

**Tool registration pattern:**
```python
def register_weather_tools(mcp: FastMCP) -> None:
    @mcp.tool()
    async def get_forecast(city: str) -> str:
        """Get weather forecast for a city."""
        return await WeatherService().get_forecast(city)
```

**Schema validation:** Pydantic v2 or plain type hints (FastMCP auto-generates schemas from type hints)

**Testing:** pytest + anyio
```bash
uv add --dev pytest pytest-anyio
```

---

## C# (Tier 1)

**Install:**
```bash
dotnet add package ModelContextProtocol
```

**Entry point pattern:**
```csharp
using ModelContextProtocol.Server;

var builder = McpServerBuilder.Create("my-server", "1.0.0");
builder.AddTools<WeatherTools>();
var server = builder.Build();
await server.RunAsync();
```

**Tool registration pattern:**
```csharp
[McpServerToolType]
public class WeatherTools
{
    [McpServerTool, Description("Get weather forecast for a city")]
    public async Task<string> GetForecast([Description("City name")] string city)
        => await _weatherService.GetForecastAsync(city);
}
```

**Schema validation:** Data annotations + `System.ComponentModel.Description`

**Testing:** xUnit or NUnit

---

## Go (Tier 1)

**Install:**
```bash
go get github.com/modelcontextprotocol/go-sdk/mcp
```

**Entry point pattern:**
```go
package main

import (
    "github.com/modelcontextprotocol/go-sdk/mcp"
    "github.com/modelcontextprotocol/go-sdk/mcp/stdio"
)

func main() {
    s := mcp.NewServer("my-server", "1.0.0", nil)
    registerWeatherTools(s)
    stdio.NewTransport().Run(s)
}
```

**Tool registration pattern:**
```go
func registerWeatherTools(s *mcp.Server) {
    s.AddTool(mcp.NewTool("get-forecast",
        mcp.WithDescription("Get weather forecast"),
        mcp.WithString("city", mcp.Required(), mcp.Description("City name")),
    ), handleGetForecast)
}
```

**Testing:** stdlib `testing` + `testify`

---

## Java (Tier 2)

**Install (Maven):**
```xml
<dependency>
    <groupId>io.modelcontextprotocol</groupId>
    <artifactId>sdk</artifactId>
    <version>LATEST</version>
</dependency>
```

**Entry point pattern:**
```java
McpServer server = McpServer.builder()
    .name("my-server")
    .version("1.0.0")
    .tools(new WeatherTools())
    .build();
server.run();
```

**Testing:** JUnit 5 + Mockito

---

## Rust (Tier 2)

**Install:**
```bash
cargo add mcp-sdk
```

**Entry point pattern:**
```rust
use mcp_sdk::server::{Server, StdioTransport};

#[tokio::main]
async fn main() {
    let server = Server::builder("my-server", "1.0.0")
        .register_tools(register_weather_tools)
        .build();
    server.run(StdioTransport::new()).await.unwrap();
}
```

**Testing:** Rust built-in `#[test]` + `tokio::test`

---

## Swift (Tier 3)

**Install (Package.swift):**
```swift
.package(url: "https://github.com/modelcontextprotocol/swift-sdk", from: "0.1.0")
```

Primarily for macOS/iOS. Entry point follows the same instantiate → register → connect pattern.

**Testing:** XCTest

---

## Ruby (Tier 3)

**Install:**
```bash
bundle add mcp
```

Entry point follows register → run pattern via the `MCP::Server` class.

**Testing:** RSpec

---

## PHP (Tier 3)

**Install:**
```bash
composer require modelcontextprotocol/sdk
```

Entry point follows the instantiate → register → run pattern.

**Testing:** PHPUnit / Pest
