"""
seed_sector_10.py — Sector 09: Resiliencia (try/except)
========================================================
Niveles 81–90  |  10 misiones  |  Sector ID = 9

Temática técnica: Manejo de excepciones, bloques try/except/else/finally,
                  excepciones personalizadas y patrones defensivos.

Lore DAKI: "Escudos de Energía" (81–85) y "Protocolo de Resiliencia" (86–90).

Nivel 90 (Boss): Analizador de logs con try/except que no crashea ante
                 datos malformados.

Notas de sandbox:
  • Las clases de excepción estándar (ValueError, TypeError, etc.)
    están en el whitelist desde Prompt 31.
  • Las excepciones personalizadas (`class ErrorNexo(Exception)`) funcionan
    con __build_class__ también añadido en Prompt 31.
  • `open()` no está en el whitelist — los "archivos" se simulan con
    strings multilínea procesadas con splitlines().

Uso standalone:
    python -m scripts.seed_sector_10
    python -m scripts.seed_sector_10 --dry-run
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings
from app.models.challenge import Challenge, DifficultyTier


# ─────────────────────────────────────────────────────────────────────────────
# Textos de teoría reutilizables
# ─────────────────────────────────────────────────────────────────────────────

THEORY_TRY_BASIC = """\
## try / except básico

El bloque `try` intenta ejecutar código que puede fallar.
Si ocurre un error, `except` lo captura y el programa continúa:

```python
try:
    resultado = 10 / 0
except:
    print("ERROR CAPTURADO")
```

Sin `try/except`, `ZeroDivisionError` detendría el programa.
Con `try/except`, se captura el error y se maneja de forma controlada.
"""

THEORY_EXCEPT_SPECIFIC = """\
## except con tipo específico

Es buena práctica especificar qué tipo de excepción capturar:

```python
try:
    numero = int("NEXO")
except ValueError:
    print("CONVERSION FALLIDA")
```

Si ocurre una excepción diferente a `ValueError`, NO será capturada
y el programa sí lanzará el error. Esto evita ocultar bugs.
"""

THEORY_EXCEPT_AS = """\
## except ... as e

Puedes capturar el objeto de excepción para ver su mensaje:

```python
try:
    lista = [1, 2, 3]
    print(lista[10])
except IndexError as e:
    print("IndexError capturado")
    print(str(e))
```

`str(e)` convierte el error en texto legible, útil para logging.
"""

THEORY_MULTIPLE_EXCEPT = """\
## Múltiples cláusulas except

Puedes manejar distintos tipos de error de forma diferente:

```python
def dividir(a, b):
    try:
        return a / b
    except ValueError:
        return "VALOR INVALIDO"
    except ZeroDivisionError:
        return "DIVISION POR CERO"
```

Python prueba cada `except` en orden y ejecuta el primero que coincida.
"""

THEORY_ELSE = """\
## try / except / else

El bloque `else` se ejecuta SOLO si no ocurrió ninguna excepción:

```python
try:
    numero = int("42")
except ValueError:
    print("Conversión fallida")
else:
    print(f"Conversion exitosa: {numero}")
```

`else` es útil para el código que depende de que `try` haya tenido éxito.
"""

THEORY_FINALLY = """\
## try / except / finally

El bloque `finally` se ejecuta SIEMPRE, haya o no excepción:

```python
try:
    resultado = 10 / 2
except ZeroDivisionError:
    resultado = 0
finally:
    print("Protocolo finalizado")
```

`finally` es útil para limpiar recursos (cerrar conexiones, etc.)
independientemente del resultado.
"""

THEORY_RAISE = """\
## raise — lanzar excepciones

Puedes lanzar excepciones manualmente con `raise`:

```python
def validar_hp(hp):
    if hp < 0:
        raise ValueError("HP no puede ser negativo")
    return hp

try:
    validar_hp(-10)
except ValueError as e:
    print(str(e))
```

`raise` interrumpe la función y el `except` del llamador lo captura.
"""

THEORY_CUSTOM_EXCEPTION = """\
## Excepciones personalizadas

Puedes crear tus propias excepciones heredando de `Exception`:

```python
class ErrorNexo(Exception):
    pass

def verificar_clave(clave):
    if clave != "NEXO-7":
        raise ErrorNexo("Clave de acceso inválida")

try:
    verificar_clave("HACK")
except ErrorNexo as e:
    print(str(e))
```

Las excepciones personalizadas hacen el código más expresivo y permiten
capturar solo errores del dominio del negocio.
"""

THEORY_DEFENSIVE = """\
## Programación defensiva con try/except

Una función defensiva devuelve un valor especial en lugar de crashear:

```python
def convertir(valor):
    try:
        return int(valor)
    except (ValueError, TypeError):
        return None

datos = ["42", "ERROR", "7", "X", "15"]
validos = [convertir(d) for d in datos]
validos = [v for v in validos if v is not None]
print(validos)   # [42, 7, 15]
```

Este patrón es común en parsers y procesadores de datos reales.
"""

THEORY_LOG_ANALYZER = """\
## Analizador de logs resiliente

Un analizador de logs robusto nunca crashea ante datos malformados:

```python
log = \"\"\"HP:45
CORRUPTO
MP:30\"\"\"

for linea in log.splitlines():
    try:
        clave, valor = linea.split(":")
        print(f"{clave} = {int(valor)}")
    except (ValueError, KeyError):
        print(f"Linea ignorada: {linea}")
```

`splitlines()` convierte un string multilínea en una lista de líneas,
simulando la lectura de un archivo sin necesitar `open()`.
"""


# ─────────────────────────────────────────────────────────────────────────────
# Catálogo de misiones
# ─────────────────────────────────────────────────────────────────────────────

SECTOR_10: list[dict] = [
    # ── Nivel 81 ─────────────────────────────────────────────────────────────
    {
        "sector_id": 10,
        "level_order": 91,
        "title":       "El Primer Escudo",
        "description": (
            "Envuelve `resultado = 10 // 0` en un `try/except` genérico.\n"
            "Si hay error, imprime exactamente:\n\n"
            "```\nERROR CAPTURADO\n```"
        ),
        "difficulty_tier":       DifficultyTier.BEGINNER,
        "difficulty":            "easy",
        "base_xp_reward":        120,
        "is_project":            False,
        "telemetry_goal_time":   180,
        "challenge_type":        "code",
        "phase":                 "teoria",
        "concepts_taught_json":  ["try", "except", "ZeroDivisionError", "error_generico"],
        "initial_code": (
            "try:\n"
            "    resultado = 10 // 0\n"
            "except:\n"
            "    # Imprime el mensaje de error\n"
            "    pass\n"
        ),
        "expected_output":       "ERROR CAPTURADO",
        "test_inputs_json":      [],
        "strict_match":          True,
        "lore_briefing": (
            "DAKI — Escudos de Energía v1\n\n"
            "El sistema detectó una operación inválida que podría crashear el protocolo.\n"
            "Activa el escudo try/except para contener el daño."
        ),
        "pedagogical_objective": "Introducir el bloque try/except como mecanismo de captura de errores.",
        "syntax_hint":           "Dentro del `except:`, escribe `print(\"ERROR CAPTURADO\")`.",
        "theory_content":        THEORY_TRY_BASIC,
        "hints_json": [
            "`10 // 0` lanza `ZeroDivisionError`.",
            "Un `except:` sin tipo captura cualquier excepción.",
            "El código dentro de `except` se ejecuta solo cuando hay error.",
        ],
        "grid_map_json": None,
    },

    # ── Nivel 82 ─────────────────────────────────────────────────────────────
    {
        "sector_id": 10,
        "level_order": 92,
        "title":       "Conversión Blindada",
        "description": (
            "Intenta convertir el string `\"NEXO\"` a entero con `int()`.\n"
            "Captura específicamente `ValueError` e imprime:\n\n"
            "```\nCONVERSION FALLIDA\n```"
        ),
        "difficulty_tier":       DifficultyTier.BEGINNER,
        "difficulty":            "easy",
        "base_xp_reward":        130,
        "is_project":            False,
        "telemetry_goal_time":   200,
        "challenge_type":        "code",
        "phase":                 "teoria",
        "concepts_taught_json":  ["ValueError", "except_especifico", "int_conversion"],
        "initial_code": (
            "try:\n"
            "    numero = int(\"NEXO\")\n"
            "except ValueError:\n"
            "    # Imprime el mensaje\n"
            "    pass\n"
        ),
        "expected_output":       "CONVERSION FALLIDA",
        "test_inputs_json":      [],
        "strict_match":          True,
        "lore_briefing": (
            "DAKI — Decodificador de Señales\n\n"
            "El decodificador recibió datos corruptos que no se pueden convertir a número.\n"
            "Usa `except ValueError` para manejar el fallo específico."
        ),
        "pedagogical_objective": "Practicar captura específica de ValueError en conversiones de tipo.",
        "syntax_hint":           "`except ValueError:` captura solo errores de conversión.",
        "theory_content":        THEORY_EXCEPT_SPECIFIC,
        "hints_json": [
            "`int(\"NEXO\")` lanza `ValueError` porque no es un número válido.",
            "Usa `except ValueError:` en lugar de `except:` genérico.",
            "Dentro del except, escribe `print(\"CONVERSION FALLIDA\")`.",
        ],
        "grid_map_json": None,
    },

    # ── Nivel 83 ─────────────────────────────────────────────────────────────
    {
        "sector_id": 10,
        "level_order": 93,
        "title":       "Captura con Mensaje",
        "description": (
            "Intenta acceder a `lista[10]` donde `lista = [10, 20, 30]`.\n"
            "Captura el `IndexError` con `as e` e imprime:\n\n"
            "```\nIndexError capturado\nlist index out of range\n```"
        ),
        "difficulty_tier":       DifficultyTier.BEGINNER,
        "difficulty":            "easy",
        "base_xp_reward":        140,
        "is_project":            False,
        "telemetry_goal_time":   210,
        "challenge_type":        "code",
        "phase":                 "teoria",
        "concepts_taught_json":  ["IndexError", "except_as", "str_excepcion"],
        "initial_code": (
            "lista = [10, 20, 30]\n"
            "try:\n"
            "    print(lista[10])\n"
            "except IndexError as e:\n"
            "    # Imprime el aviso y el mensaje del error\n"
            "    pass\n"
        ),
        "expected_output":       "IndexError capturado\nlist index out of range",
        "test_inputs_json":      [],
        "strict_match":          True,
        "lore_briefing": (
            "DAKI — Registro de Fallos\n\n"
            "El sistema de telemetría accedió a un índice fuera de rango.\n"
            "Captura el error y registra el mensaje exacto para el diagnóstico."
        ),
        "pedagogical_objective": "Aprender a usar 'except ExcType as e' para inspeccionar el mensaje de la excepción.",
        "syntax_hint":           "`print(str(e))` muestra el mensaje de la excepción.",
        "theory_content":        THEORY_EXCEPT_AS,
        "hints_json": [
            "`except IndexError as e:` guarda el objeto de excepción en `e`.",
            "Usa `str(e)` para convertir el error en texto legible.",
            "Primero imprime 'IndexError capturado', luego `str(e)`.",
        ],
        "grid_map_json": None,
    },

    # ── Nivel 84 ─────────────────────────────────────────────────────────────
    {
        "sector_id": 10,
        "level_order": 94,
        "title":       "Múltiples Escudos",
        "description": (
            "Implementa `calcular_division(a, b)` que:\n"
            "- Intenta retornar `a / b`\n"
            "- Si `b` no es número: retorna `\"VALOR INVALIDO\"`\n"
            "- Si `b == 0`: retorna `\"DIVISION POR CERO\"`\n\n"
            "Llama la función con `(100, 4)`, `(100, \"X\")` y `(100, 0)`:\n\n"
            "```\n25.0\nVALOR INVALIDO\nDIVISION POR CERO\n```"
        ),
        "difficulty_tier":       DifficultyTier.BEGINNER,
        "difficulty":            "medium",
        "base_xp_reward":        160,
        "is_project":            False,
        "telemetry_goal_time":   250,
        "challenge_type":        "code",
        "phase":                 "practica",
        "concepts_taught_json":  ["multiple_except", "TypeError", "ZeroDivisionError", "funcion_defensiva"],
        "initial_code": (
            "def calcular_division(a, b):\n"
            "    try:\n"
            "        return a / b\n"
            "    except TypeError:\n"
            "        return \"VALOR INVALIDO\"\n"
            "    except ZeroDivisionError:\n"
            "        return \"DIVISION POR CERO\"\n"
            "\n"
            "print(calcular_division(100, 4))\n"
            "print(calcular_division(100, \"X\"))\n"
            "print(calcular_division(100, 0))\n"
        ),
        "expected_output":       "25.0\nVALOR INVALIDO\nDIVISION POR CERO",
        "test_inputs_json":      [],
        "strict_match":          True,
        "lore_briefing": (
            "DAKI — Calculadora Táctica\n\n"
            "La calculadora de daño recibe distintos tipos de entrada errónea.\n"
            "Cada tipo de error necesita su propio manejador."
        ),
        "pedagogical_objective": "Practicar múltiples cláusulas except para diferentes tipos de error.",
        "syntax_hint":           "Cada `except` maneja un tipo diferente. El orden importa.",
        "theory_content":        THEORY_MULTIPLE_EXCEPT,
        "hints_json": [
            "`100 / \"X\"` lanza `TypeError` (operación con tipo incorrecto).",
            "`100 / 0` lanza `ZeroDivisionError`.",
            "Python ejecuta el primer `except` que coincida con el tipo de error.",
        ],
        "grid_map_json": None,
    },

    # ── Nivel 85 ─────────────────────────────────────────────────────────────
    {
        "sector_id": 10,
        "level_order": 95,
        "title":       "else: El Escudo Inteligente",
        "description": (
            "Usa `try/except/else` para convertir `\"42\"` a entero.\n"
            "Si la conversión falla: `\"Conversion fallida\"`.\n"
            "Si tiene éxito (bloque `else`): `\"Conversion exitosa: 42\"`.\n\n"
            "```\nConversion exitosa: 42\n```"
        ),
        "difficulty_tier":       DifficultyTier.BEGINNER,
        "difficulty":            "medium",
        "base_xp_reward":        160,
        "is_project":            False,
        "telemetry_goal_time":   230,
        "challenge_type":        "code",
        "phase":                 "practica",
        "concepts_taught_json":  ["try_except_else", "else_en_try", "control_flujo"],
        "initial_code": (
            "texto = \"42\"\n"
            "try:\n"
            "    numero = int(texto)\n"
            "except ValueError:\n"
            "    print(\"Conversion fallida\")\n"
            "else:\n"
            "    # Solo se ejecuta si no hubo excepción\n"
            "    pass\n"
        ),
        "expected_output":       "Conversion exitosa: 42",
        "test_inputs_json":      [],
        "strict_match":          True,
        "lore_briefing": (
            "DAKI — Validación de Señal\n\n"
            "El escudo inteligente distingue entre éxito y fallo.\n"
            "`else` activa el protocolo de confirmación solo cuando la señal es válida."
        ),
        "pedagogical_objective": "Entender el rol del bloque else en try/except: se ejecuta solo sin errores.",
        "syntax_hint":           "En el `else:`, escribe `print(f\"Conversion exitosa: {numero}\")`.",
        "theory_content":        THEORY_ELSE,
        "hints_json": [
            "`else` solo se ejecuta cuando NO hay ninguna excepción en `try`.",
            "La variable `numero` está disponible en el bloque `else`.",
            "Usa un f-string: `f\"Conversion exitosa: {numero}\"`.",
        ],
        "grid_map_json": None,
    },

    # ── Nivel 86 ─────────────────────────────────────────────────────────────
    {
        "sector_id": 10,
        "level_order": 96,
        "title":       "finally: Protocolo de Cierre",
        "description": (
            "Calcula `10 / 2` con `try/except/finally`.\n"
            "El `finally` siempre imprime `\"Protocolo finalizado\"`.\n\n"
            "```\n5.0\nProtocolo finalizado\n```"
        ),
        "difficulty_tier":       DifficultyTier.INTERMEDIATE,
        "difficulty":            "medium",
        "base_xp_reward":        170,
        "is_project":            False,
        "telemetry_goal_time":   240,
        "challenge_type":        "code",
        "phase":                 "practica",
        "concepts_taught_json":  ["finally", "try_except_finally", "cleanup"],
        "initial_code": (
            "try:\n"
            "    resultado = 10 / 2\n"
            "    print(resultado)\n"
            "except ZeroDivisionError:\n"
            "    print(\"Error de division\")\n"
            "finally:\n"
            "    # Siempre se ejecuta\n"
            "    pass\n"
        ),
        "expected_output":       "5.0\nProtocolo finalizado",
        "test_inputs_json":      [],
        "strict_match":          True,
        "lore_briefing": (
            "DAKI — Protocolo de Resiliencia\n\n"
            "El protocolo de cierre debe ejecutarse siempre, incluso en fallo.\n"
            "Usa `finally` para garantizar que el sistema se apaga de forma segura."
        ),
        "pedagogical_objective": "Aprender que finally se ejecuta siempre, útil para limpieza de recursos.",
        "syntax_hint":           "Dentro del `finally:`, escribe `print(\"Protocolo finalizado\")`.",
        "theory_content":        THEORY_FINALLY,
        "hints_json": [
            "`finally` se ejecuta siempre: haya excepción o no.",
            "En este caso, `10 / 2 = 5.0` no falla, pero `finally` igual se ejecuta.",
            "Orden de salida: primero `try` imprime 5.0, luego `finally` imprime el mensaje.",
        ],
        "grid_map_json": None,
    },

    # ── Nivel 87 ─────────────────────────────────────────────────────────────
    {
        "sector_id": 10,
        "level_order": 97,
        "title":       "raise: El Protocolo de Alerta",
        "description": (
            "Implementa `validar_hp(hp)` que lanza `ValueError` "
            "con el mensaje `\"HP no puede ser negativo\"` si `hp < 0`.\n\n"
            "Llámala con `-10` y captura el error:\n\n"
            "```\nHP no puede ser negativo\n```"
        ),
        "difficulty_tier":       DifficultyTier.INTERMEDIATE,
        "difficulty":            "medium",
        "base_xp_reward":        180,
        "is_project":            False,
        "telemetry_goal_time":   260,
        "challenge_type":        "code",
        "phase":                 "practica",
        "concepts_taught_json":  ["raise", "ValueError", "validacion", "patron_raise_catch"],
        "initial_code": (
            "def validar_hp(hp):\n"
            "    if hp < 0:\n"
            "        raise ValueError(\"HP no puede ser negativo\")\n"
            "    return hp\n"
            "\n"
            "try:\n"
            "    validar_hp(-10)\n"
            "except ValueError as e:\n"
            "    # Imprime el mensaje de error\n"
            "    pass\n"
        ),
        "expected_output":       "HP no puede ser negativo",
        "test_inputs_json":      [],
        "strict_match":          True,
        "lore_briefing": (
            "DAKI — Sistema de Validación Táctica\n\n"
            "El sistema no debe aceptar HP negativo como entrada válida.\n"
            "Usa `raise ValueError` para rechazar datos corruptos."
        ),
        "pedagogical_objective": "Entender raise como mecanismo de señalización de condiciones de error.",
        "syntax_hint":           "`raise ValueError(\"mensaje\")` — el mensaje se accede con `str(e)`.",
        "theory_content":        THEORY_RAISE,
        "hints_json": [
            "`raise ValueError(\"HP no puede ser negativo\")` lanza el error.",
            "El `except ValueError as e:` del llamador lo captura.",
            "`print(str(e))` imprime el mensaje exacto del error.",
        ],
        "grid_map_json": None,
    },

    # ── Nivel 88 ─────────────────────────────────────────────────────────────
    {
        "sector_id": 10,
        "level_order": 98,
        "title":       "Excepción Personalizada",
        "description": (
            "Define `class ErrorNexo(Exception): pass`.\n\n"
            "Implementa `verificar_clave(clave)` que lanza `ErrorNexo` "
            "con el mensaje `\"Clave de acceso inválida\"` si la clave no es `\"NEXO-7\"`.\n\n"
            "Llámala con `\"HACK\"` y muestra:\n\n"
            "```\nClave de acceso inválida\n```"
        ),
        "difficulty_tier":       DifficultyTier.INTERMEDIATE,
        "difficulty":            "medium",
        "base_xp_reward":        200,
        "is_project":            False,
        "telemetry_goal_time":   280,
        "challenge_type":        "code",
        "phase":                 "practica",
        "concepts_taught_json":  ["excepcion_personalizada", "herencia_Exception", "raise", "OOP_excepciones"],
        "initial_code": (
            "class ErrorNexo(Exception):\n"
            "    pass\n"
            "\n"
            "def verificar_clave(clave):\n"
            "    if clave != \"NEXO-7\":\n"
            "        raise ErrorNexo(\"Clave de acceso inválida\")\n"
            "\n"
            "try:\n"
            "    verificar_clave(\"HACK\")\n"
            "except ErrorNexo as e:\n"
            "    # Imprime el mensaje\n"
            "    pass\n"
        ),
        "expected_output":       "Clave de acceso inválida",
        "test_inputs_json":      [],
        "strict_match":          True,
        "lore_briefing": (
            "DAKI — Protocolo de Acceso Seguro\n\n"
            "El sistema rechaza claves no autorizadas con una excepción propia.\n"
            "Define `ErrorNexo` y úsala para señalizar acceso no autorizado."
        ),
        "pedagogical_objective": "Crear y usar excepciones personalizadas heredando de Exception.",
        "syntax_hint":           "`class ErrorNexo(Exception): pass` — luego `raise ErrorNexo(\"mensaje\")`.",
        "theory_content":        THEORY_CUSTOM_EXCEPTION,
        "hints_json": [
            "`class ErrorNexo(Exception): pass` crea la excepción personalizada.",
            "Se usa igual que las excepciones estándar: `raise ErrorNexo(\"mensaje\")`.",
            "`except ErrorNexo as e:` la captura; `print(str(e))` muestra el mensaje.",
        ],
        "grid_map_json": None,
    },

    # ── Nivel 89 ─────────────────────────────────────────────────────────────
    {
        "sector_id": 10,
        "level_order": 99,
        "title":       "Filtro Defensivo",
        "description": (
            "Implementa `convertir(valor)` que retorna `int(valor)` o `None` si falla.\n\n"
            "Filtra la lista `[\"42\", \"ERROR\", \"7\", \"X\", \"15\"]` y muestra "
            "solo los valores convertidos correctamente:\n\n"
            "```\n42\n7\n15\n```"
        ),
        "difficulty_tier":       DifficultyTier.INTERMEDIATE,
        "difficulty":            "medium",
        "base_xp_reward":        190,
        "is_project":            False,
        "telemetry_goal_time":   270,
        "challenge_type":        "code",
        "phase":                 "practica",
        "concepts_taught_json":  ["funcion_defensiva", "None_como_sentinel", "filter_none", "patron_defensivo"],
        "initial_code": (
            "def convertir(valor):\n"
            "    try:\n"
            "        return int(valor)\n"
            "    except (ValueError, TypeError):\n"
            "        return None\n"
            "\n"
            "datos = [\"42\", \"ERROR\", \"7\", \"X\", \"15\"]\n"
            "for d in datos:\n"
            "    resultado = convertir(d)\n"
            "    if resultado is not None:\n"
            "        print(resultado)\n"
        ),
        "expected_output":       "42\n7\n15",
        "test_inputs_json":      [],
        "strict_match":          True,
        "lore_briefing": (
            "DAKI — Limpieza de Datos Corruptos\n\n"
            "El feed de telemetría mezcla datos válidos con corruptos.\n"
            "El filtro defensivo extrae solo los valores útiles."
        ),
        "pedagogical_objective": "Usar try/except para devolver None en error y filtrar resultados válidos.",
        "syntax_hint":           "Captura `(ValueError, TypeError)` en un solo `except` con tupla.",
        "theory_content":        THEORY_DEFENSIVE,
        "hints_json": [
            "Retorna `None` en el `except` para indicar fallo silencioso.",
            "En el bucle, verifica `if resultado is not None:` antes de imprimir.",
            "Un `except` puede capturar múltiples tipos: `except (ValueError, TypeError):`.",
        ],
        "grid_map_json": None,
    },

    # ── Nivel 90 (BOSS) ───────────────────────────────────────────────────────
    {
        "sector_id": 10,
        "level_order": 100,
        "title":       "CONTRATO-90: Analizador de Logs",
        "description": (
            "**BOSS del Sector 09 — Proyecto completo**\n\n"
            "El sistema recibirá N líneas de log por `input()`. Cada línea tiene formato "
            "`CLAVE:VALOR` donde VALOR es un entero.\n"
            "Algunas líneas están corrompidas (no tienen `:` o el valor no es número).\n\n"
            "Tu analizador debe:\n"
            "1. Leer `n = int(input())` — número de líneas\n"
            "2. Por cada línea: usar `try/except` para parsear `CLAVE:VALOR`\n"
            "3. Si la línea es válida: sumar el valor al total\n"
            "4. Si la línea es inválida: incrementar contador de errores\n"
            "5. Al final imprimir: `\"Total: X\"` y `\"Errores: Y\"`\n\n"
            "**Test:**\n"
            "Entradas: `5`, `HP:45`, `MP:30`, `CORRUPTO`, `XP:70`, `NEXO:X`\n\n"
            "```\nTotal: 145\nErrores: 2\n```"
        ),
        "difficulty_tier":       DifficultyTier.ADVANCED,
        "difficulty":            "hard",
        "base_xp_reward":        500,
        "is_project":            True,
        "telemetry_goal_time":   600,
        "challenge_type":        "project",
        "phase":                 "proyecto",
        "concepts_taught_json":  ["try_except_integrado", "splitlines", "parseo_resiliente", "acumulador"],
        "initial_code": (
            "n = int(input())\n"
            "total  = 0\n"
            "errores = 0\n"
            "\n"
            "for _ in range(n):\n"
            "    linea = input()\n"
            "    try:\n"
            "        # Separa la línea en clave y valor\n"
            "        # Convierte el valor a int y acumula\n"
            "        pass\n"
            "    except (ValueError, IndexError):\n"
            "        errores += 1\n"
            "\n"
            "print(f\"Total: {total}\")\n"
            "print(f\"Errores: {errores}\")\n"
        ),
        "expected_output":       "Total: 145\nErrores: 2",
        "test_inputs_json":      ["5", "HP:45", "MP:30", "CORRUPTO", "XP:70", "NEXO:X"],
        "strict_match":          True,
        "lore_briefing": (
            "DAKI — CONTRATO-90: Protocolo Omega de Resiliencia\n\n"
            "El sistema de inteligencia táctica recibe logs de múltiples fuentes.\n"
            "Algunos feeds están corrompidos. El analizador nunca debe crashear —\n"
            "registra los errores y procesa lo que pueda. La misión del sector depende de esto."
        ),
        "pedagogical_objective": (
            "Integrar try/except con acumuladores, parseo de strings y lógica de conteo de errores "
            "en un programa completo robusto ante entradas malformadas."
        ),
        "syntax_hint":           '`clave, valor = linea.split(":")` — falla si no hay ":" → IndexError.',
        "theory_content": (
            "## Boss Sector 09: Analizador de Logs resiliente\n\n"
            "Flujo completo:\n"
            "```python\n"
            "n = int(input())\n"
            "total  = 0\n"
            "errores = 0\n"
            "for _ in range(n):\n"
            "    linea = input()\n"
            "    try:\n"
            "        clave, valor = linea.split(\":\")\n"
            "        total += int(valor)\n"
            "    except (ValueError, IndexError):\n"
            "        errores += 1\n"
            "print(f\"Total: {total}\")\n"
            "print(f\"Errores: {errores}\")\n"
            "```\n\n"
            "**¿Por qué dos tipos de excepción?**\n"
            "- `IndexError`: `linea.split(\":\")` devuelve solo un elemento → unpacking falla\n"
            "- `ValueError`: `int(valor)` falla si el valor no es número (p.ej. `\"X\"`)\n\n"
            "Con `except (ValueError, IndexError):` capturamos ambos casos en una sola línea."
        ),
        "hints_json": [
            '`linea.split(":")` divide en `["CLAVE", "VALOR"]`; `clave, valor = ...` hace unpacking.',
            'Si la línea no tiene ":", split devuelve un solo elemento y el unpacking lanza `ValueError`.',
            "Acumula: `total += int(valor)` dentro del `try`.",
            "En el `except (ValueError, IndexError):`, solo incrementa `errores += 1`.",
        ],
        "grid_map_json": None,
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# Seed standalone
# ─────────────────────────────────────────────────────────────────────────────

async def seed(dry_run: bool = False) -> None:
    print("\n" + "═" * 60)
    print("  ⚡ Seed Sector 09 — Resiliencia (try/except)")
    print("═" * 60)
    if dry_run:
        print("  MODE: DRY-RUN\n")

    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    SessionLocal = async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )

    async with SessionLocal() as session:
        try:
            if not dry_run:
                await session.execute(
                    delete(Challenge).where(Challenge.sector_id == 10)
                )
            for data in SECTOR_10:
                level_order = data.get("level_order")
                title = data.get("title", "?")
                if dry_run:
                    print(f"  [DRY] ➕  L{level_order:02d}  {title}")
                else:
                    session.add(Challenge(**data))
                    print(f"  ➕  L{level_order:02d}  {title}")
            if not dry_run:
                await session.commit()
                print(f"\n  💾  Commit OK — {len(SECTOR_10)} misiones insertadas.")
        except Exception as exc:
            if not dry_run:
                await session.rollback()
            print(f"  ❌  ERROR: {exc}")
            await engine.dispose()
            sys.exit(1)

    await engine.dispose()
    print("═" * 60 + "\n")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Seed Sector 09 — Resiliencia")
    p.add_argument("--dry-run", action="store_true")
    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()
    asyncio.run(seed(dry_run=args.dry_run))
