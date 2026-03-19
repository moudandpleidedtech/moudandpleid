"""
Seed — SECTOR 02: Lógica de Flujo (10 niveles, 11–20).

Uso (desde la raíz del proyecto):
    python -m scripts.seed_sector_02

Conceptos cubiertos:
    if / else / elif / and / or / not / comparaciones encadenadas / if anidado
Nivel 20: Mini-Boss integrador — diagnóstico multi-condición del Nexo.
"""

import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings
from app.models.challenge import Challenge, DifficultyTier

# ─── Teoría en Markdown ───────────────────────────────────────────────────────

THEORY_N11 = """\
## PROTOCOLO: if / else — La Primera Bifurcación

Un `if` evalúa una condición. Si es verdadera, ejecuta su bloque.
`else` cubre el caso contrario.

```python
codigo = int(input())
if codigo >= 1000:
    print("ACCESO CONCEDIDO")
else:
    print("ACCESO DENEGADO")
```

- La condición NO lleva paréntesis (aunque funcionan)
- El bloque inferior debe tener **4 espacios** de indentación
- Solo uno de los dos bloques se ejecuta por cada corrida

---

## OPERADORES DE COMPARACIÓN

| Operador | Significado    |
|----------|----------------|
| `==`     | igual a        |
| `!=`     | distinto de    |
| `>`      | mayor que      |
| `<`      | menor que      |
| `>=`     | mayor o igual  |
| `<=`     | menor o igual  |
"""

THEORY_N12 = """\
## PROTOCOLO: elif — Bifurcaciones Múltiples

`elif` (else-if) permite evaluar más de dos casos en cadena.
Python los evalúa en orden: el primero verdadero gana.

```python
nivel = int(input())
if nivel > 80:
    print("CRÍTICO")
elif nivel > 50:
    print("ALERTA")
else:
    print("NORMAL")
```

- Puedes tener tantos `elif` como necesites
- Solo se ejecuta el primer bloque cuya condición sea verdadera
- El `else` final es opcional pero cubre todos los casos restantes
"""

THEORY_N13 = """\
## PROTOCOLO: and / or — Condiciones Compuestas

`and` requiere que **ambas** condiciones sean verdaderas.
`or` requiere que **al menos una** sea verdadera.

```python
energia = int(input())
escudo  = int(input())

if energia > 50 and escudo > 50:
    print("OPERATIVO")
else:
    print("VULNERABLE")
```

---

## TABLA DE VERDAD

| A     | B     | A and B | A or B |
|-------|-------|---------|--------|
| True  | True  | True    | True   |
| True  | False | False   | True   |
| False | True  | False   | True   |
| False | False | False   | False  |

```python
# Ejemplo con or
if sensor_a == 1 or sensor_b == 1:
    print("INTRUSO DETECTADO")
```
"""

THEORY_N18 = """\
## PROTOCOLO: if Anidado — Decisiones en Cascada

Un `if` dentro de otro `if` evalúa condiciones en cascada.
Cada nivel de anidación agrega **4 espacios** más de indentación.

```python
usuario = input()
password = input()

if usuario == "admin":
    if password == "nexo2049":
        print("BIENVENIDO, ADMIN")
    else:
        print("CONTRASEÑA INVÁLIDA")
else:
    print("USUARIO NO ENCONTRADO")
```

- El `if` interno solo se evalúa si el externo es verdadero
- Úsalo cuando una condición depende del resultado de otra
- Con más de 3 niveles de anidación, considera reescribir con `and`
"""

# ─── Definición de los 10 niveles ─────────────────────────────────────────────

SECTOR_02 = [
    # ── NIVEL 11 ─────────────────────────────────────────────────────────────
    {
        "title": "Puertas de Seguridad",
        "description": (
            "El Nexo tiene un sistema de acceso por código numérico.\n\n"
            "Lee un entero `codigo`. Si es mayor o igual a `1000`, imprime "
            "`ACCESO CONCEDIDO`. De lo contrario, imprime `ACCESO DENEGADO`."
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "medium",
        "sector_id": 2,
        "level_order": 11,
        "base_xp_reward": 150,
        "is_project": False,
        "telemetry_goal_time": 150,
        "challenge_type": "python",
        "phase": "flujo",
        "concepts_taught_json": json.dumps(["if", "else", ">=", "int()"]),
        "initial_code": (
            "# MISIÓN: Lee un código. Si >= 1000 imprime ACCESO CONCEDIDO, si no ACCESO DENEGADO\n"
            "\n"
            "codigo = int(input())\n"
            "\n"
            "if codigo >= 1000:\n"
            "    # Tu código aquí\n"
            "else:\n"
            "    # Tu código aquí\n"
        ),
        "expected_output": "ACCESO CONCEDIDO",
        "test_inputs_json": json.dumps(["1337"]),
        "lore_briefing": (
            "Operador, el muro perimetral del Nexo sólo cede ante códigos de alta frecuencia. "
            "Los valores inferiores al umbral 1000 activan el protocolo de rechazo automático."
        ),
        "pedagogical_objective": "Introducir if/else con operador >=. Primer nivel del sector de flujo.",
        "syntax_hint": 'if codigo >= 1000:\n    print("ACCESO CONCEDIDO")\nelse:\n    print("ACCESO DENEGADO")',
        "theory_content": THEORY_N11,
        "hints_json": json.dumps([
            "Un if evalúa una condición. Si es verdadera, ejecuta el bloque con 4 espacios de indentación.",
            "Para comparar 'mayor o igual', usa el operador >= : if codigo >= 1000:",
            'Dentro del if: print("ACCESO CONCEDIDO"). Dentro del else: print("ACCESO DENEGADO").',
        ]),
    },
    # ── NIVEL 12 ─────────────────────────────────────────────────────────────
    {
        "title": "Clasificación de Amenazas",
        "description": (
            "El scanner del Nexo mide el nivel de amenaza del 0 al 100.\n\n"
            "Lee un entero `nivel`. Clasifícalo:\n"
            "- Mayor a `80` → `CRÍTICO`\n"
            "- Mayor a `50` → `ALERTA`\n"
            "- Cualquier otro → `NORMAL`"
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "medium",
        "sector_id": 2,
        "level_order": 12,
        "base_xp_reward": 175,
        "is_project": False,
        "telemetry_goal_time": 180,
        "challenge_type": "python",
        "phase": "flujo",
        "concepts_taught_json": json.dumps(["elif", "if", "else", "encadenado"]),
        "initial_code": (
            "# MISIÓN: Clasifica el nivel de amenaza con if / elif / else\n"
            "\n"
            "nivel = int(input())\n"
            "\n"
            "if nivel > 80:\n"
            "    # CRÍTICO\n"
            "elif nivel > 50:\n"
            "    # ALERTA\n"
            "else:\n"
            "    # NORMAL\n"
        ),
        "expected_output": "ALERTA",
        "test_inputs_json": json.dumps(["65"]),
        "lore_briefing": (
            "El sistema de defensa del Nexo tiene tres estados de respuesta: Normal, Alerta y Crítico. "
            "El scanner entrega un valor bruto — DAKI necesita que lo clasifiques antes de que el Nexo reaccione."
        ),
        "pedagogical_objective": "Introducir elif para ramificaciones múltiples. Python evalúa en orden.",
        "syntax_hint": "if nivel > 80:\n    print('CRÍTICO')\nelif nivel > 50:\n    print('ALERTA')\nelse:\n    print('NORMAL')",
        "theory_content": THEORY_N12,
        "hints_json": json.dumps([
            "elif permite una tercera (o más) bifurcación. Se evalúa solo si el if anterior fue falso.",
            "El orden importa: Python comprueba condiciones de arriba a abajo y ejecuta el primer bloque verdadero.",
            "Estructura: if nivel > 80 → print('CRÍTICO'), elif nivel > 50 → print('ALERTA'), else → print('NORMAL').",
        ]),
    },
    # ── NIVEL 13 ─────────────────────────────────────────────────────────────
    {
        "title": "Escudo Dual",
        "description": (
            "Para estar operativo, el mech necesita energía Y escudo activos.\n\n"
            "Lee dos enteros: `energia` y `escudo`. Si **ambos** son mayores a `50`, "
            "imprime `OPERATIVO`. De lo contrario, imprime `VULNERABLE`."
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 2,
        "level_order": 13,
        "base_xp_reward": 200,
        "is_project": False,
        "telemetry_goal_time": 200,
        "challenge_type": "python",
        "phase": "flujo",
        "concepts_taught_json": json.dumps(["and", "operadores lógicos", "if"]),
        "initial_code": (
            "# MISIÓN: Si AMBOS valores > 50, imprime OPERATIVO, si no VULNERABLE\n"
            "\n"
            "energia = int(input())\n"
            "escudo  = int(input())\n"
            "\n"
            "if energia > 50 and escudo > 50:\n"
            "    # Tu código aquí\n"
            "else:\n"
            "    # Tu código aquí\n"
        ),
        "expected_output": "OPERATIVO",
        "test_inputs_json": json.dumps(["75", "60"]),
        "lore_briefing": (
            "Operador, sin energía el mech es una estatua. Sin escudo, es un blanco fácil. "
            "Ambos sistemas deben estar en línea para autorizar la misión."
        ),
        "pedagogical_objective": "Introducir el operador 'and' para condiciones compuestas.",
        "syntax_hint": "if energia > 50 and escudo > 50:\n    print('OPERATIVO')\nelse:\n    print('VULNERABLE')",
        "theory_content": THEORY_N13,
        "hints_json": json.dumps([
            "El operador 'and' une dos condiciones: ambas deben ser verdaderas para que el if se ejecute.",
            "Si una sola falla, 'and' devuelve False aunque la otra sea True.",
            "Escribe: if energia > 50 and escudo > 50: seguido del print correspondiente.",
        ]),
    },
    # ── NIVEL 14 ─────────────────────────────────────────────────────────────
    {
        "title": "Red de Sensores",
        "description": (
            "Dos sensores monitorean el perímetro. Si **al menos uno** detecta movimiento, "
            "hay intrusión.\n\n"
            "Lee dos enteros `sensor_a` y `sensor_b` (`0` = inactivo, `1` = activo). "
            "Si cualquiera vale `1`, imprime `INTRUSO DETECTADO`. "
            "Si ambos son `0`, imprime `PERÍMETRO SEGURO`."
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 2,
        "level_order": 14,
        "base_xp_reward": 200,
        "is_project": False,
        "telemetry_goal_time": 200,
        "challenge_type": "python",
        "phase": "flujo",
        "concepts_taught_json": json.dumps(["or", "operadores lógicos", "if"]),
        "initial_code": (
            "# MISIÓN: Si sensor_a == 1 OR sensor_b == 1 → INTRUSO DETECTADO\n"
            "\n"
            "sensor_a = int(input())\n"
            "sensor_b = int(input())\n"
            "\n"
            "if sensor_a == 1 or sensor_b == 1:\n"
            "    # Tu código aquí\n"
            "else:\n"
            "    # Tu código aquí\n"
        ),
        "expected_output": "INTRUSO DETECTADO",
        "test_inputs_json": json.dumps(["0", "1"]),
        "lore_briefing": (
            "La red perimetral del Nexo tiene dos nodos de detección. "
            "Si cualquiera de los dos registra actividad, el sistema activa la alarma completa."
        ),
        "pedagogical_objective": "Introducir el operador 'or'. Con que una condición sea True, basta.",
        "syntax_hint": "if sensor_a == 1 or sensor_b == 1:\n    print('INTRUSO DETECTADO')\nelse:\n    print('PERÍMETRO SEGURO')",
        "theory_content": None,
        "hints_json": json.dumps([
            "El operador 'or' devuelve True si AL MENOS UNA de las condiciones es verdadera.",
            "A diferencia de 'and', con 'or' basta que un sensor sea 1 para activar la alarma.",
            "Escribe: if sensor_a == 1 or sensor_b == 1: y los prints correspondientes.",
        ]),
    },
    # ── NIVEL 15 ─────────────────────────────────────────────────────────────
    {
        "title": "Inversión de Estado",
        "description": (
            "El operador `not` invierte una condición booleana.\n\n"
            "Lee una cadena `estado`. Si `estado` **no es** `\"OFFLINE\"`, "
            "imprime `SISTEMA ACTIVO`. Si lo es, imprime `SISTEMA CAÍDO`."
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 2,
        "level_order": 15,
        "base_xp_reward": 225,
        "is_project": False,
        "telemetry_goal_time": 210,
        "challenge_type": "python",
        "phase": "flujo",
        "concepts_taught_json": json.dumps(["not", "operadores lógicos", "string comparación"]),
        "initial_code": (
            "# MISIÓN: Si estado NO es OFFLINE → SISTEMA ACTIVO, si no → SISTEMA CAÍDO\n"
            "\n"
            "estado = input()\n"
            "\n"
            'if not estado == "OFFLINE":\n'
            "    # Tu código aquí\n"
            "else:\n"
            "    # Tu código aquí\n"
        ),
        "expected_output": "SISTEMA ACTIVO",
        "test_inputs_json": json.dumps(["ONLINE"]),
        "lore_briefing": (
            "Operador, el nodo 7 reporta su estado al inicio de cada ciclo. "
            "Si no está fuera de línea, debemos mantenerlo en la red táctica."
        ),
        "pedagogical_objective": "Introducir el operador 'not'. Invierte el valor booleano de una condición.",
        "syntax_hint": 'if not estado == "OFFLINE":\n    print("SISTEMA ACTIVO")\nelse:\n    print("SISTEMA CAÍDO")',
        "theory_content": None,
        "hints_json": json.dumps([
            "El operador 'not' invierte True en False y viceversa: not True == False.",
            "'not estado == \"OFFLINE\"' es verdadero cuando estado ES diferente de \"OFFLINE\".",
            'Completa: if not estado == "OFFLINE": → print("SISTEMA ACTIVO"), else → print("SISTEMA CAÍDO").',
        ]),
    },
    # ── NIVEL 16 ─────────────────────────────────────────────────────────────
    {
        "title": "Rango Térmico",
        "description": (
            "Los servidores del Nexo tienen un rango de temperatura operativa.\n\n"
            "Lee un entero `temp`. Evalúa:\n"
            "- Si `18 <= temp <= 25` → `TEMPERATURA ÓPTIMA`\n"
            "- Si `temp < 18` → `DEMASIADO FRÍO`\n"
            "- Cualquier otro → `SOBRECALENTAMIENTO`"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 2,
        "level_order": 16,
        "base_xp_reward": 225,
        "is_project": False,
        "telemetry_goal_time": 220,
        "challenge_type": "python",
        "phase": "flujo",
        "concepts_taught_json": json.dumps(["comparación encadenada", "elif", "rango"]),
        "initial_code": (
            "# MISIÓN: Evalúa la temperatura con comparación encadenada\n"
            "\n"
            "temp = int(input())\n"
            "\n"
            "if 18 <= temp <= 25:\n"
            "    # Tu código aquí\n"
            "elif temp < 18:\n"
            "    # Tu código aquí\n"
            "else:\n"
            "    # Tu código aquí\n"
        ),
        "expected_output": "TEMPERATURA ÓPTIMA",
        "test_inputs_json": json.dumps(["22"]),
        "lore_briefing": (
            "Los núcleos de procesamiento del Nexo tienen un umbral térmico preciso. "
            "Por debajo se congelan los cálculos; por encima se funden los circuitos. "
            "El rango operativo es crítico."
        ),
        "pedagogical_objective": "Usar comparaciones encadenadas de Python (18 <= x <= 25) para verificar rangos.",
        "syntax_hint": "if 18 <= temp <= 25:\n    print('TEMPERATURA ÓPTIMA')\nelif temp < 18:\n    print('DEMASIADO FRÍO')\nelse:\n    print('SOBRECALENTAMIENTO')",
        "theory_content": None,
        "hints_json": json.dumps([
            "Python permite comparaciones encadenadas: 18 <= temp <= 25 verifica que temp esté en ese rango.",
            "Equivale a: if temp >= 18 and temp <= 25, pero más legible.",
            "Estructura: if 18 <= temp <= 25 → ÓPTIMA, elif temp < 18 → FRÍO, else → SOBRECALENTAMIENTO.",
        ]),
    },
    # ── NIVEL 17 ─────────────────────────────────────────────────────────────
    {
        "title": "Firewall de Puertos",
        "description": (
            "El firewall del Nexo identifica protocolos por número de puerto.\n\n"
            "Lee un entero `puerto`. Identifícalo:\n"
            "- `80` → `HTTP`\n"
            "- `443` → `HTTPS`\n"
            "- `22` → `SSH`\n"
            "- Cualquier otro → `PUERTO DESCONOCIDO`"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 2,
        "level_order": 17,
        "base_xp_reward": 250,
        "is_project": False,
        "telemetry_goal_time": 230,
        "challenge_type": "python",
        "phase": "flujo",
        "concepts_taught_json": json.dumps(["elif múltiple", "==", "if/elif/else"]),
        "initial_code": (
            "# MISIÓN: Identifica el protocolo según el número de puerto\n"
            "\n"
            "puerto = int(input())\n"
            "\n"
            "if puerto == 80:\n"
            "    # HTTP\n"
            "elif puerto == 443:\n"
            "    # Tu código\n"
            "elif puerto == 22:\n"
            "    # Tu código\n"
            "else:\n"
            "    # Tu código\n"
        ),
        "expected_output": "HTTPS",
        "test_inputs_json": json.dumps(["443"]),
        "lore_briefing": (
            "Cada puerto abierto en el Nexo es un vector de ataque potencial. "
            "El sistema de seguridad necesita identificar el protocolo de cada conexión entrante "
            "para aplicar las contramedidas correctas."
        ),
        "pedagogical_objective": "Múltiples elif con comparación de igualdad. Caso clásico de 'switch' en Python.",
        "syntax_hint": "if puerto == 80:\n    print('HTTP')\nelif puerto == 443:\n    print('HTTPS')\nelif puerto == 22:\n    print('SSH')\nelse:\n    print('PUERTO DESCONOCIDO')",
        "theory_content": None,
        "hints_json": json.dumps([
            "Cuando tienes muchos casos exactos, encadena elif para cada uno.",
            "Usa == para comparar valores exactos: if puerto == 443 comprueba si el puerto es exactamente 443.",
            "Estructura: if 80→HTTP, elif 443→HTTPS, elif 22→SSH, else→PUERTO DESCONOCIDO.",
        ]),
    },
    # ── NIVEL 18 ─────────────────────────────────────────────────────────────
    {
        "title": "Autenticación en Dos Fases",
        "description": (
            "El acceso admin requiere verificar usuario **y luego** contraseña.\n\n"
            "Lee `usuario` y `password` (uno por línea). Evalúa:\n"
            "- Si usuario es `\"admin\"` y password es `\"nexo2049\"` → `BIENVENIDO, ADMIN`\n"
            "- Si usuario es `\"admin\"` pero password es incorrecto → `CONTRASEÑA INVÁLIDA`\n"
            "- Si usuario no es `\"admin\"` → `USUARIO NO ENCONTRADO`"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 2,
        "level_order": 18,
        "base_xp_reward": 275,
        "is_project": False,
        "telemetry_goal_time": 260,
        "challenge_type": "python",
        "phase": "flujo",
        "concepts_taught_json": json.dumps(["if anidado", "string comparación", "autenticación"]),
        "initial_code": (
            "# MISIÓN: Valida usuario y luego contraseña con if anidado\n"
            "\n"
            "usuario  = input()\n"
            "password = input()\n"
            "\n"
            'if usuario == "admin":\n'
            '    if password == "nexo2049":\n'
            "        # Tu código\n"
            "    else:\n"
            "        # Tu código\n"
            "else:\n"
            "    # Tu código\n"
        ),
        "expected_output": "BIENVENIDO, ADMIN",
        "test_inputs_json": json.dumps(["admin", "nexo2049"]),
        "lore_briefing": (
            "Operador, el núcleo de administración del Nexo usa autenticación en cascada: "
            "primero verifica la identidad, luego la clave de acceso. "
            "Una falla en cualquier paso activa el protocolo de rechazo."
        ),
        "pedagogical_objective": "Introducir if anidado. La segunda condición solo se evalúa si la primera es verdadera.",
        "syntax_hint": 'if usuario == "admin":\n    if password == "nexo2049":\n        print("BIENVENIDO, ADMIN")\n    else:\n        print("CONTRASEÑA INVÁLIDA")\nelse:\n    print("USUARIO NO ENCONTRADO")',
        "theory_content": THEORY_N18,
        "hints_json": json.dumps([
            "El if anidado va dentro de otro if, con 8 espacios de indentación (4 + 4).",
            "El if interno solo se comprueba cuando el externo ya fue True (usuario correcto).",
            'Estructura: if usuario=="admin": / if password=="nexo2049": → BIENVENIDO / else → CONTRASEÑA / else → NO ENCONTRADO.',
        ]),
    },
    # ── NIVEL 19 ─────────────────────────────────────────────────────────────
    {
        "title": "Evaluador de Rango",
        "description": (
            "El sistema de rangos del Nexo combina misiones completadas y precisión.\n\n"
            "Lee dos enteros: `misiones` y `precision` (0–100). Evalúa:\n"
            "- `misiones >= 10` **y** `precision >= 90` → `RANGO: ÉLITE`\n"
            "- `misiones >= 5` **y** `precision >= 70` → `RANGO: VETERANO`\n"
            "- `misiones >= 1` → `RANGO: NOVATO`\n"
            "- Cualquier otro → `RANGO: CERO`"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 2,
        "level_order": 19,
        "base_xp_reward": 300,
        "is_project": False,
        "telemetry_goal_time": 280,
        "challenge_type": "python",
        "phase": "flujo",
        "concepts_taught_json": json.dumps(["and", "elif", "condiciones compuestas", "lógica compleja"]),
        "initial_code": (
            "# MISIÓN: Determina el rango con condiciones compuestas\n"
            "\n"
            "misiones  = int(input())\n"
            "precision = int(input())\n"
            "\n"
            "if misiones >= 10 and precision >= 90:\n"
            "    # ÉLITE\n"
            "elif misiones >= 5 and precision >= 70:\n"
            "    # Tu código\n"
            "elif misiones >= 1:\n"
            "    # Tu código\n"
            "else:\n"
            "    # Tu código\n"
        ),
        "expected_output": "RANGO: VETERANO",
        "test_inputs_json": json.dumps(["7", "85"]),
        "lore_briefing": (
            "Operador, el sistema de clasificación del Nexo no solo mide la cantidad de misiones — "
            "también mide la calidad. Solo los operadores con ambas métricas en verde alcanzan el rango Élite."
        ),
        "pedagogical_objective": "Combinar 'and' con elif para lógica de clasificación multi-criterio.",
        "syntax_hint": "if misiones >= 10 and precision >= 90:\n    print('RANGO: ÉLITE')\nelif misiones >= 5 and precision >= 70:\n    print('RANGO: VETERANO')",
        "theory_content": None,
        "hints_json": json.dumps([
            "Combina 'and' con elif: cada caso necesita que AMBAS condiciones sean verdaderas.",
            "Python evalúa de arriba a abajo: si 7 misiones y 85% no pasan el umbral élite (10 y 90), prueba veterano.",
            "El tercer elif (misiones >= 1) no necesita 'and' — aplica para cualquier operador con al menos 1 misión.",
        ]),
    },
    # ── NIVEL 20 — MINI-BOSS ─────────────────────────────────────────────────
    {
        "title": "NEXUS-02: El Árbitro del Sistema",
        "description": (
            "**MINI-BOSS — SECTOR 02**\n\n"
            "El Nexo necesita un diagnóstico completo en tiempo real. Construye el programa que "
            "evalúa tres sistemas y emite un informe de estado.\n\n"
            "**Entrada:** `energia` (int), `escudos` (int), `intrusion` (int), uno por línea.\n\n"
            "**Reglas:**\n"
            "- Energía ≥ 75 → `ÓPTIMA`, si no → `CRÍTICA`\n"
            "- Escudos ≥ 50 → `ACTIVOS`, si no → `INACTIVOS`\n"
            "- Intrusión ≥ 70 → `CRÍTICA`, ≥ 40 → `ALERTA`, < 40 → `BLOQUEADA`\n"
            "- Estado general: energía ≥ 75 AND escudos ≥ 50 AND intrusión < 40 → `OPERATIVO`; "
            "energía < 30 OR intrusión ≥ 70 → `CAÍDO`; resto → `COMPROMETIDO`\n\n"
            "**Salida esperada** (con entradas `80`, `60`, `30`):\n"
            "```\n"
            "=== DIAGNÓSTICO DEL NEXO ===\n"
            "Energía: ÓPTIMA\n"
            "Escudos: ACTIVOS\n"
            "Intrusión: BLOQUEADA\n"
            "Estado General: OPERATIVO\n"
            "```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "hard",
        "sector_id": 2,
        "level_order": 20,
        "base_xp_reward": 600,
        "is_project": True,
        "telemetry_goal_time": 420,
        "challenge_type": "python",
        "phase": "proyecto",
        "concepts_taught_json": json.dumps([
            "if", "elif", "else", "and", "or", "variables de estado", "f-strings", "integración"
        ]),
        "initial_code": (
            "# ╔════════════════════════════════════════════════╗\n"
            "# ║  NEXUS-02: MINI-BOSS — ÁRBITRO DEL SISTEMA    ║\n"
            "# ╚════════════════════════════════════════════════╝\n"
            "#\n"
            "# Evalúa los 3 sistemas y genera el diagnóstico completo.\n"
            "\n"
            "energia   = int(input())\n"
            "escudos   = int(input())\n"
            "intrusion = int(input())\n"
            "\n"
            "# 1. Estado de energía (>= 75 → ÓPTIMA, si no → CRÍTICA)\n"
            "estado_energia = \n"
            "\n"
            "# 2. Estado de escudos (>= 50 → ACTIVOS, si no → INACTIVOS)\n"
            "estado_escudos = \n"
            "\n"
            "# 3. Estado de intrusión (>= 70 → CRÍTICA | >= 40 → ALERTA | < 40 → BLOQUEADA)\n"
            "estado_intrusion = \n"
            "\n"
            "# 4. Estado general (AND/OR con las 3 variables)\n"
            "estado_general = \n"
            "\n"
            "# 5. Imprime el diagnóstico (5 líneas exactas)\n"
        ),
        "expected_output": (
            "=== DIAGNÓSTICO DEL NEXO ===\n"
            "Energía: ÓPTIMA\n"
            "Escudos: ACTIVOS\n"
            "Intrusión: BLOQUEADA\n"
            "Estado General: OPERATIVO"
        ),
        "test_inputs_json": json.dumps(["80", "60", "30"]),
        "lore_briefing": (
            "Operador, el Nexo está en modo de crisis. Tres sistemas reportan anomalías simultáneas. "
            "Necesito que construyas el árbitro de decisiones que evalúe energía, escudos e intrusión "
            "y me dé un diagnóstico consolidado. La estabilidad del Nexo depende de tu lógica."
        ),
        "pedagogical_objective": (
            "Mini-Boss integrador del Sector 02. Combina: if/elif/else, and, or, variables de estado "
            "y f-strings para construir un sistema de diagnóstico multi-condición."
        ),
        "syntax_hint": (
            "estado_energia = 'ÓPTIMA' if energia >= 75 else 'CRÍTICA'\n"
            "estado_escudos = 'ACTIVOS' if escudos >= 50 else 'INACTIVOS'\n"
            "if intrusion >= 70: estado_intrusion = 'CRÍTICA'\n"
            "elif intrusion >= 40: estado_intrusion = 'ALERTA'\n"
            "else: estado_intrusion = 'BLOQUEADA'"
        ),
        "theory_content": None,
        "hints_json": json.dumps([
            "Divide el problema en 4 partes: calcula cada estado_xxx por separado, luego el estado_general.",
            "Para el estado general: if energia >= 75 and escudos >= 50 and intrusion < 40 → OPERATIVO, elif energia < 30 or intrusion >= 70 → CAÍDO, else → COMPROMETIDO.",
            (
                "Usa variables intermedias: estado_energia = 'ÓPTIMA' if energia >= 75 else 'CRÍTICA'. "
                "Luego imprime con f-strings: print(f'Energía: {estado_energia}')."
            ),
        ]),
    },
]


# ─── Lógica de población ──────────────────────────────────────────────────────

async def seed() -> None:
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    async with SessionLocal() as session:
        deleted = await session.execute(
            delete(Challenge).where(Challenge.sector_id == 2)
        )
        await session.flush()
        print(f"🧹  Sector 02 anterior eliminado — {deleted.rowcount} challenge(s) removidos.")

        print(f"\n🌱  Insertando {len(SECTOR_02)} niveles del Sector 02...\n")
        for data in SECTOR_02:
            challenge = Challenge(**data)
            session.add(challenge)
            project_flag = " ★ MINI-BOSS" if data["is_project"] else ""
            print(
                f"    [{data['level_order']:02d}/20] {data['title']:<40} "
                f"({data['difficulty'].upper()}, {data['base_xp_reward']} XP, "
                f"~{data['telemetry_goal_time']}s){project_flag}"
            )

        await session.commit()

    await engine.dispose()
    print(f"\n✅  Sector 02 cargado — {len(SECTOR_02)} niveles listos.")
    print("    Conceptos: if · elif · else · and · or · not · if anidado · diagnóstico multi-condición\n")


if __name__ == "__main__":
    asyncio.run(seed())
