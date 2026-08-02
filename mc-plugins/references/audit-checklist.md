# Audit checklist

Use this when reviewing, auditing, or polishing an existing Spigot/Bukkit plugin against the four mc-plugins standards. Work through all four sections for every plugin — don't stop at the first violation found.

---

## 1. OIC UUID resolution

- [ ] Does the plugin persist any data keyed by player (balance, ownership, settings, flags, cooldown history) to a YAML file? If **no**, confirm it correctly has *no* `UUIDHelper` and *no* `softdepend: [OnlineIdentityChecker]` — adding either would itself be a violation (unused dependency).
- [ ] If **yes**, is there a `UUIDHelper` (or equivalently named) class matching the reference shape: `initialize()` that checks `getPlugin(...) != null && isEnabled()`, caches `getUUIDFromName(String)` via reflection, and `getRealUUID(Player)` that falls back to `player.getUniqueId().toString()`?
- [ ] Does `getRealUUID` return `String`? (A `UUID` return type is a known drift — flag it even though it "works," since it breaks the shared contract other plugins in the ecosystem rely on.)
- [ ] Is `softdepend: [OnlineIdentityChecker]` declared in `plugin.yml` (appended to, not replacing, any other soft-deps)?
- [ ] Grep for `player.getUniqueId()` and `player.getName()` across the codebase. For each hit, is it:
  - a **persisted YAML storage key** → violation, must route through `UUIDHelper.getRealUUID()`
  - an **in-memory-only map, display string, or permission-node lookup** → fine, not a violation
- [ ] Does resolving an **offline** target player (by name, e.g. a command argument) go through an OIC-aware helper method, or does a command handler duplicate raw `Bukkit.getOfflinePlayer(name).getUniqueId()` fallback logic inline? The latter is a minor violation — the resolution logic should live in one place.

### Good example
```java
public static String getRealUUID(Player player) {
    if (checkerAvailable && getUUIDFromNameMethod != null) {
        try {
            Object result = getUUIDFromNameMethod.invoke(onlineIdentityChecker, player.getName());
            if (result instanceof String) return (String) result;
        } catch (Exception e) { /* log and fall through */ }
    }
    return player.getUniqueId().toString();
}
```

### Bad example (flag this)
```java
// Returns UUID instead of String — breaks the shared contract
public static UUID getRealUUID(Player player) {
    ...
    return player.getUniqueId();
}
```

---

## 2. YAML comment headers

- [ ] For every non-`plugin.yml` YAML file the plugin reads/writes, is there a `private static final String XXX_HEADER` constant with a full descriptive comment block (keys, types, meaning)?
- [ ] Does the save path call `config.saveToString()`, strip residual `#` lines with `.replaceAll("(?m)^#[^\\n]*\\n?", "")`, and prepend the header — in that order?
- [ ] **Shallow-save check**: does the save method write the header constant directly (e.g. `fw.write(HEADER)`) without ever calling `saveToString()` on the live config? This is a silent data-loss bug — flag it as high severity even if the file currently holds no real keys, because it will discard the first real value written.
- [ ] Is persistence done via plain `java.io.FileWriter`, not a Paper-only API?
- [ ] Are there inline YAML comments (`key: value # note`) that the author is relying on for documentation? These get stripped on every save — the only durable place for documentation is the header constant.

### Bad example (flag this)
```java
private void saveConfigWithHeader() {
    try (FileWriter fw = new FileWriter(configFile)) {
        fw.write(CONFIG_HEADER); // never merges config.saveToString() — discards real values
    } catch (IOException e) { ... }
}
```

---

## 3. SOLID structure

- [ ] Does the main plugin class's `onEnable()` read as a wiring list (construct managers, register listeners/commands), or does it contain business logic, YAML parsing, or command-argument handling directly?
- [ ] Is there a single command class handling many subcommands with inline `if/else` or `switch` chains and ad-hoc argument parsing? Count roughly how many subcommands and how many lines. A file handling 15+ subcommands past ~400–500 lines (in practice, some grow past 800) is a God class — recommend splitting into one handler class per subcommand implementing a shared interface, dispatched by a router class.
- [ ] Before recommending a split, check whether business logic is already correctly delegated to a manager/service class and only the command-parsing layer is bloated — if so, the fix is mechanical (extract each subcommand's branch into its own class) and doesn't require touching business logic.
- [ ] Does the package layout separate concerns (`command/`, `manager/` or `config/`+`service/`, `model/`, `listener/`, `util/`)? A plugin with everything in one or two files, regardless of size, still violates SOLID if it mixes persistence, business logic, and command parsing in the same class.
- [ ] Method names follow `get*`/`set*`/`is*` Java conventions.

### Good example — command dispatch
```java
interface SubcommandHandler {
    void execute(CommandSender sender, String[] args);
}

class CommandDispatcher {
    private final Map<String, SubcommandHandler> handlers = Map.of(
        "setflag", new SetFlagHandler(configService),
        "removeflag", new RemoveFlagHandler(configService)
    );
    // onCommand looks up handlers.get(args[0].toLowerCase()) and delegates
}
```

### Bad example (flag this)
```java
// One class, 20+ subcommands, inline parsing and business logic mixed together
public boolean onCommand(CommandSender sender, Command cmd, String label, String[] args) {
    if (args[0].equalsIgnoreCase("set")) { /* 40 lines of parsing + logic */ }
    else if (args[0].equalsIgnoreCase("setwarp")) { /* 40 more lines */ }
    else if (args[0].equalsIgnoreCase("seticon")) { /* ... */ }
    // ...17 more branches...
}
```

---

## 4. Commands, permissions, and help visibility

- [ ] Do `save` and `reload` subcommands exist at all? They're mandatory on every plugin in this family, not optional — flag their absence even if nothing else about the plugin is broken.
- [ ] Does the `reload` handler call `.reload()` on *every* manager the plugin constructs (config manager **and** every data manager), or only on the config manager? Calling only the config manager's `reload()` is a real bug pattern: the command compiles, runs, and reports success while silently leaving data managers un-reloaded. Cross-check against the manager list in the main class's `onEnable()` — every manager constructed there should have a matching `.reload()` call in the `reload` subcommand.
- [ ] Does the `save` handler call `.save()` on every manager the plugin constructs, the same way? A manager left out of `save` means its in-memory state is never flushed on demand, only on whatever automatic interval (if any) the plugin uses.
- [ ] Does every command *and every subcommand* — including unglamorous ones like `save` and `reload` — have a dedicated permission node declared in `plugin.yml`?
- [ ] Is that node actually checked in code (`sender.hasPermission(node)`), not just declared?
- [ ] Grep every `hasPermission("...")` string literal in the codebase — does each one have a matching declaration in `plugin.yml`'s `permissions:` block? This is distinct from the command/subcommand check above: help-menu section gates (like PAPI visibility) aren't tied to any `commands:` entry, so they're easy to check in code and forget to declare entirely.
- [ ] Does any subcommand gate on `sender.isOp()` instead of a permission node? Flag it — it can't be granted to non-op staff through a permissions plugin.
- [ ] Do node names follow `<pluginname>.<subcommand>` (or `<pluginname>.<group>.<subcommand>` for nested features), lowercase, dot-namespaced?
- [ ] Do player-facing nodes default to `true` and admin-facing nodes default to `op`?
- [ ] Does `help` default to `true`, even in a command where every *other* subcommand is `op`? If it's been swept into the admin parent's `children` map "because the rest of the command is admin-only," flag it — `help` stays standalone with its own `default: true` so a regular player can still see a (correctly filtered) menu instead of a blanket permission denial.
- [ ] Does `sendHelp()` (or equivalent) filter each section/line by the sender's actual permission, in this order: unconditional header → unconditional `/<command> help` usage line → permission-gated "Player Commands" section (each line individually checked) → permission-gated "Server Admin Commands" section (each line individually checked)? Printing the whole menu unconditionally, or gating the entire method behind one permission check, is a violation even if `help` itself defaults to `true` correctly.
- [ ] Is there a parent node (e.g. `<plugin>.admin`) with a `children` map grouping related admin subcommands, and a top-level `<plugin>.*` wildcard covering everything?
- [ ] If the plugin registers a PlaceholderAPI expansion and documents its placeholders in `sendHelp()` (or equivalent), is that documentation section gated on a **dedicated `<plugin>.papi` permission** (declared in `plugin.yml`, `default: op`, a child of `<plugin>.admin`) — never shown unconditionally, never gated only on a player-level permission, and never gated by directly checking `<plugin>.admin` itself?
- [ ] Is the PlaceholderAPI expansion itself registered conditionally (`getPlugin("PlaceholderAPI") != null`), not as a hard `depend`?

### Bad example (flag this)
```java
// isOp() instead of a permission node — can't be delegated via a perms plugin
if (!sender.isOp()) {
    sender.sendMessage("No permission.");
    return true;
}

// PAPI docs shown to everyone, not gated at all
void sendHelp(CommandSender sender) {
    sender.sendMessage("/myplugin use");
    sender.sendMessage("--- PAPI Placeholders ---");
    sender.sendMessage("%myplugin_balance%");
}

// Bad variant: checked in code but myplugin.papi was never declared in
// plugin.yml at all. Bukkit falls back to sender.isOp() for any permission
// string with no registered Permission object, so it happens to still work
// for ops — but it can't be granted to non-op staff through a permissions
// plugin, is invisible to permission-listing tools, and is silently excluded
// from the myplugin.* wildcard's children (there's no node to include).
if (sender.hasPermission("myplugin.papi")) {
    sender.sendMessage("--- PAPI Placeholders ---");
}
```

```yaml
# Bad: help swept into the admin group just because every real subcommand is op
myplugin.admin:
  default: op
  children:
    myplugin.help: true       # wrong — blocks regular players from /myplugin help entirely
    myplugin.reload: true
    myplugin.save: true
```

```java
// Bad: reload only touches the config manager — dataManager is never reloaded.
// Compiles, runs, reports success — and silently reloads nothing but config.yml.
if (args[0].equalsIgnoreCase("reload")) {
    configManager.reload();
    sender.sendMessage("Reloaded!");
    return true;
}
```

### Good example
```java
if (!sender.hasPermission("myplugin.admin.reload")) {
    sender.sendMessage("No permission.");
    return true;
}

void sendHelp(CommandSender sender) {
    sender.sendMessage("/myplugin use");
    // Dedicated node, declared in plugin.yml as a child of myplugin.admin —
    // not a direct check of myplugin.admin itself.
    if (sender.hasPermission("myplugin.papi")) {
        sender.sendMessage("--- PAPI Placeholders ---");
        sender.sendMessage("%myplugin_balance%");
    }
}
```

```yaml
# Good: help stays standalone and default: true, even though every real
# subcommand here is admin-only
myplugin.help:
  default: true
myplugin.admin:
  default: op
  children:
    myplugin.reload: true
    myplugin.save: true
myplugin.*:
  default: op
  children:
    myplugin.help: true      # alongside, not inside, the admin group
    myplugin.admin: true
```

```java
// Good: reload calls every manager the plugin constructed in onEnable().
if (args[0].equalsIgnoreCase("reload")) {
    configManager.reload();
    dataManager.reload();
    sender.sendMessage("Reloaded!");
    return true;
}
```

---

## Reporting

Summarize per-plugin findings as: ✅ compliant / ⚠️ partial / ❌ violation for each of the four standards, with a one-line detail per finding (file + rough line count or line number where relevant). End with a prioritized fix list, worst offenders first — a `reload` subcommand that silently skips a data manager is a data-integrity bug and ranks with data-loss-risk shallow saves, ahead of largest God classes and missing permission nodes on admin actions, which in turn rank ahead of cosmetic drift like a wrong return type.
