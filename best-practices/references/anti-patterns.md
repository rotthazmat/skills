# Anti-Pattern Reference

## Over-engineering beyond the task

```php
// WRONG — adds retry logic, caching, and circuit breaker that nobody asked for
public function getUser(int $id): ?User
{
  if ($this->cache->has($id)) {
    return $this->cache->get($id);
  }
  for ($attempt = 0; $attempt < 3; $attempt++) {
    try {
      $user = $this->client->get($id);
      $this->cache->set($id, $user);
      return $user;
    } catch (\Throwable $e) {
      if ($attempt === 2) { break; }
      sleep(1);
    }
  }
  return null;
}

// CORRECT — only what was asked
public function getUser(int $id): ?User
{
  try {
    return $this->client->get($id);
  } catch (\Throwable $e) {
    $this->logger->error('User fetch failed', ['id' => $id]);
    return null;
  }
}
```

## Premature abstraction

```php
// WRONG — three similar lines wrapped into an abstraction nobody else needs
interface Formattable
{
  public function format(): string;
}
final class NameFormatter implements Formattable { ... }
final class EmailFormatter implements Formattable { ... }
final class PhoneFormatter implements Formattable { ... }

// CORRECT — three similar lines are fine as-is
$name = trim($name);
$email = strtolower($email);
$phone = preg_replace('/\D/', '', $phone);
```

## Unnecessary comments

```php
// WRONG — comment describes what, not why
// Loop through users and check if active
foreach ($users as $user) {
  if ($user->isActive()) {
    // add to result array
    $result[] = $user;
  }
}

// CORRECT — code is self-explanatory; no comment needed
foreach ($users as $user) {
  if ($user->isActive()) {
    $result[] = $user;
  }
}
```

## Error handling for impossible scenarios

```php
// WRONG — validates something the type system already guarantees
public function process(Order $order): void
{
  if ($order === null) {           // can never be null — typed parameter
    throw new \InvalidArgumentException('Order required');
  }
  if (!$order instanceof Order) {  // can never be false — typed parameter
    throw new \InvalidArgumentException('Must be an Order');
  }
}

// CORRECT — trust the type system
public function process(Order $order): void
{
  // implementation
}
```

## Validation deep inside implementations

```php
// WRONG — validation buried inside a service, not at the entry point
final class OrderService
{
  public function create(array $data): Order
  {
    if (empty($data['email'])) {
      throw new \InvalidArgumentException('Email required');
    }
  }
}

// CORRECT — validate at the entry point (controller/route handler)
class OrderController
{
  public function store(Request $request): Response
  {
    $request->validate(['email' => 'required|email']);
    return $this->service->create($request->validated());
  }
}
```

## Flooding templates with context

```php
// WRONG — passes the entire object; template gets 30+ properties
return view('user-card', ['user' => $user]);

// CORRECT — extract only what the template actually uses
return view('user-card', [
  'avatarUrl' => $user->avatar_url,
  'email' => $user->email,
  'name' => $user->name,
]);
```

## Wrapping deployment errors in try/catch

```php
// WRONG — hides a missing template, which is a deployment misconfiguration
try {
  return $twig->render('user/profile.html.twig', $context);
} catch (\Exception $e) {
  return '';
}

// CORRECT — let it throw; a missing template must be fixed in deployment
return $twig->render('user/profile.html.twig', $context);
```
