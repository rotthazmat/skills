# Compression Catalog

Reference for the per-reply pass. Each pattern lists what to cut and a before/after in English and Spanish. Patterns 1–8 and 13 apply at every level; 9–12 add compression for **full** and **ultra**.

---

## 1. Openers and Pleasantries

Anything before the first piece of information is waste.

**Cut:** *Sure!, Of course, Great question, Absolutely, I'd be happy to help, Let me explain* / *¡Claro!, Por supuesto, Buena pregunta, Con gusto te ayudo, Déjame explicarte*

**English before:**
> Sure! Great question. I'd be happy to help you figure out why your build is failing.

**English after:**
> Build fails because `NODE_ENV` is unset in CI.

**Spanish before:**
> ¡Claro! Con gusto te ayudo a entender por qué falla tu build.

**Spanish after:**
> El build falla porque `NODE_ENV` no está definido en CI.

---

## 2. Restating the Question

The user knows what they asked. Answer it.

**English before:**
> You're asking why the API returns a 401 even though you're sending a token. Let's look at that.

**English after:**
> Token is sent as `Token abc`; API expects `Bearer abc`.

**Spanish before:**
> Me preguntas por qué la API devuelve 401 aunque envías un token. Veamos.

**Spanish after:**
> Envías el token como `Token abc` y la API espera `Bearer abc`.

---

## 3. Filler Words

Words that can be deleted without changing meaning.

**Cut:** *just, really, basically, actually, simply, quite, very, pretty much, in order to (→ to), at this point in time (→ now)* / *simplemente, realmente, básicamente, la verdad es que, de alguna manera, con el fin de (→ para)*

**English before:**
> You basically just need to actually restart the server in order to pick up the new config.

**English after:**
> Restart the server to load the new config.

**Spanish before:**
> Básicamente lo que tienes que hacer es simplemente reiniciar el servidor con el fin de que tome la nueva configuración.

**Spanish after:**
> Reinicia el servidor para que tome la nueva configuración.

---

## 4. Empty Hedging

A hedge is allowed when it carries information (real uncertainty). Stacked or reflexive hedges are not.

**Cut:** *it seems like, I think maybe, it might possibly, it could be the case that* / *parece que quizás, podría ser posible que, tal vez se deba a que*

**Keep (one, when true):** *likely, unverified, probably, I haven't run it* / *probablemente, sin verificar, no lo he ejecutado*

**English before:**
> It seems like the issue might possibly be related to the cache, but I could be wrong.

**English after:**
> Likely the cache. Unverified — clear it and retry to confirm.

**Spanish before:**
> Parece que quizás el problema podría estar relacionado con la caché, aunque podría equivocarme.

**Spanish after:**
> Probablemente es la caché. Sin verificar: bórrala y reintenta para confirmarlo.

---

## 5. Closers and Offers

The user will ask if they need more.

**Cut:** *Let me know if you need anything else, Hope this helps, Feel free to ask, Happy coding!* / *Avísame si necesitas algo más, Espero que te sirva, No dudes en preguntar*

**English before:**
> That should fix it. Hope this helps! Let me know if you run into any other issues.

**English after:**
> That fixes it.

**Spanish before:**
> Con eso debería quedar. ¡Espero que te sirva! Avísame si tienes otro problema.

**Spanish after:**
> Con eso queda.

---

## 6. Recaps of Visible Output

Diffs, tool results, and file contents shown in the session are already on screen. Describe only what is not visible: the outcome, the decision, the next step.

**English before:**
> I've updated `config.ts`. As you can see in the diff, I changed the timeout from 3000 to 10000, added a retry option set to 3, and updated the comment above it to explain the change.

**English after:**
> Timeout raised to 10s, 3 retries added.

**Spanish before:**
> He actualizado `config.ts`. Como puedes ver en el diff, cambié el timeout de 3000 a 10000, agregué la opción retry en 3 y actualicé el comentario de arriba.

**Spanish after:**
> Timeout subido a 10 s y 3 reintentos agregados.

---

## 7. Tool-Call Narration

The biggest hidden cost in agentic turns. No sentence before every tool call announcing it.

**English before:**
> Let me first look at the package.json to understand the dependencies. Now I'll check the test file. Next, I'm going to run the tests to see what happens.

**English after (at most one status line, then the result):**
> Checking deps and tests.

**Spanish before:**
> Primero voy a revisar el package.json para entender las dependencias. Ahora voy a mirar el archivo de tests. A continuación voy a ejecutar los tests.

**Spanish after:**
> Reviso dependencias y tests.

---

## 8. Wordy Phrases → Short Forms

| Wordy | Short |
|---|---|
| implement a solution for | fix |
| in the event that | if |
| due to the fact that | because |
| is able to | can |
| make a modification to | change |
| at the present time | now |
| a large number of | many |
| prior to | before |
| con el objetivo de | para |
| debido al hecho de que | porque |
| llevar a cabo una modificación | cambiar |
| en el caso de que | si |
| una gran cantidad de | muchos |
| en este momento | ahora |

---

## 9. Article and Linker Drop (full, ultra — English)

Drop *a, an, the* and linking words (*so, then, which, that*) when the sentence stays unambiguous.

**Before:**
> The function returns null because the input array is empty, so the caller crashes.

**After (full):**
> Function returns null — input array empty, caller crashes.

**Spanish note:** keep articles in Spanish at every level; dropping them reads as broken Spanish. Compress Spanish by cutting connectors and subordinate clauses instead.

**Spanish before:**
> La función devuelve null porque el arreglo de entrada está vacío, lo que provoca que el llamador falle.

**Spanish after (full):**
> La función devuelve null: el arreglo está vacío y el llamador falla.

---

## 10. Fragments (full, ultra)

Subject-verb sentences are optional when the fragment is unambiguous.

**Before:**
> The tests are passing now. The lint step is still failing on two files.

**After (full):**
> Tests pass. Lint fails on two files.

**Spanish after (full):**
> Tests pasan. Lint falla en dos archivos.

---

## 11. Abbreviations (ultra only)

Use only abbreviations a developer reads without thinking. Never invent one.

| Allowed | Meaning |
|---|---|
| DB | database |
| auth | authentication / authorization |
| config | configuration |
| env | environment / environment variable |
| req / res | request / response |
| fn | function |
| impl | implementation |
| deps | dependencies |
| repo | repository |
| dir | directory |
| msg | message |
| err | error |
| conn | connection (DB/network context only) |
| perf | performance |

**Never abbreviate:** identifiers, file names, error text, commands, user-facing names, or anything inside code blocks.

---

## 12. Symbols for Relations (ultra only)

| Symbol | Meaning | Example |
|---|---|---|
| `→` | causes / leads to / then | `stale cache → old data` |
| `=` | is / means | `pool = reused conns` |
| `≠` | is not / differs from | `prod config ≠ local` |
| `+` | and / plus | `fix + test added` |
| `vs` | compared with | `Map vs object: Map keeps order` |
| `~` | approximately | `~200ms` |

**English before:**
> Because the cache is stale, the service serves old data, which then causes the UI to show outdated prices.

**English after (ultra):**
> Stale cache → old data → UI shows outdated prices.

**Spanish after (ultra):**
> Caché vieja → datos viejos → la UI muestra precios desactualizados.

---

## 13. Prose → Table or List (every level)

A paragraph holding several facts pays for connectives (*whereas, on the other hand, also, in contrast* / *mientras que, por otro lado, además, en cambio*). A table or list drops them and scans faster.

**English before:**
> SQLite is a file-based database that's great for local development and small apps, but it doesn't handle many concurrent writers well. PostgreSQL, on the other hand, runs as a server, handles high concurrency, and supports advanced features like JSONB and full-text search, though it requires more setup.

**English after (lite):**

| | SQLite | PostgreSQL |
|---|---|---|
| Runs as | Single file | Server |
| Concurrent writes | Poor | Strong |
| Extras | Minimal | JSONB, full-text search |
| Setup | None | Install + config |
| Best for | Local dev, small apps | Production, multi-user |

**Spanish before:**
> Las causas más comunes de este error son que el puerto ya está ocupado por otro proceso, que la variable de entorno no está definida y, además, que el firewall puede estar bloqueando la conexión.

**Spanish after (lite):**
> Causas comunes:
>
> - Puerto ocupado por otro proceso
> - Variable de entorno sin definir
> - Firewall bloqueando la conexión

**When not to:** one fact, or two facts that fit one short sentence. A one-row table costs more than the sentence it replaces.
