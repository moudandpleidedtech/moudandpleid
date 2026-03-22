/**
 * tacticalKnowledge.ts — Base de Conocimiento Táctico en el frontend (Prompt 58)
 *
 * Espejo del knowledge_base.py del backend. Se usa para resolver tooltips
 * interactivos en la terminal sin necesidad de una petición de red.
 *
 * La fuente canónica sigue siendo el backend — este archivo es una copia
 * de lectura para el cliente.
 */

export interface TacticalConcept {
  concept_id: string
  tactical_name: string
  python_term: string
  keywords: string[]
  definition: string
  syntax: string
  example: string
  tactics: string
}

export const TACTICAL_KNOWLEDGE: Record<string, TacticalConcept> = {
  variable: {
    concept_id: 'variable',
    tactical_name: 'Registro / Nodo de Memoria',
    python_term: 'variable',
    keywords: ['variable', 'variables', 'registro', 'nodo de memoria'],
    definition:
      'Un registro es un contenedor con nombre que almacena un valor en la memoria del programa. El Nexo puede leerlo o sobreescribirlo en cualquier punto de la secuencia.',
    syntax: 'nombre = valor',
    example: "operador = 'ARIA'\nnivel = 7\nactivo = True",
    tactics: 'Declara el registro antes de usarlo. Un registro no declarado lanza NameError — la señal no existe en los registros del Nexo.',
  },
  for_loop: {
    concept_id: 'for_loop',
    tactical_name: 'Protocolo de Iteración For',
    python_term: 'for loop',
    keywords: ['for', 'bucle for', 'protocolo de iteración', 'iteración'],
    definition:
      'Ejecuta un bloque de código para cada elemento de una secuencia. El Nexo recorre cada nodo de la colección, ejecuta el cuerpo, y avanza al siguiente — sin repetir ni saltar.',
    syntax: 'for elemento in secuencia:\n    # cuerpo',
    example: 'registros = [10, 20, 30]\nfor nodo in registros:\n    print(nodo)',
    tactics: 'El `for` termina automáticamente al agotar la secuencia. Para iterar N veces, usa `range(N)`.',
  },
  while_loop: {
    concept_id: 'while_loop',
    tactical_name: 'Protocolo de Iteración While',
    python_term: 'while loop',
    keywords: ['while', 'bucle while', 'while loop'],
    definition:
      'Ejecuta un bloque de código mientras una condición sea verdadera. A diferencia del `for`, el `while` no recorre una secuencia fija — continúa hasta que la condición cambia a False.',
    syntax: 'while condicion:\n    # cuerpo\n    # actualizar condicion',
    example: 'energia = 10\nwhile energia > 0:\n    print(energia)\n    energia -= 1',
    tactics: 'Siempre modifica la condición dentro del cuerpo. Si nunca se vuelve False, el programa entra en bucle infinito.',
  },
  if_else: {
    concept_id: 'if_else',
    tactical_name: 'Bifurcación Táctica',
    python_term: 'if / elif / else',
    keywords: ['if', 'elif', 'else', 'bifurcación', 'condicional', 'condición'],
    definition:
      'Ejecuta bloques de código distintos según una condición. La bifurcación evalúa: si es True ejecuta el bloque `if`; si no, ejecuta `elif` o `else`.',
    syntax: 'if condicion:\n    # bloque A\nelif otra:\n    # bloque B\nelse:\n    # bloque C',
    example: "nivel = 5\nif nivel >= 10:\n    print('Acceso concedido')\nelif nivel >= 5:\n    print('Acceso parcial')\nelse:\n    print('Acceso denegado')",
    tactics: 'Usa `==` para comparar (no `=`). El `else` es el fallback — se ejecuta solo si ningún bloque anterior fue True.',
  },
  function: {
    concept_id: 'function',
    tactical_name: 'Módulo / Núcleo Funcional',
    python_term: 'function',
    keywords: ['def', 'function', 'función', 'módulo', 'núcleo', 'definir función'],
    definition:
      'Un módulo es un bloque de código reutilizable con nombre. Recibe parámetros de entrada y puede devolver un resultado con `return`. Encapsula lógica para no repetirla.',
    syntax: 'def nombre(parametro):\n    # cuerpo\n    return resultado',
    example: 'def calcular_poder(nivel, bonus):\n    return nivel * 10 + bonus\n\nresultado = calcular_poder(5, 3)',
    tactics: 'Sin `return`, el módulo devuelve `None`. Los parámetros son registros locales — solo existen dentro del módulo.',
  },
  list: {
    concept_id: 'list',
    tactical_name: 'Secuencia de Datos',
    python_term: 'list',
    keywords: ['list', 'lista', 'secuencia', 'array', 'arreglo'],
    definition:
      'Una secuencia ordenada y mutable de elementos. Cada elemento ocupa una posición (índice, comenzando en 0). Puede contener mezcla de tipos.',
    syntax: 'secuencia = [elemento0, elemento1, elemento2]',
    example: "operadores = ['ARIA', 'NEXO', 'DAKI']\nprint(operadores[0])  # ARIA\noperadores.append('ZEUS')",
    tactics: 'El índice -1 accede al último elemento. Fuera de rango → IndexError.',
  },
  dict: {
    concept_id: 'dict',
    tactical_name: 'Mapa de Inteligencia',
    python_term: 'dict',
    keywords: ['dict', 'diccionario', 'dictionary', 'mapa', 'clave', 'valor', 'key', 'value'],
    definition:
      'Estructura clave→valor. Cada clave es única y mapea a un valor. El Nexo accede al valor directamente por clave — sin recorrer la estructura.',
    syntax: "mapa = {'clave': valor, 'clave2': valor2}",
    example: "operador = {'nombre': 'ARIA', 'nivel': 7}\nprint(operador['nombre'])  # ARIA\noperador['nivel'] = 8",
    tactics: 'Acceder a clave inexistente → KeyError. Usa `.get(\'clave\', default)` para acceso seguro.',
  },
  string: {
    concept_id: 'string',
    tactical_name: 'Cadena de Señales',
    python_term: 'string',
    keywords: ['str', 'string', 'cadena', 'texto'],
    definition:
      'Secuencia inmutable de caracteres. Se define con comillas simples o dobles. Soporta slicing, concatenación y métodos como `.upper()`, `.split()`, `.strip()`.',
    syntax: 'cadena = "texto"  # o  cadena = \'texto\'',
    example: "codename = 'NEXO-7'\nprint(codename.upper())   # NEXO-7\nprint(codename[0:4])      # NEXO",
    tactics: 'Las cadenas son inmutables. Para cadenas dinámicas usa f-strings: `f\'Nivel: {nivel}\'`.',
  },
  number: {
    concept_id: 'number',
    tactical_name: 'Registro Numérico',
    python_term: 'int / float',
    keywords: ['int', 'float', 'integer', 'número', 'entero', 'decimal'],
    definition:
      '`int` almacena enteros (sin decimales). `float` almacena decimales. `input()` siempre devuelve `str` — debes convertir con `int()` o `float()` antes de operar matemáticamente.',
    syntax: 'n = int(\'42\')   # str → int\nf = float(\'3.14\')  # str → float',
    example: "entrada = input('Nivel: ')\nnivel = int(entrada)\npoder = nivel * 10.5",
    tactics: 'División entera: `//`. División flotante: `/`. Módulo: `%` (resto). `int(\'abc\')` lanza ValueError.',
  },
  input_fn: {
    concept_id: 'input_fn',
    tactical_name: 'Señal de Entrada',
    python_term: 'input()',
    keywords: ['input', 'input()', 'señal de entrada', 'entrada'],
    definition:
      'Lee una línea de texto desde el canal de entrada (teclado). SIEMPRE devuelve `str` — independientemente de lo que escriba el Operador.',
    syntax: 'registro = input(\'Mensaje: \')',
    example: "nombre = input('Introduce tu codename: ')\nnivel = int(input('Nivel de acceso: '))",
    tactics: 'Nunca operes matemáticamente sobre `input()` sin convertir. TypeError es el síntoma clásico.',
  },
  print_fn: {
    concept_id: 'print_fn',
    tactical_name: 'Emisión al Canal de Salida',
    python_term: 'print()',
    keywords: ['print', 'print()', 'emisión', 'imprimir', 'mostrar'],
    definition:
      'Emite valores al canal de salida estándar (stdout). Acepta múltiples argumentos separados por comas. No devuelve ningún valor (`None`).',
    syntax: "print(valor1, valor2, sep=' ', end='\\n')",
    example: "operador = 'ARIA'\nprint('Operador:', operador)\nprint(f'Nivel: {7 * 10}')",
    tactics: '`print()` dentro de una función no reemplaza al `return`. Si el ejercicio pide "retorna", usa `return`.',
  },
  range_fn: {
    concept_id: 'range_fn',
    tactical_name: 'Generador de Secuencia',
    python_term: 'range()',
    keywords: ['range', 'range()', 'generador de secuencia'],
    definition:
      'Genera una secuencia de enteros sin almacenarlos en memoria. `range(n)` produce 0, 1, …, n-1.',
    syntax: 'range(stop)  |  range(start, stop)  |  range(start, stop, step)',
    example: '# 0, 1, 2, 3, 4\nfor i in range(5):\n    print(i)\n\n# Pares: 0, 2, 4, 6, 8\nfor par in range(0, 10, 2):\n    print(par)',
    tactics: '`range(5)` va de 0 a 4 — el límite superior es exclusivo. Reversa: `range(10, 0, -1)`.',
  },
  return_stmt: {
    concept_id: 'return_stmt',
    tactical_name: 'Protocolo de Extracción',
    python_term: 'return',
    keywords: ['return', 'retorno', 'protocolo de extracción', 'devolver'],
    definition:
      'Finaliza la ejecución de un módulo y devuelve un valor al punto de llamada. Sin `return`, el módulo devuelve `None` implícitamente.',
    syntax: 'def modulo():\n    # lógica\n    return resultado',
    example: "def calcular_nivel(xp):\n    if xp >= 100:\n        return 'Maestro'\n    return 'Trainee'\n\nrango = calcular_nivel(150)",
    tactics: 'Confundir `print` con `return` es la falla más frecuente. Si dice "la función debe retornar X", usa `return X` dentro del `def`.',
  },
  import_stmt: {
    concept_id: 'import_stmt',
    tactical_name: 'Carga de Módulo Externo',
    python_term: 'import',
    keywords: ['import', 'from import', 'módulo externo', 'librería'],
    definition:
      'Carga un módulo externo para usar sus funciones. `import math` carga el módulo completo. `from math import sqrt` importa solo `sqrt`.',
    syntax: 'import modulo\nfrom modulo import funcion',
    example: 'import math\nraiz = math.sqrt(144)  # 12.0\n\nfrom random import randint\ndado = randint(1, 6)',
    tactics: 'Los imports van al inicio del archivo. Importar algo inexistente lanza ModuleNotFoundError.',
  },
  boolean: {
    concept_id: 'boolean',
    tactical_name: 'Registro de Estado Binario',
    python_term: 'bool',
    keywords: ['bool', 'boolean', 'true', 'false', 'verdadero', 'falso', 'booleano'],
    definition:
      'Tipo con solo dos valores: `True` o `False`. Es el resultado de comparaciones. Los operadores `and`, `or`, `not` combinan booleanos.',
    syntax: 'activo = True\nvalidado = (nivel >= 10)',
    example: 'nivel = 7\nacceso = nivel >= 5 and nivel < 10\nprint(acceso)      # True\nprint(not acceso)  # False',
    tactics: 'En Python, `0`, `\'\'`, `[]`, `None` son falsy. Cualquier otro valor es truthy.',
  },
}

/**
 * Mapea un término Python (con o sin paréntesis) al concept_id correspondiente.
 * Usado por el parser de la terminal para detectar keywords en backticks.
 */
export const TERM_TO_CONCEPT: Record<string, string> = {
  // for_loop
  for: 'for_loop',
  // while_loop
  while: 'while_loop',
  // if_else
  if: 'if_else',
  elif: 'if_else',
  else: 'if_else',
  // function
  def: 'function',
  function: 'function',
  función: 'function',
  // list
  list: 'list',
  lista: 'list',
  // dict
  dict: 'dict',
  diccionario: 'dict',
  dictionary: 'dict',
  // string
  str: 'string',
  string: 'string',
  cadena: 'string',
  // number
  int: 'number',
  float: 'number',
  integer: 'number',
  número: 'number',
  // input
  input: 'input_fn',
  // print
  print: 'print_fn',
  // range
  range: 'range_fn',
  // return
  return: 'return_stmt',
  // import
  import: 'import_stmt',
  // boolean
  bool: 'boolean',
  boolean: 'boolean',
  true: 'boolean',
  false: 'boolean',
  // variable
  variable: 'variable',
  variables: 'variable',
  registro: 'variable',
}
