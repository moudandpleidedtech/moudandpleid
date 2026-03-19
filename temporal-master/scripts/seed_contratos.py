"""
Seed — CONTRATOS: Proyectos Finales de Certificación (niveles 50, 60, 70).

Uso (desde la raíz del proyecto):
    python -m scripts.seed_contratos

Comportamiento:
    1. Elimina solo los challenges con sector_id IN (5, 6, 7) (idempotente).
    2. Inserta los 3 contratos de dificultad EXPERT, uno por sector.

Contratos:
    50 — Sector 05 — Terminal de Acceso    (login con 3 intentos, while + dict)
    60 — Sector 06 — Procesador de Datos   (función + lista de dicts, salario promedio)
    70 — Sector 07 — Calculadora de Daño   (función + dict de modificadores matemáticos)

test_validacion: el script de validación interna de cada contrato se almacena
en theory_content como documentación técnica para el evaluador y el operador.
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
        "sector_id": 5,
        "level_order": 50,
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
        "sector_id": 6,
        "level_order": 60,
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
        "sector_id": 7,
        "level_order": 70,
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
]


# ─── Lógica de población ──────────────────────────────────────────────────────

async def seed() -> None:
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    async with SessionLocal() as session:
        # Idempotente: elimina sectores 5, 6, 7
        from sqlalchemy import or_
        deleted = await session.execute(
            delete(Challenge).where(
                Challenge.sector_id.in_([5, 6, 7])
            )
        )
        deleted_count = deleted.rowcount
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
    print("    Los Contratos 50, 60 y 70 están disponibles para certificación.\n")


if __name__ == "__main__":
    asyncio.run(seed())
