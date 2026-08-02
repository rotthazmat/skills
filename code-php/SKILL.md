---
name: code-php
description: PHP code style, design patterns, naming conventions, and testing rules. Use when writing or reviewing PHP classes, services, or Pest/PHPUnit test files.
---

Apply the following rules to all PHP code you write or review.

## Code Style

- **2-space indentation** — no tabs
- **Single quotes** for strings unless interpolation is needed
- **No Yoda comparisons** — `$x === 'value'`, not `'value' === $x`
- **Use `===` and `!==`** — never `==` or `!=`
- **Use null-coalescing operators** `??` instead of ternary isset checks
- **Short array syntax** `[]` — never `array()`
- **Max line length: 120 characters** — ternary operators exceeding this must be multi-line
- **Max file length: 400 lines** (excludes test files)
- **Max function length: 100 lines**
- **Opening brace on same line** as function/method (Kernighan & Ritchie style)
- **No blank line between methods**, none before first or after last
- **Array keys must be alphabetically sorted** — applies to all associative arrays including context and config arrays
- **`use` imports must be alphabetically sorted**
- **No unused imports, no unused variables, no unused parameters**
- **No empty functions**
- **Declare types**: always use typed properties, parameter types, and return types
- **Forbidden debug functions**: `var_dump`, `print_r`, `dd`
- **No silenced errors** — `@function()` is forbidden
- **Sanitize output** — use escaping functions or parameterized queries before embedding user-supplied values in HTML, attributes, or queries

## Design Patterns

- **Fluent Interface** — All setters return `$this` or `static` for method chaining
- **Dependency Injection** — Constructor injection with `readonly` typed properties
- **Strategy Pattern** — Route behavior through enums or interface implementations
- **Hook-Based Init** — Classes register framework hooks in `__construct()`
- **Enum Patterns** — Use backed enums to represent domain values with metadata

## Naming Conventions

- **Classes** — PascalCase
- **Methods** — camelCase
- **Constants** — UPPER_SNAKE_CASE
- **Namespaces mirror directory structure**

## Testing (Pest / PHPUnit)

**Unit test pattern** — use `beforeEach`/`afterEach` to reset mocking state per test:

```php
beforeEach(function () {
  Monkey\setup();
});

afterEach(function () {
  Monkey\tearDown();
  Mockery::close();
});

test('does the thing', function () {
  $result = (new MyClass())->doThing();
  expect($result)->toBe('expected');
});
```

**Integration test pattern** — use `beforeAll`/`afterAll` for one-time setup per file:

```php
beforeAll(function () {
  // shared setup once
});

afterAll(function () {
  Mockery::close();
});
```

**Parameterized tests** with `->with()`:

```php
test('behaves correctly', function (bool $flag) {
  // ...
})->with([
  'enabled' => [true],
  'disabled' => [false],
]);
```

**Mocking**: use Mockery for objects, Brain\Monkey\Functions for global/framework functions.

**Critical rule — never mix `when` and `expect` for the same function in the same scope:**

Calling `Functions\when('fn')->justReturn(...)` in `beforeEach` and then `Functions\expect('fn')->once()->with(...)` in a specific test causes a conflict — the `when` takes precedence and the assertion is never verified. Set mocks individually per test — either `when` or `expect`, never both for the same function.

```php
// WRONG
beforeEach(function () {
  Functions\when('some_fn')->justReturn(''); // conflicts with expect() below
});
test('asserts call', function () {
  Functions\expect('some_fn')->once()->with('X')->andReturn('Y'); // never fires
});

// CORRECT
beforeEach(function () {
  // some_fn NOT mocked here
});
test('default case', function () {
  Functions\when('some_fn')->justReturn('');
});
test('asserts call', function () {
  Functions\expect('some_fn')->once()->with('X')->andReturn('Y');
});
```

## Resources

- **`references/patterns.md`** — full design pattern examples with code. Load when implementing or reviewing patterns (fluent interface, DI, enums, strategy, hooks).
- **`assets/class-template.php`** — base template for a new PHP service class.
- **`assets/pest-test-template.php`** — base template for a Pest test file.
- **`evals/evals.json`** — test cases to verify this skill produces correct reviews.
