# MCP Server Testing Guide

Full testing setup per language. Load when adding or reviewing tests for an MCP server.

---

## Testing strategy

| Layer | What to test | Tools involved |
|---|---|---|
| Unit | `lib/` services with mocked dependencies | No MCP SDK |
| Integration | Tool/resource/prompt handlers via in-memory MCP client | MCP SDK test utilities |
| Manual | Full server end-to-end | MCP Inspector |

---

## TypeScript — Vitest

### Setup
```bash
npm install -D vitest @vitest/coverage-v8
```

**vitest.config.ts:**
```ts
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    globals: true,
    environment: "node",
    coverage: { provider: "v8", include: ["src/**"] },
  },
});
```

### Unit test — service layer

```ts
// tests/unit/lib/weather-service.test.ts
import { describe, it, expect, vi } from "vitest";
import { WeatherService } from "../../../src/lib/weather-service.js";
import type { HttpClient } from "../../../src/lib/types.js";

const mockHttp: HttpClient = {
  get: vi.fn(),
  post: vi.fn(),
};

describe("WeatherService", () => {
  it("maps API response to ForecastOutput", async () => {
    vi.mocked(mockHttp.get).mockResolvedValue({
      name: "London",
      main: { temp: 15 },
      weather: [{ description: "cloudy" }],
      daily: [{ dt_txt: "2026-04-26", temp: { max: 17, min: 12 } }],
    });

    const svc = new WeatherService(mockHttp);
    const result = await svc.getForecast("London", 1);

    expect(result.city).toBe("London");
    expect(result.temperature).toBe(15);
    expect(result.days).toHaveLength(1);
  });

  it("propagates HTTP errors", async () => {
    vi.mocked(mockHttp.get).mockRejectedValue(new Error("HTTP 503"));

    const svc = new WeatherService(mockHttp);
    await expect(svc.getForecast("London", 1)).rejects.toThrow("HTTP 503");
  });
});
```

### Integration test — tool handler via MCP test client

```ts
// tests/integration/tools/weather.test.ts
import { describe, it, expect, beforeAll, afterAll } from "vitest";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { InMemoryTransport } from "@modelcontextprotocol/sdk/inMemory.js";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { registerWeatherTools } from "../../../src/tools/weather.js";

async function createTestServer() {
  const server = new McpServer({ name: "test", version: "0.0.0" });
  registerWeatherTools(server);

  const [clientTransport, serverTransport] = InMemoryTransport.createLinkedPair();
  const client = new Client({ name: "test-client", version: "0.0.0" }, {});

  await server.connect(serverTransport);
  await client.connect(clientTransport);
  return { client, server };
}

describe("get-forecast tool", () => {
  let client: Client;

  beforeAll(async () => {
    ({ client } = await createTestServer());
  });

  afterAll(async () => {
    await client.close();
  });

  it("returns forecast for valid city", async () => {
    const result = await client.callTool({
      name: "get-forecast",
      arguments: { city: "London", days: 1 },
    });
    expect(result.isError).toBeFalsy();
    expect(result.content[0].type).toBe("text");
  });

  it("returns isError for unknown city", async () => {
    const result = await client.callTool({
      name: "get-forecast",
      arguments: { city: "NOTACITY_12345" },
    });
    expect(result.isError).toBe(true);
  });

  it("lists the tool in tool list", async () => {
    const { tools } = await client.listTools();
    expect(tools.some((t) => t.name === "get-forecast")).toBe(true);
  });
});
```

---

## Python — pytest + anyio

### Setup
```bash
uv add --dev pytest pytest-anyio
```

### Unit test — service layer
```python
# tests/unit/test_weather_service.py
import pytest
from unittest.mock import AsyncMock
from src.lib.weather_service import WeatherService

@pytest.mark.anyio
async def test_get_forecast_maps_response():
    mock_http = AsyncMock()
    mock_http.get.return_value = {
        "name": "London",
        "main": {"temp": 15},
        "weather": [{"description": "cloudy"}],
        "daily": [{"dt_txt": "2026-04-26", "temp": {"max": 17, "min": 12}}],
    }

    svc = WeatherService(mock_http)
    result = await svc.get_forecast("London", days=1)

    assert result["city"] == "London"
    assert result["temperature"] == 15
```

### Integration test
```python
# tests/integration/test_weather_tools.py
import pytest
from mcp import ClientSession
from mcp.shared.memory import create_connected_server_and_client_session
from src.server import create_server

@pytest.mark.anyio
async def test_get_forecast_tool():
    server = create_server()
    async with create_connected_server_and_client_session(server) as client:
        result = await client.call_tool("get-forecast", {"city": "London"})
        assert not result.isError
```

---

## Go — stdlib testing

### Unit test
```go
// tests/unit/weather_service_test.go
package lib_test

import (
    "testing"
    "github.com/yourorg/myserver/src/lib"
)

func TestGetForecast(t *testing.T) {
    svc := lib.NewWeatherService(lib.NewMockHTTPClient(t))
    result, err := svc.GetForecast("London", 1)
    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
    if result.City != "London" {
        t.Errorf("expected London, got %s", result.City)
    }
}
```

---

## Java — JUnit 5

### Unit test
```java
// tests/unit/WeatherServiceTest.java
@ExtendWith(MockitoExtension.class)
class WeatherServiceTest {
    @Mock HttpClient httpClient;
    WeatherService service;

    @BeforeEach
    void setUp() { service = new WeatherService(httpClient); }

    @Test
    void getForecastMapsResponse() {
        when(httpClient.get(anyString())).thenReturn(mockResponse());
        ForecastOutput result = service.getForecast("London", 1);
        assertEquals("London", result.getCity());
    }
}
```

---

## Rust — built-in tests

```rust
// src/lib/weather_service.rs (at the bottom)
#[cfg(test)]
mod tests {
    use super::*;
    use mockall::predicate::*;

    #[tokio::test]
    async fn test_get_forecast() {
        let mut mock = MockHttpClient::new();
        mock.expect_get().returning(|_| Ok(mock_response()));

        let svc = WeatherService::new(mock);
        let result = svc.get_forecast("London", 1).await.unwrap();
        assert_eq!(result.city, "London");
    }
}
```

---

## MCP Inspector (all languages)

Run before shipping to manually test tools, resources, and prompts:

```bash
# TypeScript
npx @modelcontextprotocol/inspector node dist/index.js

# Python
npx @modelcontextprotocol/inspector python -m myserver

# Any compiled binary
npx @modelcontextprotocol/inspector ./myserver
```

Inspector opens at `http://localhost:5173`. Use it to:
1. Verify the tool list matches what you registered
2. Call each tool with real arguments and inspect the response
3. Check that errors return `isError: true` rather than crashing

---

## Test coverage targets

| Layer | Target | Why |
|---|---|---|
| `lib/` unit tests | 90%+ | Pure logic, easy to test, most bugs live here |
| Tool handler integration | All tools called at least once | Catches registration and schema errors |
| Error paths | At least one error case per tool | Confirms `handleToolError` is wired |
