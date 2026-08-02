---
name: mc-plugins
description: Build, update, review, or audit a Minecraft server plugin (Spigot/Bukkit/Paper-family Java plugin) to this plugin family's conventions — Maven project setup with git init, OnlineIdentityChecker (OIC) player UUID resolution, YAML config/data files whose comments survive runtime saves, SOLID command/service architecture, and command/permission/help-text registration. Use this skill whenever the user wants to make, scaffold, add to, fix, polish, review, or audit a Minecraft/MC/Bukkit/Spigot plugin — including casual phrasing like "create a new plugin", "add a command to this plugin", "update this MC plugin", or "check this plugin for issues" — even if they don't say "Spigot" or "Bukkit" explicitly.
user-invocable: true
argument-hint: "e.g. new plugin name, or path to an existing plugin to audit"
---

Conventions for a family of Spigot/Bukkit Minecraft plugins that share four standards: UUID resolution through an optional OnlineIdentityChecker (OIC) dependency, YAML files whose comments survive `saveToString()`, a SOLID package/command layout with no God classes, and consistent command/permission registration.

## When to apply this skill

Apply immediately and fully whenever the user:

- Says anything about making, building, scaffolding, or starting a new Minecraft plugin, MC plugin, server plugin, Bukkit plugin, or Spigot plugin — regardless of which of those exact words they use
- Asks to add, change, fix, extend, or remove a command, permission, listener, or persisted data file in an existing plugin in this style
- Asks to review, audit, check, polish, or "clean up" a Minecraft/Bukkit/Spigot plugin for standards compliance
- Writes any code that resolves a `Player` to a UUID for storage purposes
- Writes any code that saves a `FileConfiguration` to disk at runtime
- Registers a command executor, declares a permission node, or writes a `sendHelp()`-style help method
- Is about to build/release a plugin and needs to decide the version bump
- Mentions the name of any plugin in this ecosystem (e.g. bank-plugin, TimeRestrictions, online-identity-checker, or any plugin folder under the same workspace) in the context of changing or reviewing it

This applies even when the request is short and doesn't name "Spigot," "Bukkit," or this skill directly — e.g. "make me a new plugin that tracks X" or "add a leaderboard command to this plugin" are enough on their own. Do not wait to be asked to apply these rules, and do not proceed from memory of this file's contents without formally invoking it first — enforce them proactively on every matching task, including polish passes on code the user didn't flag as broken.

---

## Reviewing / auditing an existing plugin

When the task is to review, audit, check, or polish an existing plugin, **apply all four standards below in full**, not just the ones obviously broken:

- Restructure command handling to the per-subcommand pattern (Step 3) even if the plugin currently has one big command class.
- Verify every persisted YAML file uses the header-survival pattern (Step 2), not just the ones that already have some comments.
- Verify UUID resolution (Step 1) is present wherever per-player data is persisted — and correctly *absent* where it isn't needed.
- Verify every command and subcommand has a dedicated permission node, declared in `plugin.yml` *and* checked in code (Step 4) — missing nodes on `save`/`reload`-style admin subcommands are the single most common gap found in past audits.
- Verify `save` and `reload` subcommands exist at all (they're mandatory, not optional — Step 4), and specifically verify `reload` calls `.reload()` on *every* manager the plugin constructs, not just the config manager — this exact bug (reload silently skipping data managers) has been caught in practice.

Load `references/audit-checklist.md` for the full per-file checklist and worked good/bad examples before reporting findings.

---

## Step 0 — Project setup (Maven, default)

Every plugin in this ecosystem is a standalone Maven module. Use `assets/pom.xml` as the starting template, filling in `groupId`, `artifactId`, `version`, `name`, `description`, and any extra `provided` dependencies the plugin needs beyond `spigot-api`.

Fixed conventions — apply these to every new plugin without asking:

- **Java 11** (`maven.compiler.source`/`target` = `11`).
- `org.spigotmc:spigot-api:1.20.1-R0.1-SNAPSHOT`, scope `provided`, resolved from the `spigot-repo` repository (`https://hub.spigotmc.org/nexus/content/repositories/snapshots/`).
- `packaging` = `jar`.
- A `<resources>` block with `filtering` set to `true` on `src/main/resources` — required so `plugin.yml`'s `version: '${project.version}'` resolves from the POM instead of the version being hardcoded in two places.
- **No shade/shadow plugin by default.** Every third-party integration (Vault, PlaceholderAPI, OnlineIdentityChecker) is `provided` scope, because those are separate plugins already on the server's classpath at runtime. Only add `maven-shade-plugin` if the plugin genuinely needs to bundle a library that is *not* itself a Bukkit plugin — confirm that need before adding it.
- Add a repository entry only for the specific dependency that requires it (e.g. `jitpack.io` for VaultAPI, `https://repo.extendedclip.com/content/repositories/placeholderapi/` for PlaceholderAPI). Don't add repositories speculatively for integrations the plugin doesn't use.

`plugin.yml` conventions that follow from the POM setup:
- `main:` is the fully-qualified main class.
- `api-version:` matches the Spigot API minor version (`1.20`).
- `version: '${project.version}'` (quoted) — filled in by Maven resource filtering, never hand-written.
- `depend:` lists hard dependencies the plugin cannot run without (e.g. `[Vault]`); `softdepend:` lists optional integrations, including `OnlineIdentityChecker` (Step 1) and `PlaceholderAPI`.

### Git (universal — every new plugin)

Every plugin in this ecosystem is its own standalone local git repository — not a subfolder of one shared monorepo, and with no remote configured by default. When scaffolding a brand-new plugin:

1. `git init` in the plugin's root directory.
2. Add `.gitignore` from `assets/gitignore` (Maven `target/`, IDE files, OS files) before staging anything.

This is scaffolding setup only — it says nothing about whether or when to actually run `git commit`; that's a separate decision governed by whatever the user has told you about commit policy in this workspace, not something this skill decides.

### Gradle — project-specific, only when the user explicitly asks for it

Maven is the default and the standard across this plugin family. If the user explicitly requests Gradle for a given plugin, load `references/gradle-setup.md` for the equivalent `build.gradle(.kts)` setup — don't switch build tools on your own judgment, and don't mix the two within one plugin.

### Version bumping (universal)

Before building/releasing, decide the semver bump deliberately — don't default to a patch bump out of habit:

- **MINOR** (`x.Y.0`, reset patch to 0) — any new permission node, new subcommand, `plugin.yml` restructuring, or replacing a raw `sender.isOp()` check with a real permission node.
- **PATCH** (`x.y.Z`, increment only the last number) — small fixes with no permission/command surface change: help-text wording, display-only corrections, cosmetic fixes.
- When genuinely unsure which bucket a change falls into, default to **MINOR** — it's the safer overcorrection.

### Building (universal)

Build with `mvn package` (produces the jar in `target/`) when the jar itself is needed, or `mvn compile` for a quick compile-only check when just verifying the code builds. Just build — never build-and-clean:

- Don't run `mvn clean` as part of a routine build.
- Never delete `target/` or the built jar afterward, even to tidy up the working directory. Leave the build output in place — the user needs the jar available (e.g. to copy onto a test server) without forcing an unnecessary rebuild.

---

## Step 1 — OIC UUID resolution

**First decide if this plugin needs it at all.** OIC integration is *conditional*, not universal:

- **Required** — the plugin persists any data keyed by player (balances, ownership, settings, flags, cooldowns, history) to a YAML file that outlives the session.
- **Not needed** — the plugin has only global config, or per-player state that is purely in-memory and session-scoped (e.g. a double-click timer, a temporary GUI cursor). Don't add a `UUIDHelper` or a `softdepend` entry the plugin has no use for.

When required, add a `UUIDHelper` class (usually `util/UUIDHelper.java`) with exactly this shape — use `assets/UUIDHelper.java` as the starting template, adapting only the package name and log prefix:

- `static void initialize()` — looks up `Bukkit.getPluginManager().getPlugin("OnlineIdentityChecker")`, checks `isEnabled()`, and reflectively caches its `getUUIDFromName(String)` method via `getClass().getMethod(...)`. Logs whether the integration is active.
- `static String getRealUUID(Player player)` — invokes the cached reflection method when available and returns its result; otherwise falls back to `player.getUniqueId().toString()`.

**The return type is `String`, always** — never `UUID`. See Gotchas.

Rules:
- `plugin.yml` declares `softdepend: [OnlineIdentityChecker]` (append to any existing soft-deps like `Vault` or `LuckPerms` — don't replace them).
- Code must never use `player.getUniqueId()` or `player.getName()` directly as a YAML storage key. Always go through `UUIDHelper.getRealUUID()`. Raw calls are fine only for in-memory-only maps, display strings, or permission-node lookups — never for anything written to a persisted file.
- Resolving an **offline** player (e.g. a command target who isn't online) should still go through OIC-aware lookup logic in the helper — extend `UUIDHelper` with a `getUUIDFromName(String)` overload rather than duplicating raw `Bukkit.getOfflinePlayer(name).getUniqueId()` fallback code inside command handlers.

---

## Step 2 — YAML comment headers, and the save()/reload() pair every manager needs

Bukkit's `YamlConfiguration.saveToString()` strips all comments on every save. Any YAML file that needs a documented structure (anything other than `plugin.yml`, which Bukkit never rewrites) needs this pattern:

```java
private static final String PLAYERS_HEADER =
    "# players.yml - <Plugin> Player Data\n" +
    "#\n" +
    "# Structure:\n" +
    "# players:\n" +
    "#   <uuid>:\n" +
    "#     balance: <double>   # one line per field, explain type + meaning\n" +
    "#\n";

private void writeWithHeader(File file, FileConfiguration config, String header) {
    String yaml = config.saveToString().replaceAll("(?m)^#[^\\n]*\\n?", "");
    try (FileWriter fw = new FileWriter(file)) {
        fw.write(header + yaml);
    } catch (IOException e) {
        plugin.getLogger().severe("Could not save " + file.getName() + ": " + e.getMessage());
    }
}
```

Rules:
- Always call `config.saveToString()` first and strip residual `#` lines with the regex above, *then* prepend the header. Never write the header string alone and skip the merge — that silently discards every real value in the file (see Anti-patterns).
- Use plain `java.io.FileWriter`. Do not use Paper-only file APIs — these plugins target Spigot compatibility.
- Don't rely on inline YAML comments (`key: value # comment`) for anything that must survive a save; they get stripped along with the rest. Document structure only in the header block.
- One header constant per YAML file, named `<FILE>_HEADER`, defined next to the manager class that owns that file's persistence.
- `config.yml`'s header should document more than just `Structure:` — mirror bank-plugin's `config.yml` header by also listing a `Commands:` section (every command the plugin registers, with a one-line description) and, if the plugin has a PAPI expansion, a `Placeholders:` section (every placeholder it exposes). An admin editing the file by hand should get full context from the header alone, without needing external docs.

### Every manager needs `reload()`, not just `save()` (universal)

`save()` is the memory→disk direction. Every manager that persists YAML data also needs the disk→memory direction: a public `reload()` that clears the current in-memory state and re-runs the same loading logic used in the constructor. Structure it so both share one private method:

```java
public DataManager(Plugin plugin) {
    this.plugin = plugin;
    this.playersFile = new File(plugin.getDataFolder(), "players.yml");
    load();
}

private void load() {
    plugin.getDataFolder().mkdirs();
    if (!playersFile.exists()) plugin.saveResource("players.yml", false);
    playersConfig = YamlConfiguration.loadConfiguration(playersFile);

    balances.clear();   // clear before repopulating, or a reload() after an external edit
    ConfigurationSection section = playersConfig.getConfigurationSection("players");
    if (section != null) {
        for (String uuid : section.getKeys(false)) {
            balances.put(uuid, section.getDouble(uuid + ".balance", 0.0));
        }
    }
}

/** Re-reads the YAML file from disk, replacing all in-memory state — the inverse of save(). */
public void reload() {
    load();
}
```

This matters because the plugin's `/‹command› reload` subcommand (Step 4) is required to call `.reload()` on *every* manager, not just the config manager — a manager with no `reload()` method is a manager that subcommand silently fails to reload.

See `assets/DataManager-header-pattern.java` for a complete manager class using this pattern for two related files.

---

## Step 3 — SOLID structure, no God classes

### Package layout (universal)

```
<plugin>/
  <MainClass>.java        ← onEnable/onDisable only: wire managers, listeners, commands. No business logic.
  command/                ← one class per command, or one handler class per subcommand
  manager/  (or config/ + service/)   ← config loading, YAML persistence, in-memory caches
  model/                  ← plain data classes
  listener/               ← Bukkit event listeners
  util/                   ← UUIDHelper and other stateless helpers
  gui/                    ← inventory-based UIs, if any
  task/                   ← BukkitRunnable/scheduled tasks, if any
  expansion/              ← PlaceholderAPI expansions, if any
```

For plugins large enough to need it, split further into `repositories/` + `repositories/impl/` and `services/` + `services/impl/` — full layered architecture with interfaces separated from implementations.

### Command dispatch (universal — for any command with 3+ subcommands)

Prefer one class per subcommand implementing a shared interface, dispatched by a single router class:

```java
interface SubcommandHandler {
    void execute(CommandSender sender, String[] args);
}

class SetFlagHandler implements SubcommandHandler { /* one subcommand's logic only */ }
class RemoveFlagHandler implements SubcommandHandler { /* ... */ }

class CommandDispatcher {
    private final Map<String, SubcommandHandler> handlers = Map.of(
        "setflag", new SetFlagHandler(...),
        "removeflag", new RemoveFlagHandler(...)
    );
    // onCommand looks up handlers.get(args[0]) and delegates
}
```

**God-class threshold:** a single command-parsing class that handles many subcommands inline, mixing argument parsing with business logic, and grows past roughly **400–500 lines**, is a God class — split it using the pattern above. In practice this shows up as one file handling 15–25+ subcommands with ad-hoc inline argument parsing (e.g. hand-rolled quoted-string splitting) instead of delegating; such files have been observed growing past 800 lines. Splitting the command layer doesn't require touching business logic that's already correctly delegated to a manager/service — check that first, since the fix is often purely mechanical.

### Main class (universal)

The main plugin class's `onEnable()` should read as a wiring list — construct managers, register listeners, register commands — and contain no business logic itself. If it's under ~200 lines and does nothing but construction/registration, that's the target shape.

### `onEnable()` ordering (universal)

Wire things in this order — later steps depend on earlier ones:

1. Check hard dependencies (e.g. Vault's `Economy` service); if a required one is missing, log a severe error and call `getServer().getPluginManager().disablePlugin(this)`, then `return` immediately.
2. `UUIDHelper.initialize()` (Step 1), so it's ready before any manager loads player data.
3. Initialize config/data files with their headers (Step 2) — create the resource if missing, then load it.
4. Construct managers/services, passing already-loaded config values into their constructors.
5. Construct listeners/GUIs and register them: `getServer().getPluginManager().registerEvents(listener, this)`.
6. Register commands (see Step 4 below).
7. Start any scheduled tasks (`BukkitRunnable#runTaskTimer`), keeping the returned `BukkitTask` so `onDisable()` can cancel it.
8. Register a PlaceholderAPI expansion **only if present**: `if (getServer().getPluginManager().getPlugin("PlaceholderAPI") != null) { new MyExpansion(...).register(); }` — this is a soft integration, never a hard dependency.
9. Log an enabled message including the plugin version and a one-line summary of key loaded config (interval, rate limit, etc.) — makes misconfiguration visible in the console immediately.

`onDisable()` mirrors it in reverse only where needed: cancel scheduled tasks, then log a disabled message. Data is normally already persisted on each mutation via the manager layer (Step 2), so `onDisable()` doesn't need to force a final save unless a manager intentionally batches writes.

---

## Step 4 — Commands, permissions, and help visibility

### `plugin.yml` command + permission declarations (universal)

Every command **and every subcommand** gets a dedicated permission node — declared in `plugin.yml` and checked in code with `sender.hasPermission(node)`. A subcommand with no permission node is a violation even if it's op-only in practice; the most commonly missed nodes in past audits were unglamorous ones like `save` and `reload`. See `assets/plugin.yml` for a full worked example.

### `save` and `reload` are mandatory subcommands on every plugin (universal)

Every plugin scaffolded with this skill gets a `save` and a `reload` subcommand — not an optional nicety, and not something to add only if the plugin "seems to need it." Put them on the main command, or on the admin command if the plugin splits admin subcommands out (Step 4's large-admin-surface rule above); either way both get their own permission node, admin-gated (`default: op`), grouped under the admin parent.

Exact semantics — get this right, it's a real source of bugs:
- **`save`** flushes current in-memory state to disk: call `.save()` on *every* manager that holds persisted YAML data — the config manager **and** every data manager.
- **`reload`** re-reads all persisted YAML files from disk back into memory: call `.reload()` on *every* manager — the config manager **and** every data manager (see Step 2's `reload()` pattern).

The failure mode to avoid: wiring `reload` to call only `configManager.reload()` because "config" is the first manager that comes to mind, while data managers (e.g. a `PlayerDataManager`, a `ServerDataManager`) are left out because they never had a `reload()` method written for them in the first place. The command will compile, run, and print a success message, while silently reloading nothing but an unrelated config value. Before wiring the `reload` subcommand, enumerate every manager the plugin constructed in `onEnable()` and confirm each one is called.

Naming and defaults:
- Nodes are lowercase, dot-namespaced: `<pluginname>.<subcommand>`, or `<pluginname>.<group>.<subcommand>` for a nested feature (e.g. `bank.admin.withdraw`).
- `default: true` for actions any player should be able to run; `default: op` for admin-only actions.
- Group related admin subcommands under one parent node with a `children` map, so granting the parent grants all of them:
  ```yaml
  permissions:
    myplugin.admin:
      description: All admin subcommands
      default: op
      children:
        myplugin.admin.save: true
        myplugin.admin.reload: true
        myplugin.papi: true       # dedicated PAPI-doc-visibility node — see below
    myplugin.*:
      description: All MyPlugin permissions
      default: op
      children:
        myplugin.help: true
        myplugin.use: true
        myplugin.admin: true
  ```
- Never gate a subcommand with a raw `sender.isOp()` check instead of a permission node — it can't be granted piecemeal through a permissions plugin and is a MINOR-bump-worthy fix when found (see Step 0's version rule).
- For a plugin with a large, clearly separate admin surface (e.g. a dozen+ admin subcommands), split them into their own top-level command (`/plugin` for players, `/pluginadmin` for admins) rather than growing one command's argument list — this is project-specific: only do it when the admin surface is genuinely large, not for a plugin with two or three admin subcommands.

### `help` defaults to `true` even in an all-admin command (universal)

The top-level `help` subcommand/permission (e.g. `myplugin.help`) should default to `true` almost always — **even when every other subcommand in that same command is admin-only (`op`)**. Don't sweep `help` into the admin parent's `children` map just because the rest of the command is op-gated; keep it a standalone permission with its own `default: true`, and let `myplugin.*`'s children list include it alongside (not inside) the admin group. The reason: a regular player should still be able to run `/myplugin help` and see whatever subset of the menu applies to them (which may be nothing beyond "you don't have access to this command's actions"), rather than getting Bukkit's blanket "no permission" message for the command itself.

`sendHelp()` must reflect this by filtering line-by-line, mirroring bank-plugin's `BankCommand.sendHelp()` exactly:
1. Print the header banner unconditionally.
2. Print the `/<command> help` usage line unconditionally, directly below the header — not gated on anything.
3. If the sender has any player-facing permission for this command, print a "Player Commands" section, checking each line's own permission individually.
4. If the sender has the admin parent permission, print a "Server Admin Commands" section, checking each line's own permission individually.
5. If the plugin has a PlaceholderAPI expansion, print a "PAPI Placeholders" section *last*, gated on the dedicated `.papi` permission (see below) — after the admin section, not folded into it.

Getting this wrong looks like: defaulting `help` to `op` "because the rest of the command is admin-only," or printing the entire help text unconditionally without per-line permission checks. Both were real mistakes caught only after implementation — treat this as a required check on every `sendHelp()`-equivalent method, not just a stylistic preference.

### PAPI placeholder visibility in help output (universal, when the plugin registers a PlaceholderAPI expansion)

If a plugin's `sendHelp()` (or equivalent) documents PlaceholderAPI placeholders, that section must be gated on a **dedicated `myplugin.papi` permission** — declared in `plugin.yml` as its own node, `default: op`, and listed as a child of `myplugin.admin` — never shown unconditionally, never gated only on a player-level permission, and never gated by directly checking `myplugin.admin` itself:

```java
if (sender.hasPermission("myplugin.papi")) {
    sender.sendMessage("--- PAPI Placeholders ---");
    sender.sendMessage("%myplugin_balance% - player's current balance");
}
```

Using a separate node rather than checking `myplugin.admin` directly gives finer control — an admin's PAPI-doc visibility can be revoked without touching their other admin permissions — and matches the reference implementation (bank-plugin's `bank.papi`, a genuine child permission of `bank.admin`, not a re-check of the admin node itself).

Registering the expansion itself still only depends on PlaceholderAPI being present (Step 0/`onEnable` ordering) — that's independent from who can *see the documentation* for it.

---

## Gotchas

- **Resource filtering must be on in `pom.xml`, or `plugin.yml`'s `${project.version}` won't resolve** — it will literally read the string `${project.version}` at runtime instead of the POM version.
- **`UUIDHelper.getRealUUID()` must return `String`, never `UUID`.** Returning `UUID` is a real drift that has been observed in practice — don't copy it even if you see it in an existing file; normalize to `String` when touching that code.
- **`initialize()` must check `plugin.isEnabled()`**, not just that `getPlugin(...)` returned non-null — a disabled-but-installed OIC plugin must fall through to the legacy UUID method, not be treated as available.
- **`softdepend`, never `depend`.** OIC integration is optional-at-runtime; a hard `depend` would prevent the plugin from loading at all on servers without OIC installed.
- **Comments only survive via the header-constant + `writeWithHeader` pattern.** Any other approach (inline comments, writing the header without merging `saveToString()`) loses data or loses documentation on the next save.
- **A plugin with no persisted per-player data should not get a `UUIDHelper`.** Forcing OIC integration into a plugin that doesn't need it is itself a standards violation — it adds an unused dependency and misleads future maintainers into thinking UUID resolution matters here.
- **In-memory-only maps keyed by `player.getUniqueId()` are fine.** The rule is about persisted YAML storage keys, not every use of a player's UUID in the JVM.
- **`save`/`reload` subcommands are the most commonly missing permission nodes.** They feel like internal/admin plumbing, so they get declared as commands but skipped when writing the `permissions:` block — always pair the two.
- **`reload` must call `.reload()` on every manager, not just the config manager.** This is a real bug caught in practice, not hypothetical: a plugin's `reload` subcommand called `configManager.reload()` only, while its data managers (`players.yml`, `general.yml`) had no `reload()` method at all — the command ran, printed success, and reloaded nothing but an unrelated config value. Before wiring `reload`, list every manager constructed in `onEnable()` and confirm each is called.
- **PAPI expansion registration and PAPI help-text visibility are two separate gates.** The expansion registers whenever PlaceholderAPI is present; the *documentation* of its placeholders in `sendHelp()` is gated on its own dedicated `myplugin.papi` permission regardless. Don't conflate "PAPI is installed" with "this player should see placeholder docs," and don't gate the docs by directly checking `myplugin.admin` instead of the dedicated node.
- **A permission checked via `hasPermission()` in code but never declared anywhere in `plugin.yml` is a real, easy-to-miss bug** — distinct from a command with no permission node. Help-menu section gates like PAPI visibility aren't tied to any `commands:` entry, so it's easy to add a check in code and forget the declaration entirely. This has been found in an actual sibling plugin's help command (a PAPI-visibility check with no matching `plugin.yml` entry at all) — grep for every `hasPermission("...")` string literal and confirm each has a matching declaration.
- **`help` defaults to `true` even when every other subcommand in that command is `op`.** Sweeping it into the admin permission's `children` map because "the rest of the command is admin-only" is a real mistake caught in practice — it blocks regular players from seeing even a filtered help menu.
- **Scaffolding a new plugin includes `git init` + `.gitignore`, not just the Maven files.** Every sibling plugin in this ecosystem is its own git repo from the start; forgetting this step was a real gap found in practice, not a hypothetical one.
- **Never delete `target/` or the built jar after building.** Just build — don't build-and-clean. The jar needs to stay available afterward (e.g. to copy onto a test server); tidying it up as a courtesy is an unwanted side effect, not a nicety.
- **Tab completion isn't used anywhere in this plugin family today.** Implementing a `TabCompleter` is a genuine quality improvement for a new plugin, but don't present it as an existing convention to match — it would be a net-new addition, not a fix to bring something back in line.

---

## Anti-patterns to avoid

| Anti-pattern | Why it's wrong |
|---|---|
| `getRealUUID()` returns `UUID` instead of `String` | Breaks the established contract other plugins in this ecosystem rely on; forces callers to `.toString()` inconsistently |
| Save method writes the header constant directly without calling `config.saveToString()` first | Silently discards every real key/value in the file the next time it saves |
| One command class with 15+ subcommands and inline argument parsing | Impossible to test or modify safely; violates SRP; the fix (per-subcommand handler + dispatcher) is well-established in this ecosystem |
| Raw `player.getUniqueId()`/`getName()` used as a YAML map key | Bypasses OIC resolution entirely, defeating the point of the integration |
| Adding `UUIDHelper`/`softdepend: [OnlineIdentityChecker]` to a plugin with no persisted per-player data | Unused dependency; signals a UUID-resolution need that doesn't exist |
| Duplicating offline-player UUID fallback logic inside a command handler instead of extending `UUIDHelper` | Same resolution logic ends up defined twice and can drift out of sync |
| Business logic inside the main plugin class's `onEnable`/command listener | Prevents reuse and testing of the logic outside the Bukkit lifecycle |
| Hardcoding the version in both `pom.xml` and `plugin.yml` | The two drift apart; use `version: '${project.version}'` with resource filtering instead |
| Adding `maven-shade-plugin` and bundling `provided`-scope dependencies (Vault, PlaceholderAPI, OnlineIdentityChecker) | Bloats the jar and risks classloading conflicts with the real plugin already installed on the server |
| Switching to Gradle without the user asking for it | Breaks consistency with the rest of the plugin family, which is Maven-only by default |
| A command/subcommand declared in `plugin.yml` with no matching permission node | Found repeatedly in past audits, especially on `save`/`reload`; leaves the action unrestricted or inconsistently gated |
| A `hasPermission("...")` check in code with no matching declaration anywhere in `plugin.yml` | Distinct from the row above — this isn't tied to a `commands:` entry (e.g. a PAPI-visibility check in a help method), so it's easy to add in code and forget to declare; found in a real sibling plugin |
| A plugin scaffolded without `save`/`reload` subcommands at all | Every plugin in this family needs both — it's not optional plumbing to add only "if the plugin seems to need it" |
| `reload` subcommand calls `configManager.reload()` but not `.reload()` on the plugin's data managers | Compiles and reports success while silently reloading nothing but an unrelated config value; a real bug caught in practice |
| Gating a subcommand with `sender.isOp()` instead of a permission node | Can't be granted through a permissions plugin to non-op staff; also can't be revoked from an op without stripping full op |
| PAPI placeholder docs shown unconditionally, gated only on a player-level permission, or gated by directly checking `myplugin.admin` in `sendHelp()` | Exposes admin-facing scoreboard/TAB configuration detail to every player, or over-couples doc visibility to every other admin permission; use a dedicated `myplugin.papi` child node |
| Registering PlaceholderAPI as a hard `depend` instead of checking `getPlugin("PlaceholderAPI") != null` | Forces the plugin to fail loading on servers without PAPI, even though the integration is optional |
| Defaulting to a patch version bump without checking whether the change added a permission/command | Under-signals a MINOR-worthy change (new node, new subcommand, `isOp()` replacement) to anyone reading version history |
| Defaulting `help` to `op` because the rest of the command is admin-only | Blocks regular players from a permission-filtered help menu; `help` stays `default: true` and standalone, never nested under the admin parent |
| Scaffolding a new plugin's Maven files without `git init` + `.gitignore` | Leaves the plugin without version control from the start, inconsistent with every sibling plugin in the ecosystem |
| Deleting `target/` or the built jar after `mvn package`/`mvn compile` | Forces an unnecessary rebuild next time the jar is needed; just build, don't build-and-clean |

---

## Resources

- **`assets/pom.xml`** — Maven POM template with the standard Java 11 / spigot-api / resource-filtering setup. Use when scaffolding a new plugin's project file (Step 0).
- **`assets/gitignore`** — standard `.gitignore` (Maven `target/`, IDE files, OS files). Use when running `git init` for a new plugin (Step 0) — copy to `.gitignore` in the plugin root.
- **`assets/plugin.yml`** — full worked example of command + permission declarations, including the parent/`children`/wildcard pattern and the standalone-`help`-defaults-`true` rule. Use when declaring commands and permissions (Step 4) for a new or existing plugin.
- **`assets/UUIDHelper.java`** — ready-to-adapt UUID resolution helper. Use as the starting point whenever Step 1 applies to a new or existing plugin.
- **`assets/DataManager-header-pattern.java`** — complete manager class showing the header-constant + `writeWithHeader` pattern, plus the mandatory `reload()` method mirroring `save()`. Use when implementing or fixing YAML persistence.
- **`references/audit-checklist.md`** — full compliance checklist plus worked good/bad examples for all four standards. Load when reviewing, auditing, or polishing an existing plugin.
- **`references/gradle-setup.md`** — Gradle equivalent of Step 0. Load only when the user explicitly asks for Gradle instead of Maven.
- **`evals/evals.json`** — test cases covering scaffolding, review, and the conditional-OIC edge case.
