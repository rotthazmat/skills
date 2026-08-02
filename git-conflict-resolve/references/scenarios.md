# Conflict Scenario Examples

Worked examples of the most common conflict patterns. In every case, `git show <hash> -- <file>` is the source of truth — never the conflict markers alone.

---

## Scenario A — Commit modified lines inside a function that has since moved

**What happened:** The cherry-picked commit changed 2 lines inside `processOrder()`. After that commit, someone moved `processOrder()` from line 45 to line 120 in the same file.

**`git show <hash> -- <file>` shows:**
```diff
-    $total = array_sum($items);
+    $total = array_sum($items) + $shipping;
```

**What the conflict markers show:**
```
<<<<<<< HEAD
  (function not here — it moved to line 120)
=======
  function processOrder(array $items): float
  {
    $total = array_sum($items) + $shipping;
    return $total;
  }
>>>>>>> abc1234
```

**Wrong resolution:** Accept the full incoming side — this duplicates a function already at line 120.

**Correct resolution:**
1. Discard the entire incoming conflict block.
2. Find `processOrder()` at line 120 in HEAD.
3. Apply only the one-line change there: replace `array_sum($items)` with `array_sum($items) + $shipping`.

---

## Scenario B — Commit added a new method; the surrounding code was renamed

**What happened:** The cherry-picked commit added `getLabel()` after `getValue()`. In HEAD, `getValue()` was renamed to `resolve()` in a later refactor.

**`git show <hash> -- <file>` shows:**
```diff
  public function getValue(): string
  {
    return $this->value;
  }
+
+ public function getLabel(): string
+ {
+   return $this->label;
+ }
```

**Correct resolution:** Insert `getLabel()` after `resolve()` in HEAD (the renamed equivalent of `getValue()`). Do not restore `getValue()` — the rename stands.

---

## Scenario C — Commit deleted a method that HEAD already removed

**What happened:** The cherry-picked commit deleted `legacyFormat()`. In HEAD, the method was already removed in an earlier refactor.

**`git show <hash> -- <file>` shows:**
```diff
- public function legacyFormat(): string
- {
-   return $this->value . '_legacy';
- }
```

**What the conflict markers show:**
```
<<<<<<< HEAD
  (method not present — already removed in HEAD)
=======
  public function legacyFormat(): string
  {
    return $this->value . '_legacy';
  }
>>>>>>> abc1234
```

**Correct resolution:** This is a no-op — the method is already gone from HEAD. Accept HEAD (empty). Do not re-introduce `legacyFormat()`.

---

## Scenario D — Rebase conflict: both sides added code to the same constructor

**What happened:** Your feature branch added `$discount` to `__construct()`. While you worked, the base branch also added `$taxRate` to the same constructor.

**Base branch `__construct` (HEAD):**
```php
public function __construct(
  private readonly string $currency,
  private readonly float $taxRate,
) {}
```

**Your commit adds (from `git show`):**
```diff
  public function __construct(
+   private readonly float $discount,
    private readonly string $currency,
  ) {}
```

**Correct resolution — merge both, keep alphabetical order:**
```php
public function __construct(
  private readonly string $currency,
  private readonly float $discount,
  private readonly float $taxRate,
) {}
```

Both changes are preserved. Properties remain alphabetically sorted per convention.

---

## Scenario E — Net-zero change across a series of cherry-picked commits

**What happened:** You cherry-pick three commits: A moves `validate()` to a trait, B adds one line inside it, C moves it back.

**Expected net result:**
- `validate()` exists in its original location (moves cancel out).
- It contains the one line added by commit B (the only real change).

**Verify after all three commits:**
```bash
git diff HEAD~3 HEAD -- <file>
```
This should show **only** the single-line addition from commit B — nothing else. If it shows any structural differences, re-examine the series.
