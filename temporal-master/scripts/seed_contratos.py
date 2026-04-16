"""
Seed — CONTRATOS: Proyectos Finales de Certificación (niveles 60, 70, 80, 140, 185).

NOTA: sector_ids y level_orders actualizados post-migración restructure_sectors.
  Sector_ids originales (5,6,7,13,17) ahora son (6,7,8,14,18).
  Level_orders originales (50,60,70,130,175) ahora son (60,70,80,140,185).

Uso (desde la raíz del proyecto):
    python -m scripts.seed_contratos

Comportamiento:
    1. Elimina solo los challenges con sector_id IN (6, 7, 8, 14, 18) (idempotente).
    2. Inserta los 5 contratos de dificultad EXPERT, uno por sector.

Contratos:
    60  — Sector 06 — Terminal de Acceso         (while + dict, autenticación)
    70  — Sector 07 — Procesador de Datos        (función + lista de dicts, promedio)
    80  — Sector 08 — Calculadora de Daño        (función + dict modificadores)
    140 — Sector 14 — Clasificador de Operadores (OOP: herencia + override + max/key)
    185 — Sector 18 — Procesador Táctico         (Strategy pattern + Protocol + testing)

theory_content almacena la especificación técnica y el script de validación interna.
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

# ─── Especificaciones técnicas + scripts de validación ───────────────────────

SPEC_C50 = """\
## CONTRATO-50 — Especificación Técnica: Terminal de Acceso

### Credenciales del sistema (predefinidas)
```python
USUARIOS = {
    "nexo":  "nexo123",
    "admin": "admin999",
}
```

### Protocolo de autenticación
- Máximo **3 intentos** usando un bucle `while`
- Cada intento lee `usuario` y `clave` con dos `input()` consecutivos
- Si las credenciales coinciden con el diccionario:
  - Imprimir `BIENVENIDO, {USUARIO_EN_MAYUSCULAS}` y terminar
- Si no coinciden y quedan intentos:
  - Imprimir `CLAVE INCORRECTA. Intentos restantes: {n}`
- Si se agotan los 3 intentos sin éxito:
  - Imprimir `ACCESO DENEGADO. SISTEMA BLOQUEADO.`

---

### Script de Validación Interna

```python
# Test A — 3 fallos consecutivos → bloqueo del sistema
inputs_A = ["nexo", "mala", "nexo", "mala", "nexo", "mala"]
expected_A = (
    "CLAVE INCORRECTA. Intentos restantes: 2\\n"
    "CLAVE INCORRECTA. Intentos restantes: 1\\n"
    "CLAVE INCORRECTA. Intentos restantes: 0\\n"
    "ACCESO DENEGADO. SISTEMA BLOQUEADO."
)

# Test B — 2 fallos + éxito en el tercer intento (evaluación oficial)
inputs_B = ["nexo", "mala1", "nexo", "mala2", "nexo", "nexo123"]
expected_B = (
    "CLAVE INCORRECTA. Intentos restantes: 2\\n"
    "CLAVE INCORRECTA. Intentos restantes: 1\\n"
    "BIENVENIDO, NEXO"
)

# Test C — éxito en el primer intento
inputs_C = ["admin", "admin999"]
expected_C = "BIENVENIDO, ADMIN"
```
"""

SPEC_C60 = """\
## CONTRATO-60 — Especificación Técnica: Procesador de Datos

### Firma de la función requerida
```python
def salario_promedio(empleados: list[dict]) -> float:
    \"\"\"
    Recibe una lista de dicts con claves 'nombre' y 'salario'.
    Retorna el salario promedio como float.
    \"\"\"
```

### Formato de entrada (stdin)
```
n               ← cantidad de empleados
nombre_1        ← nombre del empleado 1
salario_1       ← salario (entero)
nombre_2
salario_2
...
```

### Formato de salida
El script imprime el resultado de `salario_promedio(lista)` con `print()`.

---

### Script de Validación Interna

```python
# Test A — 4 empleados con promedio exacto (evaluación oficial)
empleados_A = [
    {"nombre": "Ana",    "salario": 5000},
    {"nombre": "Bob",    "salario": 3500},
    {"nombre": "Carlos", "salario": 4200},
    {"nombre": "Diana",  "salario": 7800},
]
# (5000+3500+4200+7800)/4 = 20500/4 = 5125.0
assert salario_promedio(empleados_A) == 5125.0    # expected_output: "5125.0"

# Test B — 1 empleado (caso borde)
empleados_B = [{"nombre": "Solo", "salario": 9000}]
assert salario_promedio(empleados_B) == 9000.0

# Test C — promedio no entero
empleados_C = [
    {"nombre": "X", "salario": 1000},
    {"nombre": "Y", "salario": 2000},
    {"nombre": "Z", "salario": 3000},
]
assert salario_promedio(empleados_C) == 2000.0
```
"""

SPEC_C130 = """\
## CONTRATO-130 — Especificación Técnica: Clasificador de Operadores

### Clases requeridas

```python
class Operador:
    def __init__(self, nombre: str, nivel: int) -> None: ...
    def eficiencia(self) -> int: ...   # retorna nivel * 10

class OperadorElite(Operador):
    def eficiencia(self) -> int: ...   # override: retorna nivel * 15
```

### Función requerida

```python
def seleccionar_lider(equipo: list) -> str:
    \"\"\"Retorna el nombre del operador con mayor eficiencia.\"\"\"
```

### Datos de prueba (predefinidos en el skeleton)

```python
equipo = [
    Operador("VASQUEZ", 8),      # eficiencia = 80
    OperadorElite("NOVA", 6),    # eficiencia = 90  (elite: 6*15)
    Operador("ROOK", 10),        # eficiencia = 100
]
```

### Formato de salida

```
ROOK
100
```

---

### Script de Validación Interna

```python
# Verificar eficiencias base
assert Operador("X", 5).eficiencia()      == 50
assert OperadorElite("Y", 5).eficiencia() == 75   # 5*15

# Verificar herencia
assert isinstance(OperadorElite("Z", 3), Operador)

# Verificar selección
equipo_test = [Operador("A", 4), OperadorElite("B", 3), Operador("C", 7)]
# A:40, B:45 (elite), C:70 → lider=C
assert seleccionar_lider(equipo_test) == "C"

# Verificar que retorna string, no objeto
assert isinstance(seleccionar_lider(equipo_test), str)
```
"""

SPEC_C175 = """\
## CONTRATO-175 — Especificación Técnica: Procesador Táctico

### Interfaz requerida (Protocol o ABC)

```python
from typing import Protocol

class EstrategiaOrden(Protocol):
    def ordenar(self, datos: list[int]) -> list[int]: ...
```

### Clases de estrategia requeridas

```python
class OrdenAscendente:
    def ordenar(self, datos: list[int]) -> list[int]:
        return sorted(datos)                  # de menor a mayor

class OrdenDescendente:
    def ordenar(self, datos: list[int]) -> list[int]:
        return sorted(datos, reverse=True)    # de mayor a menor
```

### Clase principal requerida

```python
class ProcesadorTactico:
    def __init__(self, estrategia: EstrategiaOrden) -> None: ...
    def cambiar_estrategia(self, estrategia: EstrategiaOrden) -> None: ...
    def procesar(self, datos: list[int]) -> str:
        # Aplica estrategia y une con espacio: "7 15 23 42 99"
```

### Función de test requerida

```python
def test_procesador() -> bool:
    proc = ProcesadorTactico(OrdenAscendente())
    assert proc.procesar([5, 1, 3]) == "1 3 5"
    proc.cambiar_estrategia(OrdenDescendente())
    assert proc.procesar([5, 1, 3]) == "5 3 1"
    return True
```

### Formato de salida

```
7 15 23 42 99
99 42 23 15 7
TEST: OK
```

---

### Script de Validación Interna

```python
datos = [42, 7, 15, 99, 23]

proc = ProcesadorTactico(OrdenAscendente())
assert proc.procesar(datos) == "7 15 23 42 99"

proc.cambiar_estrategia(OrdenDescendente())
assert proc.procesar(datos) == "99 42 23 15 7"

# Verifica que test_procesador no modifica la lista original
original = [5, 1, 3]
copia = original.copy()
proc2 = ProcesadorTactico(OrdenAscendente())
proc2.procesar(original)
assert original == copia, "procesar() no debe mutar la lista original"

assert test_procesador() == True
```
"""

SPEC_C70 = """\
## CONTRATO-70 — Especificación Técnica: Calculadora de Daño Táctico

### Tabla de modificadores (predefinida en el skeleton)
```python
MODIFICADORES = {
    "LASER":   {"base": 100, "mult": 1.5},
    "PLASMA":  {"base": 80,  "mult": 2.0},
    "KINETIC": {"base": 120, "mult": 1.2},
}
```

### Firma de la función requerida
```python
def calcular_dano(tipo_ataque: str, nivel_defensa: int) -> int:
    \"\"\"
    Calcula el daño neto usando la fórmula:
        round(base * mult - nivel_defensa * 0.5)
    Si tipo_ataque no existe en MODIFICADORES, retorna 0.
    \"\"\"
```

### Formato de entrada/salida
- Entrada: tipo de ataque (str) y nivel de defensa (int), uno por línea
- Salida: daño neto (int)

---

### Script de Validación Interna

```python
# Test A — PLASMA con defensa 30 (evaluación oficial)
# 80 * 2.0 - 30 * 0.5 = 160 - 15 = 145
assert calcular_dano("PLASMA", 30)  == 145     # expected_output: "145"

# Test B — LASER con defensa 40
# 100 * 1.5 - 40 * 0.5 = 150 - 20 = 130
assert calcular_dano("LASER", 40)   == 130

# Test C — KINETIC con defensa 20
# round(120 * 1.2 - 20 * 0.5) = round(144 - 10) = 134
assert calcular_dano("KINETIC", 20) == 134

# Test D — tipo desconocido → 0
assert calcular_dano("UNKNOWN", 50) == 0
```
"""


# ─── Contratos ────────────────────────────────────────────────────────────────

CONTRATOS = [
    # ══════════════════════════════════════════════════════════════════════════
    # CONTRATO-50: Terminal de Acceso
    # ══════════════════════════════════════════════════════════════════════════
    {
        "title": "CONTRATO-50: Terminal de Acceso",
        "description": (
            "**CONTRATO DE CERTIFICACIÓN — SECTOR 05**\n\n"
            "El núcleo del Nexo está protegido por una terminal de acceso de máxima seguridad. "
            "Un agente infiltrado tiene solo **3 intentos** para introducir las credenciales "
            "correctas antes de que el sistema se bloquee permanentemente.\n\n"
            "**Tu misión:** Implementa el sistema de autenticación completo.\n\n"
            "**Credenciales válidas:**\n"
            "- usuario `nexo` → clave `nexo123`\n"
            "- usuario `admin` → clave `admin999`\n\n"
            "**Lógica requerida:**\n"
            "1. Bucle `while` con máximo 3 intentos\n"
            "2. Cada intento lee `usuario` y `clave` con `input()`\n"
            "3. Si es válido → `BIENVENIDO, {USUARIO_EN_MAYUSCULAS}` y termina\n"
            "4. Si es inválido → `CLAVE INCORRECTA. Intentos restantes: {n}`\n"
            "5. Si se agotan → `ACCESO DENEGADO. SISTEMA BLOQUEADO.`\n\n"
            "**Entradas de prueba:** `nexo`, `mala1`, `nexo`, `mala2`, `nexo`, `nexo123`\n\n"
            "**Salida esperada:**\n"
            "```\n"
            "CLAVE INCORRECTA. Intentos restantes: 2\n"
            "CLAVE INCORRECTA. Intentos restantes: 1\n"
            "BIENVENIDO, NEXO\n"
            "```"
        ),
        "difficulty_tier": DifficultyTier.ADVANCED,
        "difficulty": "expert",
        "sector_id": 6,
        "level_order": 60,
        "base_xp_reward": 1500,
        "is_project": True,
        "telemetry_goal_time": 600,
        "challenge_type": "python",
        "phase": "contrato",
        "concepts_taught_json": json.dumps([
            "while", "diccionarios", "autenticación", "break",
            "intentos limitados", "upper()", "control de flujo avanzado"
        ]),
        "initial_code": (
            "# ╔══════════════════════════════════════════════════════╗\n"
            "# ║  CONTRATO-50: TERMINAL DE ACCESO                    ║\n"
            "# ║  Dificultad: EXPERT — Proyecto de Certificación     ║\n"
            "# ╚══════════════════════════════════════════════════════╝\n"
            "#\n"
            "# Implementa el sistema de autenticación con 3 intentos.\n"
            "# Las credenciales válidas están en el diccionario USUARIOS.\n"
            "\n"
            "USUARIOS = {\n"
            '    "nexo":  "nexo123",\n'
            '    "admin": "admin999",\n'
            "}\n"
            "\n"
            "intentos  = 0\n"
            "max_intentos = 3\n"
            "acceso   = False\n"
            "\n"
            "while intentos < max_intentos:\n"
            "    usuario = input()\n"
            "    clave   = input()\n"
            "    intentos += 1\n"
            "    restantes = max_intentos - intentos\n"
            "\n"
            "    # Verifica si las credenciales son correctas\n"
            "    # Si sí: imprime bienvenida, cambia acceso a True y sal del bucle\n"
            "    # Si no: imprime 'CLAVE INCORRECTA. Intentos restantes: {restantes}'\n"
            "\n"
            "# Si no hubo acceso exitoso, imprime el mensaje de bloqueo\n"
        ),
        "expected_output": (
            "CLAVE INCORRECTA. Intentos restantes: 2\n"
            "CLAVE INCORRECTA. Intentos restantes: 1\n"
            "BIENVENIDO, NEXO"
        ),
        "test_inputs_json": json.dumps([
            "nexo", "mala1",
            "nexo", "mala2",
            "nexo", "nexo123",
        ]),
        "lore_briefing": (
            "Operador, el núcleo central del Nexo fue comprometido por un agente doble. "
            "Para evitar el acceso no autorizado, DAKI ha activado el Protocolo de Bloqueo Trifásico: "
            "solo tres intentos antes del cierre total del sistema. "
            "Necesitas construir el guardián de la terminal — un sistema que diferencie "
            "al aliado del infiltrado con precisión quirúrgica. El Nexo no admite errores aquí."
        ),
        "pedagogical_objective": (
            "Contrato integrador de Sectores 01-05. Combina: while + contador, "
            "diccionarios como base de datos de credenciales, string methods (upper()), "
            "break para salida anticipada, flag booleano para lógica post-bucle."
        ),
        "syntax_hint": (
            "while intentos < max_intentos:\n"
            "    # ...\n"
            "    if usuario in USUARIOS and USUARIOS[usuario] == clave:\n"
            "        print(f'BIENVENIDO, {usuario.upper()}')\n"
            "        acceso = True\n"
            "        break\n"
            "    else:\n"
            "        print(f'CLAVE INCORRECTA. Intentos restantes: {restantes}')\n"
            "\n"
            "if not acceso:\n"
            "    print('ACCESO DENEGADO. SISTEMA BLOQUEADO.')"
        ),
        "theory_content": SPEC_C50,
        "hints_json": json.dumps([
            (
                "Usa 'usuario in USUARIOS and USUARIOS[usuario] == clave' "
                "para verificar las credenciales en una sola condición."
            ),
            (
                "Si el acceso es exitoso: print(f'BIENVENIDO, {usuario.upper()}'), "
                "cambia acceso = True y ejecuta break para salir del while."
            ),
            (
                "El mensaje de bloqueo va FUERA del while con: if not acceso: "
                "print('ACCESO DENEGADO. SISTEMA BLOQUEADO.')"
            ),
        ]),
    },

    # ══════════════════════════════════════════════════════════════════════════
    # CONTRATO-60: Procesador de Datos
    # ══════════════════════════════════════════════════════════════════════════
    {
        "title": "CONTRATO-60: Procesador de Datos",
        "description": (
            "**CONTRATO DE CERTIFICACIÓN — SECTOR 06**\n\n"
            "El departamento de Recursos del Nexo necesita un módulo que analice "
            "la nómina de operadores y calcule el salario promedio del equipo "
            "para los reportes tácticos de presupuesto.\n\n"
            "**Tu misión:** Implementa `salario_promedio(empleados)` que reciba "
            "una lista de diccionarios y retorne el promedio de los salarios.\n\n"
            "**Estructura de cada empleado:**\n"
            "```python\n"
            '{"nombre": "Ana", "salario": 5000}\n'
            "```\n\n"
            "**Entrada:** `n` (número de empleados), luego `n` pares nombre/salario.\n\n"
            "**Salida:** El salario promedio como número flotante.\n\n"
            "Entradas: `4`, `Ana`, `5000`, `Bob`, `3500`, `Carlos`, `4200`, `Diana`, `7800`\n\n"
            "**Salida esperada:** `5125.0`"
        ),
        "difficulty_tier": DifficultyTier.ADVANCED,
        "difficulty": "expert",
        "sector_id": 7,
        "level_order": 70,
        "base_xp_reward": 1500,
        "is_project": True,
        "telemetry_goal_time": 720,
        "challenge_type": "python",
        "phase": "contrato",
        "concepts_taught_json": json.dumps([
            "def", "lista de diccionarios", "return float", "acumulador",
            "len()", "promedio", "parámetros complejos"
        ]),
        "initial_code": (
            "# ╔══════════════════════════════════════════════════════╗\n"
            "# ║  CONTRATO-60: PROCESADOR DE DATOS                   ║\n"
            "# ║  Dificultad: EXPERT — Proyecto de Certificación     ║\n"
            "# ╚══════════════════════════════════════════════════════╝\n"
            "#\n"
            "# Implementa salario_promedio(empleados).\n"
            "# Recibe lista de dicts {nombre, salario} → retorna promedio (float).\n"
            "\n"
            "def salario_promedio(empleados):\n"
            "    # Suma todos los salarios y divide entre el total de empleados\n"
            "    # Retorna el promedio como float\n"
            "    pass\n"
            "\n"
            "\n"
            "# ── No modificar lo de abajo ──\n"
            "n = int(input())\n"
            "lista = []\n"
            "for _ in range(n):\n"
            "    nombre  = input()\n"
            "    salario = int(input())\n"
            '    lista.append({"nombre": nombre, "salario": salario})\n'
            "\n"
            "print(salario_promedio(lista))\n"
        ),
        "expected_output": "5125.0",
        "test_inputs_json": json.dumps([
            "4",
            "Ana",    "5000",
            "Bob",    "3500",
            "Carlos", "4200",
            "Diana",  "7800",
        ]),
        "lore_briefing": (
            "El Nexo gestiona una fuerza de operadores altamente especializados. "
            "Cada ciclo táctico, el sistema de nómina genera un reporte con el salario promedio "
            "para verificar que el presupuesto asignado al sector está dentro de los parámetros. "
            "DAKI necesita que construyas el procesador de datos que automatice este cálculo. "
            "Un error en el promedio compromete la distribución de recursos de todo el sector."
        ),
        "pedagogical_objective": (
            "Contrato integrador de Sectores 01-06. Implementar una función que procesa "
            "una lista de diccionarios, extrae valores por clave, acumula y calcula promedio. "
            "Evalúa: def + parámetros complejos, dict access, acumulador, return float."
        ),
        "syntax_hint": (
            "def salario_promedio(empleados):\n"
            "    total = 0\n"
            "    for emp in empleados:\n"
            '        total += emp["salario"]\n'
            "    return total / len(empleados)"
        ),
        "theory_content": SPEC_C60,
        "hints_json": json.dumps([
            (
                'Accede al salario de cada empleado con emp["salario"] '
                "dentro del for que recorre la lista."
            ),
            (
                "Acumula en total con total += emp[\"salario\"]. "
                "Al final del for (fuera del bucle), return total / len(empleados)."
            ),
            (
                "La división / siempre retorna float en Python 3. "
                "No necesitas conversión — return total / len(empleados) da el resultado correcto."
            ),
        ]),
    },

    # ══════════════════════════════════════════════════════════════════════════
    # CONTRATO-70: Calculadora de Daño Táctico
    # ══════════════════════════════════════════════════════════════════════════
    {
        "title": "CONTRATO-70: Calculadora de Daño Táctico",
        "description": (
            "**CONTRATO DE CERTIFICACIÓN — SECTOR 07**\n\n"
            "El sistema de combate del Nexo necesita un motor de cálculo de daño "
            "que tenga en cuenta el tipo de arma y las defensas del objetivo. "
            "Cada arma tiene un daño base y un multiplicador que determinan su potencia real.\n\n"
            "**Tu misión:** Implementa `calcular_dano(tipo_ataque, nivel_defensa)` "
            "usando la tabla de modificadores predefinida.\n\n"
            "**Tabla de modificadores:**\n"
            "```\n"
            "LASER   → base: 100, mult: 1.5\n"
            "PLASMA  → base: 80,  mult: 2.0\n"
            "KINETIC → base: 120, mult: 1.2\n"
            "```\n\n"
            "**Fórmula:** `round(base * mult - nivel_defensa * 0.5)`\n\n"
            "Si el tipo de ataque no existe, retorna `0`.\n\n"
            "**Entradas de prueba:** `PLASMA`, `30`\n\n"
            "**Salida esperada:** `145`\n"
            "*(80 × 2.0 − 30 × 0.5 = 160 − 15 = 145)*"
        ),
        "difficulty_tier": DifficultyTier.ADVANCED,
        "difficulty": "expert",
        "sector_id": 8,
        "level_order": 80,
        "base_xp_reward": 2000,
        "is_project": True,
        "telemetry_goal_time": 900,
        "challenge_type": "python",
        "phase": "contrato",
        "concepts_taught_json": json.dumps([
            "def", "diccionario de modificadores", "return", "round()",
            "operadores matemáticos", "acceso condicional a dict", "lógica de juego"
        ]),
        "initial_code": (
            "# ╔══════════════════════════════════════════════════════╗\n"
            "# ║  CONTRATO-70: CALCULADORA DE DAÑO TÁCTICO           ║\n"
            "# ║  Dificultad: EXPERT — Proyecto de Certificación     ║\n"
            "# ╚══════════════════════════════════════════════════════╝\n"
            "#\n"
            "# Implementa calcular_dano(tipo_ataque, nivel_defensa).\n"
            "# Usa MODIFICADORES para obtener base y mult.\n"
            "# Fórmula: round(base * mult - nivel_defensa * 0.5)\n"
            "# Si tipo_ataque no existe en MODIFICADORES, retorna 0.\n"
            "\n"
            "MODIFICADORES = {\n"
            '    "LASER":   {"base": 100, "mult": 1.5},\n'
            '    "PLASMA":  {"base": 80,  "mult": 2.0},\n'
            '    "KINETIC": {"base": 120, "mult": 1.2},\n'
            "}\n"
            "\n"
            "def calcular_dano(tipo_ataque, nivel_defensa):\n"
            "    # 1. Verifica si tipo_ataque está en MODIFICADORES\n"
            "    # 2. Si no está, retorna 0\n"
            "    # 3. Si está, extrae base y mult\n"
            "    # 4. Calcula y retorna round(base * mult - nivel_defensa * 0.5)\n"
            "    pass\n"
            "\n"
            "\n"
            "# ── No modificar lo de abajo ──\n"
            "tipo    = input()\n"
            "defensa = int(input())\n"
            "print(calcular_dano(tipo, defensa))\n"
        ),
        "expected_output": "145",
        "test_inputs_json": json.dumps(["PLASMA", "30"]),
        "lore_briefing": (
            "El arsenal del Nexo cuenta con tres tipos de armamento de élite: "
            "el láser de precisión, el cañón de plasma de alto impacto y el impactador cinético pesado. "
            "Cada arma interactúa diferente con los escudos defensivos del enemigo. "
            "DAKI necesita un motor de cálculo que aplique los modificadores correctos "
            "y determine el daño neto real para el sistema de combate táctico. "
            "Sin este módulo, el Nexo no puede calcular si un ataque será suficiente para penetrar "
            "las defensas enemigas antes de comprometer recursos."
        ),
        "pedagogical_objective": (
            "Contrato integrador de Sectores 01-07. Implementar una función que usa "
            "un diccionario de configuración como tabla de datos, accede condicionalmente, "
            "aplica fórmula matemática con round(), y retorna 0 como caso de error. "
            "Evalúa: def + return, dict lookup, guard clause, operaciones float, round()."
        ),
        "syntax_hint": (
            "def calcular_dano(tipo_ataque, nivel_defensa):\n"
            "    if tipo_ataque not in MODIFICADORES:\n"
            "        return 0\n"
            '    mod = MODIFICADORES[tipo_ataque]\n'
            '    return round(mod["base"] * mod["mult"] - nivel_defensa * 0.5)'
        ),
        "theory_content": SPEC_C70,
        "hints_json": json.dumps([
            (
                "Primero verifica si el tipo existe: if tipo_ataque not in MODIFICADORES: return 0. "
                "Este es el 'guard clause' — maneja el caso de error antes de seguir."
            ),
            (
                'Accede al modificador con: mod = MODIFICADORES[tipo_ataque]. '
                'Luego extrae: mod["base"] y mod["mult"].'
            ),
            (
                'Fórmula final: return round(mod["base"] * mod["mult"] - nivel_defensa * 0.5). '
                "round() sin segundo argumento redondea al entero más cercano."
            ),
        ]),
    },

    # ══════════════════════════════════════════════════════════════════════════
    # CONTRATO-130: Clasificador de Operadores  (OOP + Algoritmos)
    # ══════════════════════════════════════════════════════════════════════════
    {
        "title": "CONTRATO-130: Clasificador de Operadores",
        "description": (
            "**CONTRATO DE CERTIFICACIÓN — SECTOR 13**\n\n"
            "El Nexo necesita un sistema que identifique automáticamente al operador "
            "más eficiente de cualquier equipo táctico. Los operadores de élite tienen "
            "un multiplicador de eficiencia superior al personal estándar.\n\n"
            "**Tu misión:** Implementa la jerarquía de clases y la función de selección.\n\n"
            "**Clases requeridas:**\n"
            "- `Operador(nombre, nivel)` → `eficiencia()` retorna `nivel * 10`\n"
            "- `OperadorElite(Operador)` → override: `eficiencia()` retorna `nivel * 15`\n\n"
            "**Función requerida:**\n"
            "- `seleccionar_lider(equipo)` → retorna el **nombre** del más eficiente\n\n"
            "**Equipo de prueba:**\n"
            "```python\n"
            "equipo = [\n"
            '    Operador("VASQUEZ", 8),    # eficiencia = 80\n'
            '    OperadorElite("NOVA", 6),  # eficiencia = 90\n'
            '    Operador("ROOK", 10),      # eficiencia = 100\n'
            "]\n"
            "```\n\n"
            "**Salida esperada:**\n"
            "```\n"
            "ROOK\n"
            "100\n"
            "```"
        ),
        "difficulty_tier": DifficultyTier.ADVANCED,
        "difficulty": "expert",
        "sector_id": 14,
        "level_order": 140,
        "base_xp_reward": 3000,
        "is_project": True,
        "telemetry_goal_time": 1200,
        "challenge_type": "python",
        "phase": "contrato",
        "concepts_taught_json": json.dumps([
            "clases", "herencia", "override", "polimorfismo",
            "max() con key", "lambda", "type hints", "OOP"
        ]),
        "initial_code": (
            "# ╔══════════════════════════════════════════════════════╗\n"
            "# ║  CONTRATO-130: CLASIFICADOR DE OPERADORES            ║\n"
            "# ║  Dificultad: EXPERT — Proyecto de Certificación     ║\n"
            "# ╚══════════════════════════════════════════════════════╝\n"
            "#\n"
            "# Implementa Operador, OperadorElite y seleccionar_lider().\n"
            "\n"
            "\n"
            "class Operador:\n"
            "    def __init__(self, nombre: str, nivel: int) -> None:\n"
            "        # Almacena nombre y nivel como atributos de instancia\n"
            "        pass\n"
            "\n"
            "    def eficiencia(self) -> int:\n"
            "        # Retorna nivel * 10\n"
            "        pass\n"
            "\n"
            "\n"
            "class OperadorElite(Operador):\n"
            "    def eficiencia(self) -> int:\n"
            "        # Override: retorna nivel * 15  (bonus de élite)\n"
            "        pass\n"
            "\n"
            "\n"
            "def seleccionar_lider(equipo: list) -> str:\n"
            "    \"\"\"Retorna el nombre del operador con mayor eficiencia.\"\"\"\n"
            "    # Usa max() con key=lambda op: op.eficiencia()\n"
            "    # Retorna .nombre del ganador (string, no el objeto)\n"
            "    pass\n"
            "\n"
            "\n"
            "# ── No modificar lo de abajo ──\n"
            "equipo = [\n"
            '    Operador("VASQUEZ", 8),\n'
            '    OperadorElite("NOVA", 6),\n'
            '    Operador("ROOK", 10),\n'
            "]\n"
            "\n"
            "lider = seleccionar_lider(equipo)\n"
            "print(lider)\n"
            "print(max(op.eficiencia() for op in equipo))\n"
        ),
        "expected_output": "ROOK\n100",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El Nexo enfrenta una misión de infiltración de máxima complejidad. "
            "Para optimizar las probabilidades de éxito, el sistema de asignación táctica "
            "debe identificar automáticamente al operador más capaz del equipo disponible. "
            "Los Operadores de Élite tienen una ventaja de rendimiento sobre el personal estándar "
            "gracias a su entrenamiento especializado. DAKI necesita que construyas el clasificador "
            "que hará esta determinación de forma precisa y sin margen de error."
        ),
        "pedagogical_objective": (
            "Contrato integrador de Sectores 01-13. Evalúa OOP completa: definición de clase, "
            "__init__ con atributos de instancia, método de instancia, herencia, override de método, "
            "polimorfismo implícito (max() llama eficiencia() sin saber el tipo real). "
            "Combina con algoritmo: max() con key=lambda para selección óptima."
        ),
        "syntax_hint": (
            "class Operador:\n"
            "    def __init__(self, nombre: str, nivel: int) -> None:\n"
            "        self.nombre = nombre\n"
            "        self.nivel  = nivel\n"
            "    def eficiencia(self) -> int:\n"
            "        return self.nivel * 10\n"
            "\n"
            "class OperadorElite(Operador):\n"
            "    def eficiencia(self) -> int:\n"
            "        return self.nivel * 15\n"
            "\n"
            "def seleccionar_lider(equipo: list) -> str:\n"
            "    lider = max(equipo, key=lambda op: op.eficiencia())\n"
            "    return lider.nombre"
        ),
        "theory_content": SPEC_C130,
        "hints_json": json.dumps([
            (
                "En __init__ de Operador: self.nombre = nombre y self.nivel = nivel. "
                "OperadorElite hereda __init__ automáticamente — no lo repitas."
            ),
            (
                "OperadorElite solo necesita redefinir eficiencia(): return self.nivel * 15. "
                "Todo lo demás (nombre, nivel, __init__) lo hereda de Operador."
            ),
            (
                "seleccionar_lider: lider = max(equipo, key=lambda op: op.eficiencia()). "
                "Retorna lider.nombre — el string, no el objeto."
            ),
        ]),
    },

    # ══════════════════════════════════════════════════════════════════════════
    # CONTRATO-175: Procesador Táctico  (Design Patterns + Testing)
    # ══════════════════════════════════════════════════════════════════════════
    {
        "title": "CONTRATO-175: Procesador Táctico",
        "description": (
            "**CONTRATO DE CERTIFICACIÓN — SECTOR 17**\n\n"
            "El sistema de análisis del Nexo necesita un procesador flexible que pueda "
            "cambiar su estrategia de ordenamiento en tiempo de ejecución sin reescribir "
            "el código principal. La solución debe seguir el patrón Strategy e incluir "
            "un test integrado que valide el comportamiento.\n\n"
            "**Tu misión:** Implementa el patrón Strategy con Protocol y un test real.\n\n"
            "**Clases requeridas:**\n"
            "- `EstrategiaOrden` (Protocol) — interfaz con `ordenar(datos) -> list[int]`\n"
            "- `OrdenAscendente` — implementación ascendente\n"
            "- `OrdenDescendente` — implementación descendente\n"
            "- `ProcesadorTactico` — composición + `cambiar_estrategia()`\n\n"
            "**Función de test requerida:**\n"
            "- `test_procesador()` — al menos 2 `assert`, retorna `True`\n\n"
            "**Datos de prueba:** `[42, 7, 15, 99, 23]`\n\n"
            "**Salida esperada:**\n"
            "```\n"
            "7 15 23 42 99\n"
            "99 42 23 15 7\n"
            "TEST: OK\n"
            "```"
        ),
        "difficulty_tier": DifficultyTier.ADVANCED,
        "difficulty": "expert",
        "sector_id": 18,
        "level_order": 185,
        "base_xp_reward": 4000,
        "is_project": True,
        "telemetry_goal_time": 1800,
        "challenge_type": "python",
        "phase": "contrato",
        "concepts_taught_json": json.dumps([
            "Strategy pattern", "Protocol", "composición", "type hints",
            "assert", "testing", "inyección de dependencia", "sorted()"
        ]),
        "initial_code": (
            "# ╔══════════════════════════════════════════════════════╗\n"
            "# ║  CONTRATO-175: PROCESADOR TÁCTICO                   ║\n"
            "# ║  Dificultad: EXPERT — Proyecto de Certificación     ║\n"
            "# ╚══════════════════════════════════════════════════════╝\n"
            "#\n"
            "# Implementa el patrón Strategy con Protocol.\n"
            "# Incluye test_procesador() con assert reales.\n"
            "\n"
            "from typing import Protocol\n"
            "\n"
            "\n"
            "class EstrategiaOrden(Protocol):\n"
            "    def ordenar(self, datos: list[int]) -> list[int]: ...\n"
            "\n"
            "\n"
            "class OrdenAscendente:\n"
            "    def ordenar(self, datos: list[int]) -> list[int]:\n"
            "        # Retorna la lista ordenada de menor a mayor\n"
            "        pass\n"
            "\n"
            "\n"
            "class OrdenDescendente:\n"
            "    def ordenar(self, datos: list[int]) -> list[int]:\n"
            "        # Retorna la lista ordenada de mayor a menor\n"
            "        pass\n"
            "\n"
            "\n"
            "class ProcesadorTactico:\n"
            "    def __init__(self, estrategia: EstrategiaOrden) -> None:\n"
            "        # Almacena la estrategia como atributo privado\n"
            "        pass\n"
            "\n"
            "    def cambiar_estrategia(self, estrategia: EstrategiaOrden) -> None:\n"
            "        # Reemplaza la estrategia actual\n"
            "        pass\n"
            "\n"
            "    def procesar(self, datos: list[int]) -> str:\n"
            "        # Aplica la estrategia y retorna los números separados por espacio\n"
            '        # Ejemplo: [7, 15, 23] → "7 15 23"\n'
            "        pass\n"
            "\n"
            "\n"
            "def test_procesador() -> bool:\n"
            "    # Test 1: orden ascendente\n"
            "    proc = ProcesadorTactico(OrdenAscendente())\n"
            '    assert proc.procesar([5, 1, 3]) == "1 3 5", "FALLA: ascendente"\n'
            "    # Test 2: cambio de estrategia a descendente\n"
            "    proc.cambiar_estrategia(OrdenDescendente())\n"
            '    assert proc.procesar([5, 1, 3]) == "5 3 1", "FALLA: descendente"\n'
            "    return True\n"
            "\n"
            "\n"
            "# ── No modificar lo de abajo ──\n"
            "datos = [42, 7, 15, 99, 23]\n"
            "proc = ProcesadorTactico(OrdenAscendente())\n"
            "print(proc.procesar(datos))\n"
            "proc.cambiar_estrategia(OrdenDescendente())\n"
            "print(proc.procesar(datos))\n"
            'print("TEST:", "OK" if test_procesador() else "FALLA")\n'
        ),
        "expected_output": "7 15 23 42 99\n99 42 23 15 7\nTEST: OK",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El sistema de inteligencia del Nexo procesa streams de datos críticos en tiempo real. "
            "El problema: diferentes misiones requieren diferentes ordenamientos — "
            "a veces prioridad ascendente, a veces descendente según la amenaza. "
            "Reescribir el procesador para cada caso sería insostenible en producción. "
            "DAKI necesita que construyas un sistema flexible con intercambio de estrategias en caliente, "
            "respaldado por tests que garanticen que el cambio de estrategia funcione sin efectos secundarios."
        ),
        "pedagogical_objective": (
            "Contrato integrador de Sectores 01-17. Evalúa diseño de software avanzado: "
            "patrón Strategy con Protocol como contrato de interfaz, composición sobre herencia, "
            "inyección de dependencia en __init__, cambio de comportamiento en runtime. "
            "Introduce testing con assert como práctica profesional básica."
        ),
        "syntax_hint": (
            "class OrdenAscendente:\n"
            "    def ordenar(self, datos: list[int]) -> list[int]:\n"
            "        return sorted(datos)\n"
            "\n"
            "class ProcesadorTactico:\n"
            "    def __init__(self, estrategia: EstrategiaOrden) -> None:\n"
            "        self._estrategia = estrategia\n"
            "    def cambiar_estrategia(self, estrategia: EstrategiaOrden) -> None:\n"
            "        self._estrategia = estrategia\n"
            "    def procesar(self, datos: list[int]) -> str:\n"
            '        return " ".join(str(x) for x in self._estrategia.ordenar(datos))'
        ),
        "theory_content": SPEC_C175,
        "hints_json": json.dumps([
            (
                "OrdenAscendente: return sorted(datos). "
                "OrdenDescendente: return sorted(datos, reverse=True). "
                "sorted() nunca muta la lista original — siempre retorna una nueva."
            ),
            (
                "ProcesadorTactico.__init__: self._estrategia = estrategia. "
                "cambiar_estrategia: self._estrategia = estrategia. "
                "El underscore indica atributo privado por convención."
            ),
            (
                'procesar: resultado = self._estrategia.ordenar(datos). '
                'Luego: return " ".join(str(x) for x in resultado). '
                "Esto convierte [7, 15, 23] → \"7 15 23\"."
            ),
        ]),
    },
]


# ─── Lógica de población ──────────────────────────────────────────────────────

async def seed() -> None:
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    async with SessionLocal() as session:
        # Idempotente: elimina SOLO los 5 contratos por (sector_id, level_order)
        # NO elimina por sector_id completo para no destruir los challenges regulares
        # de S5 (L41-49), S6 (L51-59) y S7 (L61-69).
        contrato_keys = [(6, 60), (7, 70), (8, 80), (14, 140), (18, 185)]
        deleted_count = 0
        for sid, lo in contrato_keys:
            result = await session.execute(
                delete(Challenge).where(
                    Challenge.sector_id == sid,
                    Challenge.level_order == lo,
                )
            )
            deleted_count += result.rowcount
        await session.flush()
        print(f"🧹  Contratos anteriores eliminados — {deleted_count} challenge(s) removidos.")

        print(f"\n🌱  Insertando {len(CONTRATOS)} Contratos de Certificación...\n")
        for data in CONTRATOS:
            challenge = Challenge(**data)
            session.add(challenge)
            print(
                f"    [Contrato {data['level_order']:03d}] {data['title']:<45} "
                f"({data['difficulty'].upper()}, {data['base_xp_reward']} XP, "
                f"~{data['telemetry_goal_time']}s) ★ CONTRATO"
            )

        await session.commit()

    await engine.dispose()
    print(f"\n✅  {len(CONTRATOS)} Contratos cargados.")
    print("    Los Contratos 50, 60, 70, 130 y 175 están disponibles para certificación.\n")


if __name__ == "__main__":
    asyncio.run(seed())
