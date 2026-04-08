# DAKI EdTech — Guión de Demo Técnica
**Audiencia:** Jefe de Desarrollo / CTO / Tech Lead  
**Duración:** 20-30 minutos  
**Usuario demo:** `demo@dakiedtech.com` / `DemoDaki2025!`

---

## Antes de la reunión

- [ ] Ejecutar `python -m scripts.create_demo_user --no-dry-run` en Render (o local con DB de prod)
- [ ] Agregar `demo@dakiedtech.com` a `ALPHA_WHITELIST` en Render si está activa
- [ ] Abrir dakiedtech.com en el browser y loguear con el usuario demo
- [ ] Verificar que el Hub cargue con el progreso visible (nivel 28, liga Plata)
- [ ] Tener una pestaña extra con la landing page / para el CTA final
- [ ] Silenciar notificaciones del sistema

---

## Apertura (2 min)

**No vendas la herramienta. Identificá el dolor primero.**

> "Antes de mostrarte lo que construí, necesito entender algo.
> Cuando incorporás un dev junior o mid a tu equipo, ¿cuánto tiempo
> tarda en ser productivo de verdad? No en saber escribir código —
> en poder trabajar solo en tickets reales."

Dejá que responda. Escuchá. Las respuestas típicas son 2-4 semanas hasta
3 meses. Independientemente de lo que diga, el problema es el mismo:
el onboarding técnico es lento, costoso, y depende de que los seniors
dediquen tiempo que no tienen.

> "Exacto. DAKI resuelve eso."

---

## Bloque 1 — El problema que DAKI resuelve (3 min)

**Frase gancho:**
> "El problema no es que los juniors no saben código.
> El problema es que no saben *pensar* en código.
> Saben buscar en Stack Overflow, pero no diagnosticar.
> DAKI entrena el segundo tipo de conocimiento."

**Puntos clave a tocar:**
- Los LMS tradicionales (Udemy, Platzi) enseñan a copiar — no a debuggear
- Un dev que solo sabe copiar bloquea al senior con preguntas repetitivas
- DAKI entrena autonomía: leer errores, razonar sobre código, pedir ayuda con contexto
- Resultado medible: el dev llega al equipo sabiendo articular su problema, no solo reportar "no funciona"

---

## Bloque 2 — El Hub (2 min)

Mostrá el Hub con el usuario demo logueado.

**Puntos a señalar:**
1. **Campaign Map** — "Esto es el currículo. 190 niveles organizados en zonas.
   El dev no elige qué estudiar — el sistema lo guía al siguiente paso crítico."
2. **Badge de Rango** — "El progreso es visible. Liga Plata, 7 días de racha.
   Esto gamifica el aprendizaje sin hacer que parezca un juego de celular."
3. **Revisión Semanal** — "El sistema trackea qué conceptos tienen baja maestría
   y los vuelve a presentar. Spaced Repetition automático."

> "¿Notás algo? No hay un botón de 'ver video'. Cada interacción
> requiere que el dev produzca algo — código, una predicción, una explicación."

---

## Bloque 3 — El IDE en acción (8 min) ← EL NÚCLEO DE LA DEMO

Navegá a un challenge del Sector 3 (Ciclos For) — el nivel L27 está abierto.

**Paso 1: Mostrá el briefing táctico**
> "El sistema no solo da un enunciado. Da contexto. ¿Por qué importa esto?
> ¿Dónde se usa en producción real? El dev llega al editor sabiendo *para qué*."

**Paso 2: Escribí código incorrecto a propósito**
Escribí algo que genere un error (ej: `for i in range(1, 11) print(i)` — SyntaxError).

Mostrá cómo DAKI:
- Explica el error en español, en voz de operadora táctica
- No da la solución — explica *qué* está mal y *por qué*
- El dev tiene que pensar, no copiar

> "Esto es lo que diferencia a DAKI de un tutorial.
> El error no desaparece — se convierte en aprendizaje."

**Paso 3: Pedí una pista (ENIGMA)**
Si el error persiste, mostrá el Modo Socrático:
- DAKI hace preguntas ("¿Qué va después de range() en un for?") en lugar de dar la respuesta
- Es el método socrático aplicado a debugging

> "El objetivo no es que el dev llegue a la respuesta — es que desarrolle el
> hábito de hacerse preguntas antes de pedir ayuda."

**Paso 4: Solucioná el código y ejecutá**
Mostrá la victoria:
- XP y animación
- La pregunta metacognitiva post-misión ("¿Qué cambiarías si el tipo de datos fuera diferente?")
- El feedback de code review de DAKI ("podrías usar list comprehension aquí")

> "Ese último paso es crítico. No termina con 'correcto, siguiente'.
> Termina con reflexión. Así es como se forma criterio técnico."

---

## Bloque 4 — El ángulo de negocio (5 min)

Este bloque va dirigido al tech lead, no al desarrollador.

**Mostrá el perfil público** (`/p/DEMO_OPERATOR`)
> "Cada dev tiene un perfil verificable. Nivel, XP, misiones completadas.
> Cuando contratás a alguien que pasó por DAKI, sabés exactamente en qué punto está."

**Mencioná los datos que el sistema genera:**
> "Para vos como responsable técnico, esto genera telemetría real:
> qué conceptos tiene flojo el equipo, cuántos devs están bloqueados en el mismo nivel,
> qué errores se repiten. No es solo entrenamiento — es diagnóstico."

**El modelo de negocio para empresas:**
> "Para una empresa como la tuya, el modelo es por equipo.
> No pagás un curso que nadie termina — pagás por el acceso de tu equipo
> a un sistema que tiene un mecanismo anti-abandono incorporado.
> La racha de días, la liga, el leaderboard — todo está diseñado para que el dev vuelva."

---

## Bloque 5 — Cierre y siguiente paso (3 min)

**No cerrés la demo con "¿qué te parece?". Cerrá con una propuesta concreta.**

> "Lo que me interesa saber es esto: ¿tenés 2 o 3 devs en tu equipo
> que se beneficiarían de tener esto disponible durante el próximo mes?
> No como reemplazo de nada — como complemento a lo que ya hacen."

Si dice sí:
> "Puedo darte acceso a esos 3 devs esta semana. Sin costo, sin contrato.
> Al final del mes me contás si notaste diferencia en cómo vienen a las reviews."

Si pide más información:
> "¿Qué es lo que más te generó duda en lo que viste?"
> Respondé esa duda específica y volvé a la propuesta concreta.

---

## Objeciones frecuentes y respuestas

**"Los seniors no van a tener tiempo de supervisar esto"**
> "Correcto — ese es exactamente el punto. DAKI es el supervisor
> que trabaja 24/7 y no interrumpe a tu senior. El senior entra
> cuando el junior ya intentó, falló, y articuló su problema."

**"Ya tenemos un programa de onboarding"**
> "¿Qué tan escalable es? Si incorporás 3 devs a la vez, ¿el programa funciona igual?
> DAKI no reemplaza tu onboarding — es el bloque de 'nivelación técnica'
> que ocurre antes de que el dev toque el código de producción."

**"¿Por qué Python y no [lenguaje de la empresa]?"**
> "Python es el lenguaje de la lógica — algoritmos, estructuras de datos, pensamiento computacional.
> Un dev que sabe pensar en Python puede aprender cualquier lenguaje en semanas.
> El problema no es el lenguaje — es el pensamiento. Y eso lo entrenamos aquí."

**"¿Cuánto cuesta?"**
> "Para equipos de 3-5 devs, menos de lo que te cuesta 4 horas de tu tiempo
> explicando lo mismo por tercera vez. ¿Quién debería ser el primero en tu equipo en probarlo?"

---

## Credenciales del usuario demo

| Campo | Valor |
|-------|-------|
| URL | dakiedtech.com |
| Email | demo@dakiedtech.com |
| Password | DemoDaki2025! |
| Nivel | 28 |
| Liga | Plata |
| XP | 4.850 |

---

## Lo que NO hacer en la demo

- ❌ No mostrés el onboarding — es para principiantes, no impresiona a un tech lead
- ❌ No mostrés el admin dashboard — es tuyo, no de él
- ❌ No hables de "gamificación" como si fuera el punto central — es el mecanismo, no el valor
- ❌ No digas "plataforma de e-learning" — eso lo asocia con Udemy. Decí "sistema de entrenamiento técnico"
- ❌ No respondas "¿cuánto cuesta?" con un número antes de entender el tamaño del equipo

---

*Preparado para demo 2026-04-08 — DAKI EdTech v1.0*
