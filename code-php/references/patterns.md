# PHP Pattern Examples

## Fluent Interface

All setters return `$this` or `static` to support chaining:

```php
final class QueryBuilder
{
  private array $conditions = [];
  private ?int $limit = null;

  public function limit(int $count): static
  {
    $this->limit = $count;
    return $this;
  }

  public function where(string $column, mixed $value): static
  {
    $this->conditions[$column] = $value;
    return $this;
  }
}

// Usage
$query = (new QueryBuilder())
  ->limit(10)
  ->where('status', 'active');
```

## Dependency Injection

Constructor injection with `readonly` typed properties — no setter injection:

```php
final class UserService
{
  public function __construct(
    private readonly HttpClientInterface $client,
    private readonly LoggerInterface $logger,
  ) {}

  public function find(int $id): ?User
  {
    try {
      return User::fromArray($this->client->get('/users/' . $id)->json());
    } catch (\Throwable $e) {
      $this->logger->error('User fetch failed', ['error' => $e->getMessage(), 'id' => $id]);
      return null;
    }
  }
}
```

## Backed Enum with Metadata

```php
enum Status: string
{
  case Active = 'active';
  case Draft = 'draft';
  case Inactive = 'inactive';

  public function isPublic(): bool
  {
    return $this === Status::Active;
  }

  public function label(): string
  {
    return match($this) {
      Status::Active => 'Active',
      Status::Draft => 'Draft',
      Status::Inactive => 'Inactive',
    };
  }
}
```

## Strategy Pattern via Interface

```php
interface DiscountStrategy
{
  public function apply(float $price): float;
}

final class FlatDiscount implements DiscountStrategy
{
  public function __construct(private readonly float $amount) {}

  public function apply(float $price): float
  {
    return max(0.0, $price - $this->amount);
  }
}

final class PercentDiscount implements DiscountStrategy
{
  public function __construct(private readonly float $rate) {}

  public function apply(float $price): float
  {
    return $price * (1 - $this->rate);
  }
}
```

## Hook-Based Init

Classes register framework hooks in `__construct()`:

```php
final class ContentPlugin
{
  public function __construct()
  {
    add_action('init', [$this, 'register']);
    add_filter('the_content', [$this, 'filter']);
  }

  public function filter(string $content): string
  {
    return $content;
  }

  public function register(): void
  {
    // registration logic
  }
}
```

---

## Style Quick-Reference

### Sorted array keys

```php
// CORRECT
$context = [
  'email' => $user->email,
  'id' => $user->id,
  'name' => $user->name,
];

// WRONG — unsorted
$context = [
  'name' => $user->name,
  'id' => $user->id,
  'email' => $user->email,
];
```

### Sorted use imports

```php
// CORRECT
use App\Models\Order;
use App\Models\User;
use App\Services\Logger;

// WRONG — unsorted
use App\Services\Logger;
use App\Models\User;
use App\Models\Order;
```

### Null coalescing over isset ternary

```php
$name = $data['name'] ?? 'Unknown';                           // CORRECT
$name = isset($data['name']) ? $data['name'] : 'Unknown';    // WRONG
```

### Strict equality — no Yoda

```php
if ($status === 'active') { ... }   // CORRECT
if ('active' === $status) { ... }   // WRONG — Yoda
if ($status == 'active')  { ... }   // WRONG — loose
```
