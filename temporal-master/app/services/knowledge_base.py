"""
knowledge_base.py — Base de Conocimiento Táctico de DAKI (Prompt 58)

Fuente canónica de definiciones de Python reescritas con la terminología de DAKI.
El modelo LLM llama `lookup_tactical_concept` (tool use) para recuperar estas
definiciones en lugar de inventarlas o sugerir recursos externos.

Estructura de cada concepto:
    tactical_name  — nombre en vocabulario DAKI
    python_term    — nombre técnico en Python
    keywords       — triggers de búsqueda (en español e inglés)
    definition     — definición corta táctica (2-3 frases)
    syntax         — patrón de uso canónico
    example        — snippet Python aplicable a ejercicios de la plataforma
    tactics        — consejo práctico de uso
"""

from __future__ import annotations

TACTICAL_KNOWLEDGE: dict[str, dict] = {
    # ── Fundamentos ──────────────────────────────────────────────────────────

    "variable": {
        "tactical_name": "Registro / Nodo de Memoria",
        "python_term": "variable",
        "keywords": ["variable", "variables", "registro", "nodo de memoria"],
        "definition": (
            "Un registro es un contenedor con nombre que almacena un valor en "
            "la memoria del programa. El Nexo puede leerlo o sobreescribirlo en "
            "cualquier punto de la secuencia."
        ),
        "syntax": "nombre = valor",
        "example": (
            "operador = 'ARIA'\n"
            "nivel = 7\n"
            "activo = True"
        ),
        "tactics": (
            "Declara el registro antes de usarlo. Un registro no declarado "
            "lanza NameError — la señal no existe en los registros del Nexo."
        ),
    },

    "for_loop": {
        "tactical_name": "Protocolo de Iteración For",
        "python_term": "for loop",
        "keywords": ["for", "bucle for", "protocolo de iteración", "iteración"],
        "definition": (
            "Ejecuta un bloque de código para cada elemento de una secuencia. "
            "El Nexo recorre cada nodo de la colección, ejecuta el cuerpo, y "
            "avanza al siguiente — sin repetir ni saltar."
        ),
        "syntax": "for elemento in secuencia:\n    # cuerpo",
        "example": (
            "registros = [10, 20, 30]\n"
            "for nodo in registros:\n"
            "    print(nodo)"
        ),
        "tactics": (
            "El `for` termina automáticamente al agotar la secuencia. "
            "No necesita condición de salida. Para iterar N veces, usa `range(N)`."
        ),
    },

    "while_loop": {
        "tactical_name": "Protocolo de Iteración While",
        "python_term": "while loop",
        "keywords": ["while", "bucle while", "while loop"],
        "definition": (
            "Ejecuta un bloque de código mientras una condición sea verdadera. "
            "A diferencia del `for`, el `while` no recorre una secuencia fija — "
            "continúa hasta que la condición cambia a False."
        ),
        "syntax": "while condicion:\n    # cuerpo\n    # actualizar condicion",
        "example": (
            "energia = 10\n"
            "while energia > 0:\n"
            "    print(energia)\n"
            "    energia -= 1"
        ),
        "tactics": (
            "Siempre incluye una instrucción que modifique la condición dentro del cuerpo. "
            "Si la condición nunca se vuelve False, el programa entra en bucle infinito — "
            "el Nexo lo detectará como proceso parásito."
        ),
    },

    "if_else": {
        "tactical_name": "Bifurcación Táctica",
        "python_term": "if / elif / else",
        "keywords": ["if", "elif", "else", "bifurcación", "condicional", "condición"],
        "definition": (
            "Ejecuta bloques de código distintos según una condición. "
            "La bifurcación evalúa la condición: si es True, ejecuta el bloque `if`; "
            "si no, ejecuta `elif` o `else`."
        ),
        "syntax": "if condicion:\n    # bloque A\nelif otra:\n    # bloque B\nelse:\n    # bloque C",
        "example": (
            "nivel = 5\n"
            "if nivel >= 10:\n"
            "    print('Acceso concedido')\n"
            "elif nivel >= 5:\n"
            "    print('Acceso parcial')\n"
            "else:\n"
            "    print('Acceso denegado')"
        ),
        "tactics": (
            "Usa `==` para comparar (no `=`). "
            "El `else` es el fallback — se ejecuta solo si ningún bloque anterior fue True."
        ),
    },

    "function": {
        "tactical_name": "Módulo / Núcleo Funcional",
        "python_term": "function",
        "keywords": ["def", "function", "función", "módulo", "núcleo", "definir función"],
        "definition": (
            "Un módulo es un bloque de código reutilizable con nombre que realiza una operación. "
            "Recibe parámetros de entrada y puede devolver un resultado con `return`. "
            "Encapsula lógica para no repetirla."
        ),
        "syntax": "def nombre(parametro):\n    # cuerpo\n    return resultado",
        "example": (
            "def calcular_poder(nivel, bonus):\n"
            "    return nivel * 10 + bonus\n\n"
            "resultado = calcular_poder(5, 3)"
        ),
        "tactics": (
            "Sin `return`, el módulo devuelve `None`. "
            "Los parámetros son registros locales — solo existen dentro del módulo."
        ),
    },

    # ── Estructuras de datos ──────────────────────────────────────────────────

    "list": {
        "tactical_name": "Secuencia de Datos",
        "python_term": "list",
        "keywords": ["list", "lista", "secuencia", "array", "arreglo"],
        "definition": (
            "Una secuencia ordenada y mutable de elementos. "
            "Cada elemento ocupa una posición (índice, comenzando en 0). "
            "Puede contener mezcla de tipos."
        ),
        "syntax": "secuencia = [elemento0, elemento1, elemento2]",
        "example": (
            "operadores = ['ARIA', 'NEXO', 'DAKI']\n"
            "print(operadores[0])  # ARIA\n"
            "operadores.append('ZEUS')"
        ),
        "tactics": (
            "El índice -1 accede al último elemento. "
            "Fuera de rango → IndexError. "
            "Para recorrer: `for elemento in lista`."
        ),
    },

    "dict": {
        "tactical_name": "Mapa de Inteligencia",
        "python_term": "dict",
        "keywords": ["dict", "diccionario", "dictionary", "mapa", "clave", "valor", "key", "value"],
        "definition": (
            "Estructura de datos clave→valor. Cada clave es única y mapea a un valor. "
            "El Nexo accede al valor directamente por clave — sin recorrer la estructura. "
            "Las claves son inmutables (str, int, tuple)."
        ),
        "syntax": "mapa = {'clave': valor, 'clave2': valor2}",
        "example": (
            "operador = {'nombre': 'ARIA', 'nivel': 7, 'activo': True}\n"
            "print(operador['nombre'])  # ARIA\n"
            "operador['nivel'] = 8"
        ),
        "tactics": (
            "Acceder a una clave inexistente → KeyError. "
            "Usa `.get('clave', default)` para acceso seguro. "
            "Para recorrer: `for k, v in mapa.items()`."
        ),
    },

    "string": {
        "tactical_name": "Cadena de Señales",
        "python_term": "string",
        "keywords": ["str", "string", "cadena", "texto", "texto"],
        "definition": (
            "Secuencia inmutable de caracteres. "
            "Se define con comillas simples o dobles. "
            "Soporta slicing, concatenación y métodos como `.upper()`, `.split()`, `.strip()`."
        ),
        "syntax": 'cadena = "texto"  # o  cadena = \'texto\'',
        "example": (
            "codename = 'NEXO-7'\n"
            "print(codename.upper())     # NEXO-7\n"
            "print(codename[0:4])        # NEXO\n"
            "print(len(codename))        # 6"
        ),
        "tactics": (
            "Las cadenas son inmutables — no puedes cambiar un carácter directamente. "
            "Para construir cadenas dinámicas usa f-strings: `f'Nivel: {nivel}'`."
        ),
    },

    "number": {
        "tactical_name": "Registro Numérico",
        "python_term": "int / float",
        "keywords": ["int", "float", "integer", "número", "entero", "decimal"],
        "definition": (
            "`int` almacena enteros (sin decimales). `float` almacena decimales. "
            "`input()` siempre devuelve `str` — debes convertir con `int()` o `float()` "
            "antes de operar matemáticamente."
        ),
        "syntax": "n = int('42')   # str → int\nf = float('3.14')  # str → float",
        "example": (
            "entrada = input('Nivel: ')\n"
            "nivel = int(entrada)       # conversión obligatoria\n"
            "poder = nivel * 10.5"
        ),
        "tactics": (
            "División entera: `//` (sin decimal). División flotante: `/`. "
            "Módulo: `%` (resto de la división). "
            "`int('abc')` lanza ValueError — valida la entrada antes."
        ),
    },

    # ── I/O ───────────────────────────────────────────────────────────────────

    "input_fn": {
        "tactical_name": "Señal de Entrada",
        "python_term": "input()",
        "keywords": ["input", "input()", "señal de entrada", "entrada"],
        "definition": (
            "Lee una línea de texto desde el canal de entrada (teclado). "
            "SIEMPRE devuelve un `str` — independientemente de lo que escriba el Operador. "
            "Para usar el valor como número, convierte con `int()` o `float()`."
        ),
        "syntax": "registro = input('Mensaje: ')",
        "example": (
            "nombre = input('Introduce tu codename: ')\n"
            "nivel_str = input('Nivel de acceso: ')\n"
            "nivel = int(nivel_str)  # conversión str → int"
        ),
        "tactics": (
            "Nunca operes matemáticamente sobre el resultado de `input()` sin convertir. "
            "TypeError: can only concatenate str (not 'int') to str — es el síntoma clásico."
        ),
    },

    "print_fn": {
        "tactical_name": "Emisión al Canal de Salida",
        "python_term": "print()",
        "keywords": ["print", "print()", "emisión", "imprimir", "mostrar"],
        "definition": (
            "Emite valores al canal de salida estándar (stdout). "
            "Acepta múltiples argumentos separados por comas y los une con espacio. "
            "No devuelve ningún valor (`None`)."
        ),
        "syntax": "print(valor1, valor2, sep=' ', end='\\n')",
        "example": (
            "operador = 'ARIA'\n"
            "nivel = 7\n"
            "print('Operador:', operador, '| Nivel:', nivel)\n"
            "print(f'Poder total: {nivel * 10}')"
        ),
        "tactics": (
            "Usar `print()` dentro de una función no reemplaza al `return`. "
            "Si el ejercicio pide 'devuelve el resultado', usa `return`, no `print`."
        ),
    },

    "range_fn": {
        "tactical_name": "Generador de Secuencia",
        "python_term": "range()",
        "keywords": ["range", "range()", "generador de secuencia"],
        "definition": (
            "Genera una secuencia de enteros sin almacenarlos en memoria. "
            "`range(n)` produce 0, 1, …, n-1. "
            "`range(inicio, fin, paso)` permite control total."
        ),
        "syntax": "range(stop)  |  range(start, stop)  |  range(start, stop, step)",
        "example": (
            "# Iterar 5 veces: 0, 1, 2, 3, 4\n"
            "for i in range(5):\n"
            "    print(i)\n\n"
            "# Números pares: 0, 2, 4, 6, 8\n"
            "for par in range(0, 10, 2):\n"
            "    print(par)"
        ),
        "tactics": (
            "`range(5)` va de 0 a 4 — el límite superior es exclusivo. "
            "Para recorrer en reversa: `range(10, 0, -1)`."
        ),
    },

    # ── Control de flujo ──────────────────────────────────────────────────────

    "return_stmt": {
        "tactical_name": "Protocolo de Extracción",
        "python_term": "return",
        "keywords": ["return", "retorno", "protocolo de extracción", "devolver"],
        "definition": (
            "Finaliza la ejecución de un módulo y devuelve un valor al punto de llamada. "
            "Sin `return`, el módulo devuelve `None` implícitamente. "
            "Todo código después de `return` es inalcanzable."
        ),
        "syntax": "def modulo():\n    # lógica\n    return resultado",
        "example": (
            "def calcular_nivel(xp):\n"
            "    if xp >= 100:\n"
            "        return 'Maestro'\n"
            "    return 'Trainee'\n\n"
            "rango = calcular_nivel(150)  # 'Maestro'"
        ),
        "tactics": (
            "Confundir `print` con `return` es la falla más frecuente. "
            "Si el ejercicio dice 'la función debe retornar X', usa `return X` dentro del `def`."
        ),
    },

    "import_stmt": {
        "tactical_name": "Carga de Módulo Externo",
        "python_term": "import",
        "keywords": ["import", "from import", "módulo externo", "librería"],
        "definition": (
            "Carga un módulo externo para usar sus funciones y clases. "
            "`import math` carga el módulo completo. "
            "`from math import sqrt` importa solo `sqrt`."
        ),
        "syntax": "import modulo\nfrom modulo import funcion",
        "example": (
            "import math\n"
            "raiz = math.sqrt(144)  # 12.0\n\n"
            "from random import randint\n"
            "dado = randint(1, 6)"
        ),
        "tactics": (
            "Los imports van al inicio del archivo. "
            "Importar algo que no existe lanza ModuleNotFoundError."
        ),
    },

    "boolean": {
        "tactical_name": "Registro de Estado Binario",
        "python_term": "bool",
        "keywords": ["bool", "boolean", "true", "false", "verdadero", "falso", "booleano"],
        "definition": (
            "Tipo de dato con solo dos valores: `True` o `False`. "
            "Es el resultado de comparaciones (`==`, `<`, `>`, `!=`, `in`). "
            "Los operadores lógicos `and`, `or`, `not` combinan booleanos."
        ),
        "syntax": "activo = True\nvalidado = (nivel >= 10)",
        "example": (
            "nivel = 7\n"
            "acceso = nivel >= 5 and nivel < 10\n"
            "print(acceso)   # True\n"
            "print(not acceso)  # False"
        ),
        "tactics": (
            "En Python, `0`, `''`, `[]`, `None` son falsy (equivalen a False en un `if`). "
            "Cualquier otro valor es truthy."
        ),
    },
}


# ─── Acceso ───────────────────────────────────────────────────────────────────

def get_concept(concept_id: str) -> dict | None:
    """Devuelve el concepto por su ID, o None si no existe."""
    return TACTICAL_KNOWLEDGE.get(concept_id)


def list_concepts() -> list[dict]:
    """Devuelve todos los conceptos como lista con su ID incluido."""
    return [
        {"concept_id": cid, **data}
        for cid, data in TACTICAL_KNOWLEDGE.items()
    ]


def find_by_keyword(term: str) -> str | None:
    """
    Busca un concept_id cuyas keywords coincidan con el término.
    Búsqueda case-insensitive, coincidencia exacta de palabra.
    """
    term_lower = term.lower().rstrip("()")
    for cid, data in TACTICAL_KNOWLEDGE.items():
        if term_lower in [kw.lower() for kw in data["keywords"]]:
            return cid
        if term_lower == data["python_term"].lower():
            return cid
    return None
