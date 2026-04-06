/**
 * conceptGlossary.ts — Teoría mínima de DAKI para challenges sin theory_content
 *
 * Cada entrada tiene:
 *   - title:    nombre del concepto en voz DAKI
 *   - theory:   explicación de 2-3 líneas en tono DAKI
 *   - example:  fragmento Python de 2-3 líneas
 *   - realWorld: conexión con el mundo real (1 línea)
 */

export interface ConceptEntry {
  title:     string
  theory:    string
  example:   string
  realWorld: string
}

export const CONCEPT_GLOSSARY: Record<string, ConceptEntry> = {
  variable: {
    title:     'NODOS DE MEMORIA — Variables',
    theory:    'Una variable es un contenedor con nombre. Cuando escribes nombre = "DAKI", le dices a la máquina: guarda este valor bajo esta etiqueta. La máquina lo hace sin preguntar. Puedes cambiar ese valor en cualquier momento — la variable apunta al nuevo dato.',
    example:   'operador = "Alex"\nnivel = 5\nprint(operador, nivel)  # Alex 5',
    realWorld: 'Todo sistema que recuerda tu nombre de usuario, tu puntaje o tu configuración usa variables.',
  },
  for_loop: {
    title:     'PROTOCOLO DE ITERACIÓN — Bucles for',
    theory:    'Un bucle for ejecuta el mismo bloque de código para cada elemento de una secuencia. range(5) genera 0,1,2,3,4 — cinco ejecuciones. Es la herramienta más usada en Python para procesar colecciones de datos sin repetir código manualmente.',
    example:   'for i in range(3):\n    print(f"Ronda {i+1}")\n# Ronda 1 / Ronda 2 / Ronda 3',
    realWorld: 'Los algoritmos de recomendación de Netflix iteran sobre millones de usuarios con bucles como este.',
  },
  while_loop: {
    title:     'BUCLE CONDICIONAL — while',
    theory:    'El while ejecuta un bloque mientras su condición sea True. A diferencia del for, no sabe cuántas veces iterará — depende del estado del programa. Requiere que algo dentro del bucle cambie la condición, o se convierte en bucle infinito.',
    example:   'intentos = 0\nwhile intentos < 3:\n    print("Intento", intentos)\n    intentos += 1',
    realWorld: 'Los servidores web usan while True para escuchar peticiones indefinidamente hasta que se apagan.',
  },
  function: {
    title:     'MÓDULOS TÁCTICOS — Funciones',
    theory:    'Una función es un bloque de código reutilizable con nombre. def es la directiva de creación. Los parámetros son las entradas, return es la salida. Una función bien definida hace UNA cosa y la hace bien — ese es el principio más importante del código profesional.',
    example:   'def calcular_xp(nivel, bonus):\n    return nivel * 100 + bonus\n\nprint(calcular_xp(5, 50))  # 550',
    realWorld: 'Las APIs que usás cada día (Google Maps, Stripe, Anthropic) son colecciones de funciones expuestas al mundo.',
  },
  string: {
    title:     'CADENAS DE TEXTO — Strings',
    theory:    'Un string es una secuencia inmutable de caracteres. Puedes acceder a posiciones con índices (0 es el primero, -1 es el último), combinar strings con +, y extraer fragmentos con slicing [inicio:fin]. Los métodos como .upper(), .split(), .strip() son tus herramientas básicas.',
    example:   'codigo = "nexo"\nprint(codigo[0])     # n\nprint(codigo.upper()) # NEXO',
    realWorld: 'Todo procesamiento de texto — desde detectar spam hasta traducir idiomas — opera sobre strings.',
  },
  list: {
    title:     'COLECCIONES ORDENADAS — Listas',
    theory:    'Una lista guarda múltiples elementos en orden. Se accede por índice [0], se modifica con .append() y .remove(), y se itera con for. A diferencia de los strings, las listas son mutables — puedes cambiar su contenido después de crearlas.',
    example:   'mision = ["Alfa", "Beta", "Gamma"]\nmision.append("Delta")\nprint(mision[0])  # Alfa',
    realWorld: 'Las listas de reproducción, los carritos de compra y los feeds de redes sociales son listas en producción.',
  },
  dict: {
    title:     'REGISTROS CLAVE-VALOR — Diccionarios',
    theory:    'Un diccionario mapea claves únicas a valores. Acceso en O(1) — instantáneo sin importar el tamaño. Es la estructura de datos más usada en APIs, configuraciones y bases de datos documentales. Las claves son inmutables (strings, números), los valores pueden ser cualquier tipo.',
    example:   'operador = {"nombre": "Alex", "nivel": 7}\nprint(operador["nombre"])  # Alex',
    realWorld: 'Cada response JSON que ves en una API es un diccionario serializado.',
  },
  boolean: {
    title:     'BIFURCACIÓN TÁCTICA — Booleanos y Condiciones',
    theory:    'True y False son los únicos valores booleanos. Los operadores de comparación (==, !=, <, >) producen booleanos. El if evalúa la condición y ejecuta el bloque correspondiente. La lógica de todo programa se reduce eventualmente a decisiones True/False.',
    example:   'def es_par(n):\n    return n % 2 == 0\n\nprint(es_par(4))   # True\nprint(es_par(7))   # False',
    realWorld: 'Los sistemas de autenticación, permisos y filtros operan sobre condiciones booleanas.',
  },
  if_else: {
    title:     'CONTROL DE FLUJO — if / elif / else',
    theory:    'El if bifurca la ejecución basándose en una condición. elif encadena condiciones adicionales. else captura todos los casos restantes. La indentación (4 espacios) define qué pertenece a cada bloque — no es estética, es sintaxis obligatoria en Python.',
    example:   'nivel = 8\nif nivel >= 10:\n    rango = "Elite"\nelif nivel >= 5:\n    rango = "Activo"\nelse:\n    rango = "Recruit"',
    realWorld: 'Los motores de reglas de negocio (precios, descuentos, clasificaciones) son cadenas de if/elif/else.',
  },
  number: {
    title:     'OPERACIONES NUMÉRICAS — int y float',
    theory:    'Python distingue enteros (int) y decimales (float). La división / siempre produce float. La división entera // descarta decimales. El módulo % retorna el resto — fundamental para detectar pares, múltiplos y ciclos. int() y float() convierten entre tipos.',
    example:   'print(7 / 2)   # 3.5\nprint(7 // 2)  # 3\nprint(7 % 2)   # 1',
    realWorld: 'Los sistemas financieros usan Decimal (más preciso que float) para evitar errores de redondeo en pagos.',
  },
  input_fn: {
    title:     'ENTRADA DEL OPERADOR — input()',
    theory:    'input() detiene la ejecución y espera texto del usuario. SIEMPRE retorna string — aunque el usuario escriba 42, obtienes "42". Para operar numéricamente debes convertir: int(input()) o float(input()). El argumento opcional es el prompt visible.',
    example:   'nombre = input("Callsign: ")\nedad = int(input("Nivel: "))\nprint(f"Operador {nombre}, Nivel {edad}")',
    realWorld: 'Los CLIs profesionales (git, pip, docker) procesan inputs del operador con lógica más compleja pero el mismo principio.',
  },
  print_fn: {
    title:     'SALIDA DE DATOS — print()',
    theory:    'print() muestra datos en stdout. Acepta múltiples argumentos separados por comas. sep define el separador (default: espacio), end define el terminador (default: nueva línea). Los f-strings (f"Hola {variable}") son la forma moderna y legible de formatear salidas.',
    example:   'x = 42\nprint("Valor:", x)          # Valor: 42\nprint(f"Resultado: {x * 2}")  # Resultado: 84',
    realWorld: 'Los sistemas de logging en producción funcionan como print() pero con niveles (DEBUG, INFO, ERROR) y destinos configurables.',
  },
  range_fn: {
    title:     'GENERADOR DE SECUENCIAS — range()',
    theory:    'range(stop) genera 0..stop-1. range(start, stop) genera start..stop-1. range(start, stop, step) controla el paso — negativo para contar hacia atrás. No crea una lista en memoria — es un generador perezoso que produce un valor a la vez.',
    example:   'list(range(3))       # [0, 1, 2]\nlist(range(1, 4))    # [1, 2, 3]\nlist(range(0, 10, 2)) # [0, 2, 4, 6, 8]',
    realWorld: 'Los índices de bases de datos, los offsets de paginación y los lotes de procesamiento usan range().',
  },
  return_stmt: {
    title:     'PROTOCOLO DE RETORNO — return',
    theory:    'return termina la función y entrega un valor al código que la llamó. Sin return explícito, Python retorna None. Una función puede tener múltiples return (en diferentes ramas de if/else). El valor retornado puede usarse directamente o guardarse en una variable.',
    example:   'def clasificar(puntos):\n    if puntos >= 90: return "A"\n    if puntos >= 70: return "B"\n    return "C"\n\nresultado = clasificar(85)  # "B"',
    realWorld: 'Cada función de una API retorna datos al cliente — ese return es el contrato entre el servidor y el consumidor.',
  },
}

/**
 * Busca la teoría para un array de conceptos.
 * Retorna la primera entrada encontrada o null si ninguna coincide.
 */
export function getConceptTheory(concepts: string[]): ConceptEntry | null {
  for (const c of concepts) {
    const entry = CONCEPT_GLOSSARY[c.toLowerCase()] ?? CONCEPT_GLOSSARY[c]
    if (entry) return entry
  }
  return null
}
