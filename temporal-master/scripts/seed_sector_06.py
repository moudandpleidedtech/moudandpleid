"""
Seed — SECTOR 06: Manipulación de Señales (9 niveles, IDs 41–49).

Uso (desde la raíz del proyecto):
    python -m scripts.seed_sector_06

Comportamiento:
    1. Elimina solo los challenges con sector_id=5 y level_order < 50 (preserva CONTRATO-50).
    2. Inserta los 9 niveles del Sector 05 con curva easy → medium → hard.
    3. El nivel 50 (Boss) vive en seed_contratos.py — no se toca aquí.

Temática técnica: slicing, .upper()/.lower()/.strip(), f-strings avanzados,
                  .replace(), .split(), .join(), .count()/.startswith(),
                  encadenamiento de métodos, ord()/chr() + Cifrado César.
Narrativa: desencriptación de comunicaciones enemigas, limpieza de logs corruptos.
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


# ─── Contenido teórico por nivel ─────────────────────────────────────────────

THEORY_N41 = """\
## PROTOCOLO: Strings como Secuencias — Slicing

Los strings son **secuencias de caracteres** que puedes indexar y "rebanar":

```python
codigo = "NEXO-ALFA-7"
print(codigo[0])      # 'N'   → primer carácter
print(codigo[-1])     # '7'   → último carácter
print(codigo[0:4])    # 'NEXO' → del índice 0 al 3 (4 excluido)
print(codigo[5:9])    # 'ALFA'
print(codigo[:4])     # 'NEXO' → desde el inicio
print(codigo[5:])     # 'ALFA-7' → hasta el final
```

**Sintaxis del slice:** `cadena[inicio:fin]`
- `inicio` es **inclusivo** (se incluye en el resultado)
- `fin` es **exclusivo** (no se incluye)
- Los índices negativos cuentan desde el final: `-1` es el último

---

## REGLA DE ORO

```
c o d i g o = "N E X O - A L F A - 7"
índice pos:    0 1 2 3 4 5 6 7 8 9 10
índice neg:  -11-10-9-8-7-6-5-4-3-2 -1
```
"""

THEORY_N42 = """\
## PROTOCOLO: Métodos de Transformación

Los strings tienen métodos integrados que devuelven **nuevas cadenas** transformadas:

| Método        | Efecto                               | Ejemplo                            |
|---------------|--------------------------------------|------------------------------------|
| `.upper()`    | Todo en MAYÚSCULAS                   | `"nexo".upper()` → `"NEXO"`        |
| `.lower()`    | Todo en minúsculas                   | `"NEXO".lower()` → `"nexo"`        |
| `.strip()`    | Elimina espacios del inicio y final  | `"  ok  ".strip()` → `"ok"`        |
| `.lstrip()`   | Solo elimina espacios a la izquierda | `"  ok  ".lstrip()` → `"ok  "`     |
| `.rstrip()`   | Solo elimina espacios a la derecha   | `"  ok  ".rstrip()` → `"  ok"`     |

---

## ENCADENAMIENTO DE MÉTODOS

Puedes aplicar varios métodos en cadena — se ejecutan de izquierda a derecha:

```python
log = "  Error Critico  "
limpio = log.strip().upper()
print(limpio)   # "ERROR CRITICO"
```

- Primero `.strip()` elimina los espacios → `"Error Critico"`
- Luego `.upper()` convierte a mayúsculas → `"ERROR CRITICO"`

Los métodos de string **no modifican** el original — siempre devuelven una nueva cadena.
"""

THEORY_N43 = """\
## PROTOCOLO: f-strings — Mensajes con Variables

Los **f-strings** permiten incrustar variables directamente en un string.
Se definen con la letra `f` antes de las comillas:

```python
sector = 5
operador = "Kira"
estado = "ACTIVO"

print(f"SECTOR {sector} | Operador: {operador} | Estado: {estado}")
# SECTOR 5 | Operador: Kira | Estado: ACTIVO
```

Cualquier expresión Python puede ir dentro de `{}`:

```python
hp = 75
print(f"HP: {hp}/100 ({hp}%)")        # HP: 75/100 (75%)
print(f"Daño total: {12 * 5}")        # Daño total: 60
print(f"{'ALTA' if hp > 50 else 'BAJA'}")   # ALTA
```

---

## FORMATO NUMÉRICO

```python
pi = 3.14159
print(f"Pi ≈ {pi:.2f}")   # Pi ≈ 3.14  → 2 decimales
print(f"{42:05d}")          # 00042      → relleno con ceros
```
"""

THEORY_N44 = """\
## PROTOCOLO: .replace() — Sustitución de Patrones

`.replace(antiguo, nuevo)` devuelve una **nueva cadena** con todas las apariciones
de `antiguo` reemplazadas por `nuevo`:

```python
log = "10-NULL-45-NULL-78"
limpio = log.replace("NULL", "0")
print(limpio)   # "10-0-45-0-78"
```

---

## PUNTOS CLAVE

- `.replace()` **no modifica** el string original — devuelve uno nuevo
- Reemplaza **todas** las apariciones por defecto
- Para reemplazar solo las primeras N, usa el tercer argumento:
  ```python
  texto = "ERROR ERROR ERROR"
  print(texto.replace("ERROR", "OK", 1))   # "OK ERROR ERROR"
  ```
- Si `nuevo` es `""`, equivale a **eliminar** el texto:
  ```python
  datos = "NEX---O"
  print(datos.replace("-", ""))   # "NEXO"
  ```
"""

THEORY_N45 = """\
## PROTOCOLO: .split() — Descomposición de Cadena

`.split(separador)` divide un string en una **lista** usando el separador indicado:

```python
señal = "ROJO,VERDE,AZUL"
partes = señal.split(",")
print(partes)        # ['ROJO', 'VERDE', 'AZUL']
print(partes[0])     # 'ROJO'
print(len(partes))   # 3
```

---

## SEPARADOR POR DEFECTO

Sin argumentos, `.split()` divide por espacios en blanco (incluyendo tabs y saltos de línea)
y elimina las partes vacías:

```python
frase = "  el   nexo   vive  "
print(frase.split())   # ['el', 'nexo', 'vive']
```

---

## COMBINACIÓN CON for

```python
ids = "A1,B2,C3"
for id_nodo in ids.split(","):
    print(f"Escaneando nodo {id_nodo}")
# Escaneando nodo A1
# Escaneando nodo B2
# Escaneando nodo C3
```
"""

THEORY_N46 = """\
## PROTOCOLO: .join() — Reconstrucción de Cadena

`.join(iterable)` une los elementos de una lista en un **único string**,
insertando el separador entre cada par:

```python
fragmentos = ["NEXO", "ALFA", "DELTA"]
resultado = " | ".join(fragmentos)
print(resultado)   # "NEXO | ALFA | DELTA"
```

**Sintaxis:** `separador.join(lista)`

El separador puede ser cualquier string:

```python
letras = ["N", "E", "X", "O"]
print("".join(letras))    # "NEXO"      → sin separador
print("-".join(letras))   # "N-E-X-O"  → guión
print(", ".join(letras))  # "N, E, X, O"
```

---

## split() Y join() SON INVERSAS

```python
original     = "A,B,C"
partes        = original.split(",")     # ['A', 'B', 'C']
reconstruido  = ",".join(partes)        # "A,B,C"
```
"""

THEORY_N47 = """\
## PROTOCOLO: Búsqueda en Strings

Python ofrece métodos para **detectar patrones** sin necesidad de bucles:

| Método              | Retorna  | Descripción                                  |
|---------------------|----------|----------------------------------------------|
| `.count(sub)`       | int      | Número de apariciones de `sub`               |
| `.find(sub)`        | int / -1 | Índice de la primera aparición (o -1)        |
| `.startswith(pre)`  | bool     | `True` si el string comienza con `pre`       |
| `.endswith(suf)`    | bool     | `True` si el string termina con `suf`        |
| `sub in cadena`     | bool     | `True` si `sub` aparece en `cadena`          |

---

## EJEMPLOS

```python
log = "CRITICO: ERROR en sector 3. ERROR en nodo 7."

print(log.count("ERROR"))         # 2
print(log.find("ERROR"))          # 9  (índice de la 1ra aparición)
print(log.startswith("CRITICO"))  # True
print(log.endswith("."))          # True
print("sector" in log)            # True
```
"""

THEORY_N48 = """\
## PROTOCOLO: Pipeline de Transformación

Las transformaciones de strings se pueden **encadenar** en secuencia:

```python
entrada = "  nexo alfa  "
resultado = entrada.strip().replace(" ", "_").upper()
print(resultado)   # "NEXO_ALFA"
```

Orden de ejecución (izquierda a derecha):
1. `.strip()` → elimina espacios extremos: `"nexo alfa"`
2. `.replace(" ", "_")` → reemplaza espacios internos: `"nexo_alfa"`
3. `.upper()` → convierte a mayúsculas: `"NEXO_ALFA"`

---

## PATRÓN: split → procesar → join

Dividir, transformar cada parte, y reconstruir:

```python
datos = "nexo,alfa,delta"
partes = datos.split(",")
resultado = "|".join([p.upper() for p in partes])
print(resultado)   # "NEXO|ALFA|DELTA"
```
"""

THEORY_N49 = """\
## PROTOCOLO: ord() y chr() — El Código de los Caracteres

Cada carácter tiene un número ASCII/Unicode. Python permite convertir entre ambos:

| Función      | Dirección         | Ejemplo                 |
|--------------|-------------------|-------------------------|
| `ord(c)`     | carácter → número | `ord('A')` → `65`       |
| `chr(n)`     | número → carácter | `chr(65)` → `'A'`       |

Las letras mayúsculas ocupan los códigos 65 (`A`) al 90 (`Z`).

---

## CIFRADO CÉSAR

El **Cifrado César** desplaza cada letra N posiciones en el alfabeto.
Para descifrar un mensaje cifrado con +3, resta 3 a cada letra:

```python
# Descifrar shift +3: restar 3 con wrap-around
cifrado = "QHAR"
resultado = ""
for c in cifrado:
    resultado += chr((ord(c) - ord('A') - 3) % 26 + ord('A'))
print(resultado)   # "NEXO"
```

- `ord(c) - ord('A')` convierte la letra a índice 0–25
- `% 26` permite el **wrap-around** (A−1 → Z)
- `+ ord('A')` convierte de vuelta a código ASCII

Verificación: Q(81)→N(78), H(72)→E(69), A(65)→X(88), R(82)→O(79)
"""


# ─── Niveles del Sector 05 ────────────────────────────────────────────────────

SECTOR_06 = [
    # ── NIVEL 41 — Slicing de cadenas ─────────────────────────────────────────
    {
        "title": "Fragmento Alfa",
        "description": (
            "El sistema de identificación del Nexo usa códigos en el formato "
            "`NEXO-ALFA-7`. Para el protocolo de autenticación solo son relevantes "
            "el prefijo y el número de versión.\n\n"
            "Dada la cadena `codigo = \"NEXO-ALFA-7\"`, imprime:\n"
            "1. Los primeros **4 caracteres** (`NEXO`)\n"
            "2. El **último carácter** (`7`)\n\n"
            "Salida esperada:\n"
            "```\nNEXO\n7\n```"
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "easy",
        "sector_id": 6,
        "level_order": 51,
        "base_xp_reward": 100,
        "is_project": False,
        "telemetry_goal_time": 90,
        "challenge_type": "python",
        "phase": "cadenas",
        "concepts_taught_json": json.dumps(["strings", "slicing", "índices", "índice negativo"]),
        "initial_code": (
            "# MISIÓN: Extrae los primeros 4 caracteres y el último\n"
            "\n"
            'codigo = "NEXO-ALFA-7"\n'
            "\n"
            "# Imprime los primeros 4 caracteres (slice)\n"
            "print(codigo[___:___])\n"
            "\n"
            "# Imprime el último carácter (índice negativo)\n"
            "print(codigo[___])\n"
        ),
        "expected_output": "NEXO\n7",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "Las comunicaciones del Nexo usan códigos de identificación compuestos. "
            "El protocolo Alpha solo necesita el prefijo y el número de versión. "
            "DAKI te enseña a extraer fragmentos precisos de una señal "
            "para que el sistema no procese datos innecesarios."
        ),
        "pedagogical_objective": (
            "Introducir strings como secuencias indexables. "
            "Slicing con [inicio:fin] e índices negativos para acceder al último elemento."
        ),
        "syntax_hint": "print(codigo[0:4])\nprint(codigo[-1])",
        "theory_content": THEORY_N41,
        "hints_json": json.dumps([
            "Los strings se indexan igual que las listas. codigo[0] es 'N', codigo[1] es 'E'.",
            "Para un rango usa [inicio:fin]. codigo[0:4] extrae del índice 0 al 3 (el 4 no se incluye).",
            "El índice -1 apunta siempre al último carácter. Solución: print(codigo[0:4]) y print(codigo[-1]).",
        ]),
        "strict_match": True,
    },
    # ── NIVEL 42 — .upper(), .lower(), .strip() ───────────────────────────────
    {
        "title": "Señal Corrupta",
        "description": (
            "Los sensores del Sector 05 reciben señales con ruido: espacios extra "
            "al principio y al final, y capitalización inconsistente. "
            "El sistema de análisis requiere señales normalizadas antes de procesarlas.\n\n"
            "Dada la señal `señal = \"  error de sistema  \"`, "
            "imprime el texto sin espacios extremos y en **MAYÚSCULAS**.\n\n"
            "Salida esperada:\n"
            "```\nERROR DE SISTEMA\n```"
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "easy",
        "sector_id": 6,
        "level_order": 52,
        "base_xp_reward": 100,
        "is_project": False,
        "telemetry_goal_time": 90,
        "challenge_type": "python",
        "phase": "cadenas",
        "concepts_taught_json": json.dumps([
            "strings", ".strip()", ".upper()", ".lower()", "encadenamiento de métodos"
        ]),
        "initial_code": (
            "# MISIÓN: Limpia la señal y conviértela a mayúsculas\n"
            "\n"
            'señal = "  error de sistema  "\n'
            "\n"
            "# Elimina espacios del inicio/final y convierte a mayúsculas\n"
            "print(señal.___().___())\n"
        ),
        "expected_output": "ERROR DE SISTEMA",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "Los logs de error del Nexo llegan con ruido de transmisión: "
            "espacios fantasma al principio y al final, y mezcla de mayúsculas y minúsculas. "
            "Antes de que el sistema de alerta los procese, deben ser normalizados. "
            "DAKI necesita que implementes el protocolo de limpieza de señal."
        ),
        "pedagogical_objective": (
            "Introducir .strip(), .upper(), .lower(). "
            "Practicar el encadenamiento de métodos (method chaining): "
            "cada método retorna un nuevo string sobre el que puedes seguir llamando métodos."
        ),
        "syntax_hint": "print(señal.strip().upper())",
        "theory_content": THEORY_N42,
        "hints_json": json.dumps([
            ".strip() elimina los espacios del inicio y del final del string.",
            ".upper() convierte todas las letras a mayúsculas.",
            "Encadena los dos métodos: señal.strip().upper() — strip primero, luego upper.",
        ]),
        "strict_match": True,
    },
    # ── NIVEL 43 — f-strings avanzados ────────────────────────────────────────
    {
        "title": "Reporte de Estado",
        "description": (
            "El módulo de comunicaciones del Nexo genera reportes de estado "
            "en un formato estandarizado para todos los puntos de acceso.\n\n"
            "Dadas las variables `sector = 5`, `operador = \"Kira\"` y "
            "`estado = \"ACTIVO\"`, imprime exactamente:\n\n"
            "```\nSECTOR 5 | Operador: Kira | Estado: ACTIVO\n```"
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "easy",
        "sector_id": 6,
        "level_order": 53,
        "base_xp_reward": 125,
        "is_project": False,
        "telemetry_goal_time": 100,
        "challenge_type": "python",
        "phase": "cadenas",
        "concepts_taught_json": json.dumps(["strings", "f-strings", "interpolación de variables"]),
        "initial_code": (
            "# MISIÓN: Genera el reporte de estado con el formato exacto\n"
            "\n"
            "sector = 5\n"
            'operador = "Kira"\n'
            'estado = "ACTIVO"\n'
            "\n"
            "# Imprime: 'SECTOR 5 | Operador: Kira | Estado: ACTIVO'\n"
            'print(f"___")\n'
        ),
        "expected_output": "SECTOR 5 | Operador: Kira | Estado: ACTIVO",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El comando central del Nexo exige que todos los reportes de estado "
            "lleguen en el mismo formato para poder ser procesados por el sistema de monitoreo. "
            "DAKI diseñó la plantilla. Tu misión: completar el módulo de formateo "
            "que toma las variables del sistema y produce el mensaje estándar."
        ),
        "pedagogical_objective": (
            "Usar f-strings para formatear mensajes con múltiples variables. "
            "Practicar el formato exacto con texto literal y separadores específicos."
        ),
        "syntax_hint": 'print(f"SECTOR {sector} | Operador: {operador} | Estado: {estado}")',
        "theory_content": THEORY_N43,
        "hints_json": json.dumps([
            "Un f-string empieza con f antes de las comillas: f\"texto {variable} texto\".",
            "Las variables van entre llaves {} dentro del f-string. El texto literal (como ' | ') va fuera.",
            'Solución: print(f"SECTOR {sector} | Operador: {operador} | Estado: {estado}")',
        ]),
        "strict_match": True,
    },
    # ── NIVEL 44 — .replace() ─────────────────────────────────────────────────
    {
        "title": "Purga de Datos Nulos",
        "description": (
            "El stream de datos del sensor de energía tiene registros corruptos "
            "marcados como `NULL`. El analizador del Nexo no puede procesar "
            "valores nulos — deben ser reemplazados por `0` antes del análisis.\n\n"
            "Dada la cadena `datos = \"10-NULL-45-NULL-78\"`, "
            "reemplaza todos los `NULL` por `0` e imprime el resultado.\n\n"
            "Salida esperada:\n"
            "```\n10-0-45-0-78\n```"
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "easy",
        "sector_id": 6,
        "level_order": 54,
        "base_xp_reward": 125,
        "is_project": False,
        "telemetry_goal_time": 90,
        "challenge_type": "python",
        "phase": "cadenas",
        "concepts_taught_json": json.dumps(["strings", ".replace()", "limpieza de datos"]),
        "initial_code": (
            "# MISIÓN: Reemplaza todos los NULL por 0\n"
            "\n"
            'datos = "10-NULL-45-NULL-78"\n'
            "\n"
            '# Reemplaza "NULL" por "0"\n'
            "print(datos.___(___,___))\n"
        ),
        "expected_output": "10-0-45-0-78",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El sensor de energía del Sector 05 tiene intermitencias. "
            "Cuando pierde la señal registra 'NULL' en lugar del valor real. "
            "El analizador de DAKI falla si encuentra valores NULL en el stream. "
            "Antes de procesar los datos, debes aplicar el protocolo de purga "
            "y convertir todos los NULL a cero para que el sistema pueda continuar."
        ),
        "pedagogical_objective": (
            "Usar .replace(antiguo, nuevo) para sustituir todas las ocurrencias "
            "de un substring. Entender que .replace() retorna un nuevo string "
            "y no modifica el original."
        ),
        "syntax_hint": 'print(datos.replace("NULL", "0"))',
        "theory_content": THEORY_N44,
        "hints_json": json.dumps([
            '.replace() toma dos argumentos: el texto a buscar y el reemplazo. Sintaxis: cadena.replace("buscar", "nuevo")',
            '.replace() reemplaza TODAS las apariciones automáticamente, no solo la primera.',
            'Solución: print(datos.replace("NULL", "0"))',
        ]),
        "strict_match": True,
    },
    # ── NIVEL 45 — .split() ────────────────────────────────────────────────────
    {
        "title": "Parseo de Transmisión",
        "description": (
            "Las transmisiones del sistema de alerta llegan como una cadena "
            "de componentes separados por comas. El parser del Nexo necesita "
            "separar cada componente para analizarlos individualmente.\n\n"
            "Dada la señal `señal = \"ROJO,VERDE,AZUL,BLANCO\"`, "
            "divide la cadena por comas e imprime cada componente en su propia línea.\n\n"
            "Salida esperada:\n"
            "```\nROJO\nVERDE\nAZUL\nBLANCO\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 6,
        "level_order": 55,
        "base_xp_reward": 150,
        "is_project": False,
        "telemetry_goal_time": 120,
        "challenge_type": "python",
        "phase": "cadenas",
        "concepts_taught_json": json.dumps([
            "strings", ".split()", "iteración sobre lista", "parsing"
        ]),
        "initial_code": (
            "# MISIÓN: Divide la señal por comas e imprime cada componente\n"
            "\n"
            'señal = "ROJO,VERDE,AZUL,BLANCO"\n'
            "\n"
            "# Divide la cadena y recorre los componentes\n"
            "for componente in señal.___(___):  \n"
            "    print(componente)\n"
        ),
        "expected_output": "ROJO\nVERDE\nAZUL\nBLANCO",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El sistema de alerta del Nexo transmite los códigos de amenaza "
            "en una sola cadena comprimida para minimizar el ancho de banda. "
            "Al recibirlos, el parser de DAKI debe descomprimirlos "
            "y analizar cada código de forma independiente para determinar "
            "el nivel de respuesta adecuado."
        ),
        "pedagogical_objective": (
            "Usar .split(separador) para dividir un string en una lista. "
            "Combinar split() con un for para iterar sobre los componentes resultantes."
        ),
        "syntax_hint": 'for componente in señal.split(","):\n    print(componente)',
        "theory_content": THEORY_N45,
        "hints_json": json.dumps([
            '.split(",") divide la cadena en cada coma y devuelve una lista: ["ROJO", "VERDE", ...].',
            'Puedes iterar directamente: for componente in señal.split(","):',
            'Dentro del for solo necesitas print(componente).',
        ]),
        "strict_match": True,
    },
    # ── NIVEL 46 — .join() ────────────────────────────────────────────────────
    {
        "title": "Ensamblado de Protocolo",
        "description": (
            "El sistema de protocolos del Nexo recibe identificadores de módulo "
            "como elementos separados y debe ensamblarlos en una cadena unificada "
            "para el log de transmisión.\n\n"
            "Dada la lista `fragmentos = [\"NEXO\", \"ALFA\", \"DELTA\"]`, "
            "une los elementos con el separador `\" | \"` e imprime el resultado.\n\n"
            "Salida esperada:\n"
            "```\nNEXO | ALFA | DELTA\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 6,
        "level_order": 56,
        "base_xp_reward": 150,
        "is_project": False,
        "telemetry_goal_time": 120,
        "challenge_type": "python",
        "phase": "cadenas",
        "concepts_taught_json": json.dumps([
            "strings", ".join()", "listas", "unión de cadenas"
        ]),
        "initial_code": (
            "# MISIÓN: Une los fragmentos con ' | ' como separador\n"
            "\n"
            'fragmentos = ["NEXO", "ALFA", "DELTA"]\n'
            "\n"
            "# Une la lista con ' | ' entre cada elemento\n"
            "print(___.join(fragmentos))\n"
        ),
        "expected_output": "NEXO | ALFA | DELTA",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El log de transmisión del Nexo requiere que los identificadores de módulo "
            "estén unidos con el separador estándar ' | ' para mantener la legibilidad "
            "del registro de actividad. El módulo de ensamblado de DAKI recibe "
            "la lista de fragmentos activos y los une en una sola línea de transmisión."
        ),
        "pedagogical_objective": (
            "Introducir .join() como el inverso de .split(). "
            "Entender que el separador va ANTES del .join() y la lista es el argumento."
        ),
        "syntax_hint": 'print(" | ".join(fragmentos))',
        "theory_content": THEORY_N46,
        "hints_json": json.dumps([
            ".join() une los elementos de una lista con un separador. El separador va ANTES del punto.",
            'La sintaxis es: separador.join(lista). El separador aquí es " | " (con espacios).',
            'Solución: print(" | ".join(fragmentos))',
        ]),
        "strict_match": True,
    },
    # ── NIVEL 47 — .count(), .startswith(), .endswith() ───────────────────────
    {
        "title": "Análisis de Log",
        "description": (
            "El sistema de monitoreo del Nexo analiza logs para determinar "
            "la gravedad de un incidente.\n\n"
            "Dado el log:\n"
            "```\nlog = \"CRITICO: ERROR en sector 3. ERROR en nodo 7.\"\n```\n\n"
            "Imprime:\n"
            "1. Cuántas veces aparece la palabra `ERROR` en el log\n"
            "2. Si el log **comienza** con `CRITICO` (`True` o `False`)\n\n"
            "Salida esperada:\n"
            "```\n2\nTrue\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 6,
        "level_order": 57,
        "base_xp_reward": 175,
        "is_project": False,
        "telemetry_goal_time": 150,
        "challenge_type": "python",
        "phase": "cadenas",
        "concepts_taught_json": json.dumps([
            "strings", ".count()", ".startswith()", ".endswith()", ".find()"
        ]),
        "initial_code": (
            "# MISIÓN: Analiza el log sin usar bucles\n"
            "\n"
            'log = "CRITICO: ERROR en sector 3. ERROR en nodo 7."\n'
            "\n"
            '# Imprime cuántas veces aparece "ERROR"\n'
            'print(log.___("ERROR"))\n'
            "\n"
            '# Imprime True si el log comienza con "CRITICO"\n'
            'print(log.___("CRITICO"))\n'
        ),
        "expected_output": "2\nTrue",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El sistema de clasificación de alertas del Nexo necesita dos métricas rápidas: "
            "cuántos errores contiene el log (para calcular la puntuación del incidente) "
            "y si fue catalogado como crítico (para el nivel de escalado). "
            "DAKI diseñó este detector de patrones para el módulo de triaje de incidentes."
        ),
        "pedagogical_objective": (
            "Usar .count() para contar ocurrencias de un substring. "
            "Usar .startswith() para verificar prefijos. "
            "Demostrar búsqueda en strings sin necesidad de bucles manuales."
        ),
        "syntax_hint": 'print(log.count("ERROR"))\nprint(log.startswith("CRITICO"))',
        "theory_content": THEORY_N47,
        "hints_json": json.dumps([
            '.count("ERROR") cuenta cuántas veces aparece exactamente "ERROR" en el log.',
            '.startswith("CRITICO") devuelve True si el string comienza con ese prefijo exacto.',
            'Solución: print(log.count("ERROR")) y print(log.startswith("CRITICO"))',
        ]),
        "strict_match": True,
    },
    # ── NIVEL 48 — Encadenamiento + input ─────────────────────────────────────
    {
        "title": "Pipeline de Transformación",
        "description": (
            "Los operadores del campo envían identificadores de sector sin formato. "
            "El sistema de registro aplica tres transformaciones automáticas: "
            "elimina espacios extremos, reemplaza los espacios internos con `_`, "
            "y convierte todo a mayúsculas.\n\n"
            "Lee una cadena desde la entrada y aplica el pipeline completo.\n\n"
            "Entrada: `  nexo alfa  `\n\n"
            "Salida esperada:\n"
            "```\nNEXO_ALFA\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 6,
        "level_order": 58,
        "base_xp_reward": 200,
        "is_project": False,
        "telemetry_goal_time": 180,
        "challenge_type": "python",
        "phase": "cadenas",
        "concepts_taught_json": json.dumps([
            "strings", "encadenamiento de métodos",
            ".strip()", ".replace()", ".upper()", "input()"
        ]),
        "initial_code": (
            "# MISIÓN: Lee la entrada y aplica el pipeline de transformación\n"
            "\n"
            "entrada = input()\n"
            "\n"
            "# Pipeline: strip → replace espacios con _ → upper\n"
            "resultado = entrada.___().___(___, ___).___()\n"
            "print(resultado)\n"
        ),
        "expected_output": "NEXO_ALFA",
        "test_inputs_json": json.dumps(["  nexo alfa  "]),
        "lore_briefing": (
            "Los operadores de campo no siempre siguen el formato estándar "
            "cuando reportan su sector. El módulo de registro de DAKI aplica "
            "un pipeline automático: elimina el ruido de los extremos, "
            "estandariza los separadores, y normaliza a mayúsculas "
            "para que el sistema de indexación lo procese sin errores."
        ),
        "pedagogical_objective": (
            "Encadenar .strip(), .replace() y .upper() en un pipeline de una línea. "
            "Practicar transformaciones de strings con input(). "
            "Ver que el orden de los métodos importa."
        ),
        "syntax_hint": 'resultado = entrada.strip().replace(" ", "_").upper()',
        "theory_content": THEORY_N48,
        "hints_json": json.dumps([
            "El pipeline se aplica en orden de izquierda a derecha. Empieza con strip() para limpiar extremos.",
            'Después de strip(), usa .replace(" ", "_") para reemplazar los espacios internos con guión bajo.',
            'Finalmente .upper() convierte todo a mayúsculas. Cadena completa: entrada.strip().replace(" ", "_").upper()',
        ]),
        "strict_match": True,
    },
    # ── NIVEL 49 — Cifrado César ───────────────────────────────────────────────
    {
        "title": "Descifrado de Señal",
        "description": (
            "Las comunicaciones enemigas están cifradas con el **Cifrado César**: "
            "cada letra fue desplazada **3 posiciones hacia adelante** en el alfabeto. "
            "Debes descifrar el mensaje desplazando cada letra **3 posiciones atrás**.\n\n"
            "Lee un mensaje cifrado (solo letras mayúsculas, sin espacios ni símbolos) "
            "y descífralo letra por letra usando `ord()` y `chr()`.\n\n"
            "Entrada: `QHAR`\n\n"
            "Salida esperada:\n"
            "```\nNEXO\n```\n\n"
            "_Verificación: Q(−3)=N, H(−3)=E, A(−3 con wrap)=X, R(−3)=O_"
        ),
        "difficulty_tier": DifficultyTier.ADVANCED,
        "difficulty": "hard",
        "sector_id": 6,
        "level_order": 59,
        "base_xp_reward": 350,
        "is_project": False,
        "telemetry_goal_time": 300,
        "challenge_type": "python",
        "phase": "cadenas",
        "concepts_taught_json": json.dumps([
            "strings", "ord()", "chr()", "módulo %",
            "cifrado César", "iteración de string", "concatenación"
        ]),
        "initial_code": (
            "# MISIÓN: Descifra el mensaje César (desplazamiento = -3)\n"
            "\n"
            "cifrado = input()\n"
            'resultado = ""\n'
            "\n"
            "for c in cifrado:\n"
            "    # Descifra cada letra: desplaza -3 con wrap-around\n"
            "    # Pista: (ord(c) - ord('A') - 3) % 26 + ord('A')\n"
            "    letra = chr(___)\n"
            "    resultado += letra\n"
            "\n"
            "print(resultado)\n"
        ),
        "expected_output": "NEXO",
        "test_inputs_json": json.dumps(["QHAR"]),
        "lore_briefing": (
            "El servicio de inteligencia del Nexo interceptó una transmisión enemiga. "
            "El análisis de frecuencia reveló que usan el Cifrado César con desplazamiento +3. "
            "DAKI necesita que construyas el descifrador: un módulo que tome cualquier "
            "mensaje cifrado y lo convierta al texto original, letra por letra, "
            "usando la aritmética modular del alfabeto."
        ),
        "pedagogical_objective": (
            "Usar ord() y chr() para operar sobre caracteres numéricamente. "
            "Aplicar aritmética modular (%) para el wrap-around del alfabeto. "
            "Construir un string resultado concatenando caracteres en un for."
        ),
        "syntax_hint": (
            "for c in cifrado:\n"
            "    letra = chr((ord(c) - ord('A') - 3) % 26 + ord('A'))\n"
            "    resultado += letra"
        ),
        "theory_content": THEORY_N49,
        "hints_json": json.dumps([
            "ord('A') = 65. ord(c) - ord('A') convierte la letra a su índice 0-25 (A=0, B=1, ..., Z=25).",
            "El % 26 permite el wrap-around: si el índice resulta negativo, % 26 lo lleva al final del alfabeto. Ej: (-3) % 26 = 23.",
            "La fórmula completa para el chr: (ord(c) - ord('A') - 3) % 26 + ord('A'). Ponla dentro de chr().",
        ]),
        "strict_match": True,
    },
]


# ─── Lógica de población ──────────────────────────────────────────────────────

async def seed() -> None:
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    async with SessionLocal() as session:
        # Idempotente: elimina solo niveles 41–49 (preserva el CONTRATO-50)
        deleted = await session.execute(
            delete(Challenge).where(
                Challenge.sector_id == 6,
                Challenge.level_order < 50,
            )
        )
        deleted_count = deleted.rowcount
        await session.flush()
        print(f"🧹  Sector 05 (41-49) anterior eliminado — {deleted_count} challenge(s) removidos.")

        print(f"\n🌱  Insertando {len(SECTOR_06)} niveles del Sector 05...\n")
        for data in SECTOR_06:
            challenge = Challenge(**data)
            session.add(challenge)
            print(
                f"    [{data['level_order']:02d}/49] {data['title']:<38} "
                f"({data['difficulty'].upper()}, {data['base_xp_reward']} XP, "
                f"~{data['telemetry_goal_time']}s)"
            )

        await session.commit()

    await engine.dispose()
    print(f"\n✅  Sector 05 cargado — {len(SECTOR_06)} niveles listos.")
    print("    Boss CONTRATO-50 preservado (gestionar con seed_contratos.py)\n")


if __name__ == "__main__":
    asyncio.run(seed())
