# Gradle setup (project-specific — only when explicitly requested)

Maven is the default across this plugin family (see Step 0 in `SKILL.md`). Use this file only when the user explicitly asks for Gradle for a specific plugin. Don't convert an existing Maven plugin to Gradle, or vice versa, without being asked.

The dependency/repository/compiler conventions are otherwise identical to the Maven setup — same Java version, same `spigot-api` coordinates and version, same `provided`-equivalent scoping, same rule against shading `provided` dependencies.

## `build.gradle.kts` (Kotlin DSL — preferred for new Gradle plugins)

```kotlin
plugins {
    java
}

group = "com.example.plugin"
version = "1.0.0"
description = "One-line description of what the plugin does"

java {
    sourceCompatibility = JavaVersion.VERSION_11
    targetCompatibility = JavaVersion.VERSION_11
}

repositories {
    mavenCentral()
    maven("https://hub.spigotmc.org/nexus/content/repositories/snapshots/") { name = "spigot-repo" }
    // Add only if this plugin depends on VaultAPI:
    // maven("https://jitpack.io") { name = "jitpack" }
    // Add only if this plugin depends on PlaceholderAPI:
    // maven("https://repo.extendedclip.com/content/repositories/placeholderapi/") { name = "placeholderapi" }
}

dependencies {
    compileOnly("org.spigotmc:spigot-api:1.20.1-R0.1-SNAPSHOT")
    // compileOnly("com.github.MilkBowl:VaultAPI:1.7")
    // compileOnly("me.clip:placeholderapi:2.11.6")
}

tasks.processResources {
    // Equivalent of Maven's <filtering>true</filtering> — lets plugin.yml
    // reference ${version} the same way it references ${project.version} in Maven.
    filesMatching("plugin.yml") {
        expand("version" to project.version)
    }
}
```

`plugin.yml` then uses `version: '${version}'` instead of Maven's `version: '${project.version}'` — same purpose, different placeholder name because Gradle's `expand()` map key is what you name it.

## `build.gradle` (Groovy DSL — only if the user specifically prefers Groovy over Kotlin)

```groovy
plugins {
    id 'java'
}

group = 'com.example.plugin'
version = '1.0.0'
description = 'One-line description of what the plugin does'

sourceCompatibility = JavaVersion.VERSION_11
targetCompatibility = JavaVersion.VERSION_11

repositories {
    mavenCentral()
    maven { url 'https://hub.spigotmc.org/nexus/content/repositories/snapshots/' }
}

dependencies {
    compileOnly 'org.spigotmc:spigot-api:1.20.1-R0.1-SNAPSHOT'
}

processResources {
    filesMatching('plugin.yml') {
        expand version: project.version
    }
}
```

## Notes

- Use `compileOnly`, Gradle's equivalent of Maven's `<scope>provided</scope>` — the dependency is available at compile time but not bundled into the built jar.
- No shadow/shade plugin (`com.github.johnrengelman.shadow`) by default, for the same reason as Maven: Vault, PlaceholderAPI, and OnlineIdentityChecker are separate plugins already on the server's classpath. Only add it if bundling a genuinely non-Bukkit library.
- Keep the same Java 11 target and the same `spigot-api` version as the Maven convention, so plugins built with either tool stay binary-compatible with the same server versions.
- **Building follows the same "just build, don't build-and-clean" rule as Maven** (see Step 0 in `SKILL.md`): run `gradle build` or `gradle jar` (produces the jar under `build/libs/`) or `gradle compileJava` for a quick compile-only check. Never run `gradle clean` as part of a routine build, and never delete `build/` or the built jar afterward — leave it in place.
