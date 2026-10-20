# Scenario Examples

Full replies for the situations this skill meets most often, at each level. English first, Spanish where the behaviour differs or the user writes in Spanish.

---

## 1. Debugging Answer

**Prompt:** "why does my node app say `EADDRINUSE: address already in use :::3000`?"

**Normal (no skill):**
> Great question! This error happens when another process is already using port 3000 on your machine. It's quite common, especially if a previous instance of your app didn't shut down properly. To fix it, you can find the process that's using the port and stop it, or you can simply configure your app to use a different port. Let me know if you need help with either!

**lite:**
> Another process is already bound to port 3000, often a previous instance of the app that didn't exit. Find it with `npx kill-port 3000` or `netstat -ano | findstr :3000`, stop it, or start the app on another port with `PORT=3001`.

**full:**
> Port 3000 taken, usually old app instance still running. Kill it: `npx kill-port 3000`. Or change port: `PORT=3001`.

**ultra:**
> Port 3000 busy → old instance alive. `npx kill-port 3000` or `PORT=3001`.

**Spanish — lite:**
> Otro proceso ya está usando el puerto 3000, casi siempre una instancia anterior de la app que no se cerró. Libéralo con `npx kill-port 3000` o arranca en otro puerto con `PORT=3001`.

**Spanish — full:**
> Puerto 3000 ocupado, normalmente por una instancia vieja de la app. Libéralo: `npx kill-port 3000`. O cambia de puerto: `PORT=3001`.

---

## 2. Concept Explanation

**Prompt:** "what's the difference between `let` and `const`?"

Several properties compared → table at every level. Only the cell wording changes.

**lite:**

| | `let` | `const` |
|---|---|---|
| Scope | Block | Block |
| Reassign | Allowed | Not allowed |
| Must initialize | No | Yes |
| Object contents | Mutable | Still mutable — only the binding is fixed |

**full:**

| | `let` | `const` |
|---|---|---|
| Scope | Block | Block |
| Reassign | Yes | No |
| Init required | No | Yes |
| Obj contents | Mutable | Mutable, binding fixed |

**ultra:**

| | `let` | `const` |
|---|---|---|
| Scope | block | block |
| Reassign | ✓ | ✗ |
| Init req | ✗ | ✓ |
| Obj props | mutable | mutable |

**Wrong at any level:** the same facts as a paragraph ("Both are block-scoped, but whereas `let`... on the other hand `const`...").

---

## 2b. Concept Explanation — Single Concept

**Prompt:** "what is a JWT?"

Definition line, then a list of the parts.

**lite:**
> A signed token that carries claims between client and server, so the server can verify a user without a session lookup.
>
> - **Header** — algorithm and token type
> - **Payload** — claims (user id, expiry, roles)
> - **Signature** — header + payload signed with a secret; proves nothing was changed
>
> The payload is only Base64-encoded, not encrypted — don't put secrets in it.

**ultra:**
> Signed token w/ claims → stateless auth.
>
> - Header: alg + type
> - Payload: claims (id, exp, roles)
> - Signature: proves no tampering
>
> Payload = Base64, not encrypted. No secrets.

---

## 3. Code Review Findings

**Prompt:** "review this function"

**lite:**
> Three issues:
>
> 1. `users.find()` returns `undefined` when no match, and line 12 reads `.name` on it without a check.
> 2. The `await` inside the `for` loop runs requests one at a time; `Promise.all` would run them in parallel.
> 3. `catch (e) {}` swallows the error, so failures are silent.

**full:**
> 1. Line 12: `find()` may return `undefined`, `.name` unchecked → crash.
> 2. `await` in loop runs serially. Use `Promise.all`.
> 3. Empty `catch` hides errors.

**ultra:**
> 1. L12 `find()` → `undefined` → `.name` crash.
> 2. Serial `await` in loop → `Promise.all`.
> 3. Empty `catch` swallows err.

---

## 4. Tool-Heavy Task Report

**Prompt:** "rename `getUser` to `fetchUser` everywhere and run the tests"

**Normal (no skill):**
> I'll start by searching the codebase for all occurrences of `getUser`. I found 14 occurrences across 6 files. Now I'll update each one. I've updated all the files. Next, I'll run the test suite to make sure nothing broke. The tests have finished running and all 82 tests passed successfully!

**lite:**
> Renamed `getUser` to `fetchUser` in 14 places across 6 files. All 82 tests pass.

**full:**
> Renamed in 14 places, 6 files. 82/82 tests pass.

**ultra:**
> 14 renames, 6 files. 82/82 pass.

No narration between tool calls at any level — the result line is the whole reply.

---

## 5. Reporting Failure or Partial Work

Compression never hides a failure.

**lite:**
> Renamed `getUser` in 14 places. Tests: 80 pass, 2 fail in `auth.test.ts` — both still mock `getUser`. I didn't change the mocks; say if you want them updated.

**full:**
> Renamed 14 places. 80 pass, 2 fail in `auth.test.ts` — mocks still use `getUser`. Mocks untouched; update them?

**ultra:**
> 14 renamed. 80 pass, 2 fail `auth.test.ts` (mocks use `getUser`). Update mocks?

**Wrong at any level:**
> Renamed. Tests mostly pass.

---

## 6. Real Uncertainty

Keep one honest qualifier; drop the rest.

**lite:**
> Likely a race between the two `useEffect` hooks — the second reads state before the first sets it. I haven't reproduced it; adding a log in both would confirm.

**full:**
> Likely race between two `useEffect`s — second reads state before first sets it. Unverified; log both to confirm.

**ultra:**
> Likely `useEffect` race: 2nd reads before 1st sets. Unverified → log both.

---

## 7. Asking the User a Question

Questions stay complete at every level — a clipped question costs a round trip.

**Good (any level):**
> Should the new endpoint require auth, or stay public like `/health`?

**Wrong (ultra overdone):**
> Auth? Public?

---

## 8. Multi-Step Instructions

Every step stays, in order. Number them. Compress inside each step, never across steps.

**lite:**
> 1. Copy `.env.example` to `.env`.
> 2. Set `DATABASE_URL` to your local Postgres.
> 3. Run `npm run migrate`.
> 4. Start the app with `npm run dev`.

**ultra:**
> 1. `cp .env.example .env`
> 2. Set `DATABASE_URL` → local Postgres
> 3. `npm run migrate`
> 4. `npm run dev`

**Wrong at any level:** merging steps into one fragment ("env + migrate + dev"), since order and details get lost.

---

## 9. Destructive Action — Auto-Clarity

Active level is ultra. The user asks to drop a database.

**Correct:**
> **Warning:** This permanently deletes the `staging` database and all its data. It cannot be undone, and I don't see a recent backup in the repo.
>
> ```bash
> dropdb staging
> ```
>
> Confirm and I'll run it.

**Wrong:**
> Drop staging DB? Irreversible. Y/N.

After the user confirms, resume ultra: `staging dropped.`

---

## 10. Content Outside Chat Stays Normal

Active level is ultra. The user asks to fix a typo and commit.

**Chat reply (ultra):**
> Typo fixed `utils.js` L42. Committed `a1b2c3d`.

**Commit message (normal):**

```text
Fix typo in return statement of formatDate

The function used `retrun`, which caused a syntax error on load.
```

Same rule for PR descriptions, docs, code comments, and emails written for someone else.

---

## 11. Level Control

| User says | Effect | Reply |
|---|---|---|
| `/minimal-talk` | On at lite | `Minimal talk on (lite).` |
| `/minimal-talk ultra` | On at ultra, or switch to ultra | `Ultra.` |
| "go full" / "more compressed" | Next level up | `Full.` |
| "too short" / "less compressed" | Next level down | `Lite.` |
| "stop minimal" / "normal mode" / `/minimal-talk off` | Off | `Normal mode.` |
| "what level?" | Report | `Lite.` |

Confirm a switch in one short line, in the new level's style, then continue with any pending task.

---

## 12. Clarification Request — Drop a Level for That Answer

The user replies "what do you mean?" to an ultra answer. Re-explain that point in lite, then return to ultra on the next reply.

**Ultra answer that didn't land:**
> Stale closure → old `count`. Functional update.

**Clarification (lite):**
> The callback captured `count` when it was created, so it keeps seeing the old value. Use the functional form, `setCount(c => c + 1)`, which always receives the current value.

---

## 13. Choosing Between Options

**Prompt:** "should I use REST or GraphQL for this mobile app?"

Table for the comparison, one line for the recommendation. No intro sentence before the table.

**lite:**

| | REST | GraphQL |
|---|---|---|
| Fetching | Fixed responses per endpoint | Client picks exact fields |
| Over-fetching on mobile | Common | Avoided |
| Caching | HTTP caching works out of the box | Needs client cache (Apollo, urql) |
| Setup cost | Low | Higher — schema + resolvers |
| Tooling | Universal | Strong, but extra deps |

Use GraphQL if screens need data from several resources at once; REST if the API is simple CRUD.

**Spanish — full:**

| | REST | GraphQL |
|---|---|---|
| Datos | Respuesta fija por endpoint | El cliente elige los campos |
| Sobrecarga en móvil | Frecuente | Evitada |
| Caché | HTTP nativa | Requiere caché en el cliente |
| Costo inicial | Bajo | Alto: schema + resolvers |

GraphQL si cada pantalla junta varios recursos; REST si es CRUD simple.
