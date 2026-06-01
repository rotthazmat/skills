---
name: research
description: Metodología de investigación profunda y multidimensional. Usar cuando se pide investigar, analizar, estudiar, comprender o complementar información sobre un tema complejo — en cualquier dominio (histórico, técnico, social, económico, etc.).
user-invocable: true
argument-hint: "e.g. desigualdad económica en América Latina"
---

Skill de investigación rigurosa y sistémica. Aplica pensamiento sistémico, triangulación de fuentes y síntesis crítica para producir análisis coherentes y multidimensionales — no resúmenes planos.

## Cuándo aplicar este skill

Aplicar inmediatamente cuando el usuario:

- Pide investigar, estudiar o analizar un tema
- Hace una pregunta compleja que requiere más de una perspectiva
- Pide entender un fenómeno, causa, historia o estructura
- Solicita un análisis profundo, un resumen riguroso o un "mapa del tema"
- Pide complementar, ampliar, profundizar o enriquecer información ya existente

---

## Modos de respuesta

No toda activación requiere el proceso completo. Calibrar la profundidad según el tipo de pregunta:

| Modo | Cuándo aplicar | Qué usar |
|---|---|---|
| **Investigación completa** | Nueva pregunta de investigación desde cero | Pasos 1–4 + invocar `analytical-synthesis` |
| **Complemento / profundización** | "Cuéntame más de X", ampliar un punto ya tratado | Desde el paso relevante al gap |
| **Zoom en dimensión** | "Considerando solo el aspecto Y..." | Paso 3–4 + invocar `analytical-synthesis` Step 2 |
| **Comparación directa** | "¿Cuál fue más determinante, A o B?" | Invocar `analytical-synthesis` Steps 3–4 |
| **Aclaración conceptual** | "¿Qué significa X?" | Definición con contexto, sin estructura completa |
| **Validación de hipótesis** | El usuario propone una interpretación y pide confirmarla | Invocar `analytical-synthesis` Step 4 |

**Modo rápido** — para seguimientos en diálogo, aplicar este flujo comprimido:

1. Descomponer automáticamente el sub-tema o gap identificado
2. Buscar guiado por preguntas, no por keywords
3. Invocar `analytical-synthesis` para síntesis jerárquica y verificación de consistencia

---

## Proceso de investigación completo

### Paso 1 — Delimitar la pregunta

Antes de buscar información, precisar:

- ¿Qué se quiere entender exactamente?
- ¿Desde qué ángulo? (histórico, técnico, económico, social…)
- ¿Qué queda explícitamente fuera del scope?

Una pregunta mal delimitada produce investigación dispersa. Reformular si es vaga.

### Paso 2 — Mapa del tema

Convertir el tema en un sistema antes de buscar. Identificar:

- Conceptos clave
- Actores o variables principales
- Relaciones entre elementos
- Subtemas relevantes por dimensión

Este mapa guía qué buscar y evita que la investigación sea lineal.

### Paso 3 — Revisión de literatura

Antes de buscar, formular las preguntas que guiarán la búsqueda — no keywords. Ejemplo: en lugar de buscar "desigualdad Perú", preguntar "¿qué explica que la desigualdad peruana persista después de la independencia?". Esto determina qué es relevante y qué no.

Buscar luego en capas, de mayor a menor rigor:

1. Fuentes académicas (papers, libros, meta-análisis)
2. Reportes institucionales (organismos internacionales, think tanks)
3. Datos y estadísticas (fuentes primarias)
4. Perspectivas críticas o alternativas

Objetivo: identificar qué se sabe, qué se debate y qué falta.

### Paso 4 — Triangulación de fuentes

No consolidar desde una sola perspectiva. Contrastar:

- Perspectiva académica vs. datos empíricos
- Enfoque dominante vs. enfoques críticos
- Fuente institucional vs. fuente independiente

La triangulación controla sesgos y detecta puntos ciegos.

### Pasos 5–8 — Análisis y síntesis → invocar `analytical-synthesis`

Una vez completada la recolección de fuentes (pasos 1–4), invocar el skill `analytical-synthesis` para ejecutar los pasos de análisis. Ese skill es el propietario del framework de dimensiones, síntesis jerárquica, validación cruzada y modelo final.

Los pasos 1–4 son exclusivos de `research`. Los pasos 5–8 son responsabilidad de `analytical-synthesis`.

---

## Gotchas

- **No empezar por buscar** — definir primero el mapa del tema; buscar sin mapa produce acumulación, no comprensión.
- **Buscar por preguntas, no por keywords** — una keyword recupera información; una pregunta recupera relevancia.
- **Síntesis ≠ resumen** — si la salida solo parafrasea fuentes, `analytical-synthesis` no ha hecho su trabajo. Debe haber interpretación y posición propia.
- **Triangulación es obligatoria** — una sola fuente o perspectiva invalida la investigación aunque sea académica.
- **No sobrestructurar seguimientos** — aplicar el proceso completo a una aclaración conceptual o un seguimiento es excesivo. Usar el modo rápido.

---

## Anti-patterns

| Anti-pattern | Por qué es incorrecto |
|---|---|
| Resumir fuentes en secuencia | Produce inventario, no análisis; no detecta patrones ni contradicciones |
| Usar solo fuentes académicas | Ignora datos empíricos y perspectivas críticas; sesgo de campo |
| Investigar sin delimitar scope | La investigación se dispersa y pierde coherencia |
| Presentar "todos los puntos de vista" sin integrar | Falsa neutralidad; evita el trabajo analítico real |
| Asumir que más fuentes = mejor investigación | La calidad de síntesis supera a la cantidad de fuentes |
| Aplicar proceso completo a preguntas de seguimiento | Rompe el flujo del diálogo; usar el modo adecuado según el tipo de pregunta |

---

## Resources

- **`evals/evals.json`** — casos de prueba para verificar que el skill produce análisis correctos.

## Dependencias

- **`analytical-synthesis`** — requerido para pasos 5–8. Debe estar disponible en el mismo directorio de skills.
