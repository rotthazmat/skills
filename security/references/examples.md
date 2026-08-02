# Security Pattern Examples

## SQL — parameterized queries

```php
// WRONG — SQL injection risk
$query = "SELECT * FROM users WHERE email = '$email'";
$result = $db->query($query);

// CORRECT — parameterized
$stmt = $db->prepare('SELECT * FROM users WHERE email = ?');
$stmt->execute([$email]);

// CORRECT — named parameters
$stmt = $db->prepare('SELECT * FROM users WHERE email = :email AND active = :active');
$stmt->execute([':active' => 1, ':email' => $email]);
```

## HTML output — escape for context

```php
// WRONG — XSS risk (unescaped output in HTML body)
echo '<p>' . $userInput . '</p>';

// WRONG — XSS risk (unescaped output in HTML attribute)
echo '<input value="' . $userInput . '">';

// CORRECT — escape for HTML body
echo '<p>' . htmlspecialchars($userInput, ENT_QUOTES, 'UTF-8') . '</p>';

// CORRECT — escape for HTML attribute
echo '<input value="' . htmlspecialchars($userInput, ENT_QUOTES, 'UTF-8') . '">';
```

## No eval()

```php
// WRONG — remote code execution risk
eval('return ' . $userInput . ';');

// WRONG — same risk via create_function
$fn = create_function('', $userInput);

// CORRECT — whitelist allowed operations
$ops = [
  'add' => fn(float $a, float $b): float => $a + $b,
  'sub' => fn(float $a, float $b): float => $a - $b,
];
$result = isset($ops[$op]) ? $ops[$op]($a, $b) : null;
```

## External calls — wrap, log, return null

```php
// WRONG — exceptions propagate to the user; stack trace leaks internals
public function fetchData(string $url): array
{
  $response = $this->client->get($url);
  return $response->json();
}

// CORRECT — catch, log with context, return null
public function fetchData(string $url): ?array
{
  try {
    return $this->client->get($url)->json();
  } catch (\Throwable $e) {
    $this->logger->error('External fetch failed', ['error' => $e->getMessage(), 'url' => $url]);
    return null;
  }
}
```

## No circular delegation

```php
// WRONG — infinite recursion
class ServiceA
{
  public function handle(): void { $this->b->process(); }
}
class ServiceB
{
  public function process(): void { $this->a->handle(); }  // loops back to A
}

// CORRECT — unidirectional flow
class ServiceA
{
  public function handle(): void { $this->b->process(); }
}
class ServiceB
{
  public function process(): void { /* no call back into A */ }
}
```

## JavaScript — no innerHTML with user content

```js
// WRONG — XSS risk
element.innerHTML = userInput;
document.write(userInput);

// CORRECT — use textContent for plain text
element.textContent = userInput;

// CORRECT — build structured content with DOM APIs
const p = document.createElement('p');
p.textContent = userInput;
container.appendChild(p);
```
