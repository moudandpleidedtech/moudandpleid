/**
 * conceptGlossary.ts — Teoría mínima de DAKI para challenges sin theory_content
 *
 * Cada entrada tiene:
 *   - title:    nombre del concepto en voz DAKI
 *   - theory:   explicación de 2-3 líneas en tono DAKI
 *   - example:  fragmento Python de 2-3 líneas
 *   - realWorld: conexión con el mundo real (1 línea)
 *
 * Las claves deben coincidir con los valores en concepts_taught_json de la DB
 * (la búsqueda usa c.toLowerCase()).
 */

export interface ConceptEntry {
  title:     string
  theory:    string
  example:   string
  realWorld: string
}

export const CONCEPT_GLOSSARY: Record<string, ConceptEntry> = {

  // ── Variables & Tipos básicos ─────────────────────────────────────────────

  variable: {
    title:     'NODOS DE MEMORIA — Variables',
    theory:    'Una variable es un contenedor con nombre. Cuando escribes nombre = "DAKI", le dices a la máquina: guarda este valor bajo esta etiqueta. Puedes cambiar ese valor en cualquier momento — la variable apunta al nuevo dato.',
    example:   'operador = "Alex"\nnivel = 5\nprint(operador, nivel)  # Alex 5',
    realWorld: 'Todo sistema que recuerda tu nombre de usuario, tu puntaje o tu configuración usa variables.',
  },

  variables: {
    title:     'NODOS DE MEMORIA — Variables',
    theory:    'Las variables almacenan datos que el programa puede leer y modificar. Python es dinámico — una variable puede cambiar de tipo. Usa nombres descriptivos: nivel, no n; usuario, no u.',
    example:   'puntos = 0\nnombre = "Nexo"\nactivo = True\nprint(nombre, puntos)',
    realWorld: 'Cada campo de un formulario, cada configuración de usuario, cada contador de visitas — todos son variables en producción.',
  },

  number: {
    title:     'OPERACIONES NUMÉRICAS — int y float',
    theory:    'Python distingue enteros (int) y decimales (float). La división / siempre produce float. La división entera // descarta decimales. El módulo % retorna el resto — fundamental para detectar pares, múltiplos y ciclos.',
    example:   'print(7 / 2)   # 3.5\nprint(7 // 2)  # 3\nprint(7 % 2)   # 1',
    realWorld: 'Los sistemas financieros usan Decimal (más preciso que float) para evitar errores de redondeo en pagos.',
  },

  int: {
    title:     'ENTEROS — int',
    theory:    'int es el tipo de dato para números enteros sin decimal. Python maneja enteros de tamaño arbitrario — no hay overflow. La función int() convierte strings o floats a entero (trunca, no redondea).',
    example:   'x = 42\nresultado = int("100")\nprint(x + resultado)  # 142',
    realWorld: 'Los IDs de usuarios, contadores de intentos y niveles de dificultad siempre son enteros.',
  },

  'int()': {
    title:     'CONVERSIÓN A ENTERO — int()',
    theory:    'int() convierte un string o float a entero. Si el string no es un número válido, lanza ValueError. int("3.7") falla — primero convierte a float: int(float("3.7")). Siempre valida la entrada antes de convertir.',
    example:   'edad = int(input("Edad: "))\nprint(type(edad))  # <class \'int\'>\nprint(edad * 2)',
    realWorld: 'Toda entrada de usuario es string — int() es el puente entre lo que escribe el usuario y lo que calcula el programa.',
  },

  int_conversion: {
    title:     'CONVERSIÓN A ENTERO — int()',
    theory:    'int() convierte strings y floats a entero. Trunca decimales (no redondea). Falla con ValueError si el string contiene letras. Úsalo siempre que necesites operar matemáticamente con input() del usuario.',
    example:   'raw = input("Nivel: ")   # "7"\nnivel = int(raw)          # 7\nprint(nivel + 1)          # 8',
    realWorld: 'Formularios web, parseo de CSVs y procesamiento de APIs siempre requieren conversión de tipos.',
  },

  float: {
    title:     'DECIMALES — float',
    theory:    'float almacena números con parte decimal usando punto flotante IEEE 754. La división / siempre retorna float. float() convierte strings y enteros. Cuidado: 0.1 + 0.2 ≠ 0.3 exactamente — es una limitación del hardware.',
    example:   'precio = 19.99\nimpuesto = precio * 0.21\nprint(round(precio + impuesto, 2))  # 24.19',
    realWorld: 'Cálculos de precios, coordenadas GPS, métricas de rendimiento — todos usan float.',
  },

  boolean: {
    title:     'BIFURCACIÓN TÁCTICA — Booleanos',
    theory:    'True y False son los únicos valores booleanos. Los operadores de comparación (==, !=, <, >) producen booleanos. La lógica de todo programa se reduce a decisiones True/False.',
    example:   'def es_par(n):\n    return n % 2 == 0\n\nprint(es_par(4))   # True\nprint(es_par(7))   # False',
    realWorld: 'Los sistemas de autenticación, permisos y filtros operan sobre condiciones booleanas.',
  },

  string: {
    title:     'CADENAS DE TEXTO — Strings',
    theory:    'Un string es una secuencia inmutable de caracteres. Accedés a posiciones con índices (0 es el primero, -1 es el último). Los f-strings (f"Hola {variable}") son la forma moderna de formatear texto en Python.',
    example:   'codigo = "nexo"\nprint(codigo[0])      # n\nprint(codigo.upper())  # NEXO\nprint(f"Bienvenido al {codigo}")',
    realWorld: 'Todo procesamiento de texto — detección de spam, traducción automática, análisis de sentimiento — opera sobre strings.',
  },

  strings: {
    title:     'CADENAS DE TEXTO — Strings',
    theory:    'Los strings en Python son inmutables — cada operación que "modifica" un string crea uno nuevo. Los métodos .strip(), .split(), .replace(), .join() son los más usados en producción para limpiar y transformar texto.',
    example:   'texto = "  hola mundo  "\nprint(texto.strip())         # "hola mundo"\nprint(texto.split())         # ["hola", "mundo"]',
    realWorld: 'Parseo de logs, procesamiento de formularios, generación de reportes — todo empieza con manipulación de strings.',
  },

  // ── F-strings ─────────────────────────────────────────────────────────────

  'f-string': {
    title:     'INTERPOLACIÓN DINÁMICA — f-strings',
    theory:    'Los f-strings (f"...") permiten insertar variables y expresiones directamente en un string usando llaves {}. Son más legibles y rápidos que concatenar con +. Dentro de {} podés poner cualquier expresión Python válida.',
    example:   'nombre = "Alex"\nnivel = 7\nprint(f"Operador {nombre} — Nivel {nivel}")\nprint(f"XP: {nivel * 100}")',
    realWorld: 'Generación de mensajes personalizados, construcción de URLs, formateo de reportes — los f-strings son el estándar en código Python moderno.',
  },

  'f-strings': {
    title:     'INTERPOLACIÓN DINÁMICA — f-strings',
    theory:    'Los f-strings permiten insertar variables y expresiones en texto de forma legible. Prefijo f antes de las comillas. Las expresiones dentro de {} se evalúan en tiempo de ejecución.',
    example:   'precio = 29.99\nprint(f"Total: ${precio:.2f}")\nprint(f"Doble: {precio * 2:.2f}")',
    realWorld: 'Templates de email, generación de HTML, logs de aplicación — el f-string reemplaza el formateo manual.',
  },

  f_string: {
    title:     'INTERPOLACIÓN DINÁMICA — f-strings',
    theory:    'Los f-strings son la forma más limpia de combinar texto y variables. Prefijo f, variables entre llaves. Soportan formato numérico (:.2f), alineación ({valor:>10}) y expresiones completas.',
    example:   'mision = "Alfa-7"\npuntos = 1250\nprint(f"[{mision}] Puntos: {puntos:,}")  # [Alfa-7] Puntos: 1,250',
    realWorld: 'Interfaces de usuario, generación de contenido dinámico, formateo de datos para APIs.',
  },

  // ── Control de flujo ──────────────────────────────────────────────────────

  if_else: {
    title:     'CONTROL DE FLUJO — if / elif / else',
    theory:    'El if bifurca la ejecución basándose en una condición. elif encadena condiciones adicionales. else captura todos los casos restantes. La indentación (4 espacios) define qué pertenece a cada bloque — no es estética, es sintaxis obligatoria.',
    example:   'nivel = 8\nif nivel >= 10:\n    rango = "Elite"\nelif nivel >= 5:\n    rango = "Activo"\nelse:\n    rango = "Recruit"',
    realWorld: 'Los motores de reglas de negocio (precios, descuentos, clasificaciones) son cadenas de if/elif/else.',
  },

  if: {
    title:     'DECISIÓN TÁCTICA — if',
    theory:    'if evalúa una condición y ejecuta el bloque indentado si es True. Puede combinarse con elif y else para manejar múltiples casos. Las condiciones usan ==, !=, <, >, <=, >= y operadores lógicos and, or, not.',
    example:   'puntos = 85\nif puntos >= 90:\n    print("Rango A")\nelif puntos >= 70:\n    print("Rango B")\nelse:\n    print("Rango C")',
    realWorld: 'Validaciones de formularios, cálculo de descuentos, verificación de permisos — toda lógica condicional.',
  },

  'if/else': {
    title:     'CONTROL DE FLUJO — if / else',
    theory:    'El if ejecuta código cuando la condición es True; el else ejecuta cuando es False. Juntos cubren todos los casos posibles. La indentación (4 espacios) es obligatoria — define qué instrucciones pertenecen a cada rama.',
    example:   'temperatura = 38.5\nif temperatura > 37.5:\n    print("Temperatura elevada")\nelse:\n    print("Temperatura normal")',
    realWorld: 'Toda validación binaria: acceso permitido/denegado, operación exitosa/fallida, usuario activo/inactivo.',
  },

  'if/elif/else': {
    title:     'CONTROL DE FLUJO — if / elif / else',
    theory:    'elif permite encadenar múltiples condiciones mutuamente excluyentes. Python evalúa de arriba hacia abajo y ejecuta solo el primer bloque cuya condición sea True. El else es el caso por defecto.',
    example:   'score = 72\nif score >= 90:   grado = "A"\nelif score >= 80: grado = "B"\nelif score >= 70: grado = "C"\nelse:            grado = "F"',
    realWorld: 'Clasificación de clientes, asignación de descuentos por tramo, routing de peticiones HTTP.',
  },

  condicionales: {
    title:     'CONTROL DE FLUJO — Condicionales',
    theory:    'Las condicionales dirigen el flujo del programa según condiciones. Python evalúa la expresión booleana y ejecuta el bloque correspondiente. Podés anidar if dentro de if para condiciones complejas — pero más de 2 niveles suele indicar que hay que refactorizar.',
    example:   'x = 15\nif x > 0:\n    if x % 2 == 0:\n        print("Positivo par")\n    else:\n        print("Positivo impar")',
    realWorld: 'Lógica de negocio, validación de datos, routing de aplicaciones.',
  },

  // ── Bucles ────────────────────────────────────────────────────────────────

  for_loop: {
    title:     'PROTOCOLO DE ITERACIÓN — Bucles for',
    theory:    'Un bucle for ejecuta el mismo bloque para cada elemento de una secuencia. range(5) genera 0,1,2,3,4. Es la herramienta más usada en Python para procesar colecciones sin repetir código manualmente.',
    example:   'for i in range(3):\n    print(f"Ronda {i+1}")\n# Ronda 1 / Ronda 2 / Ronda 3',
    realWorld: 'Los algoritmos de recomendación iteran sobre millones de registros con bucles como este.',
  },

  for: {
    title:     'ITERACIÓN — Bucle for',
    theory:    'for itera sobre cualquier secuencia: listas, strings, rangos, diccionarios. La variable de iteración toma el valor de cada elemento en cada vuelta. Podés usar enumerate() para obtener índice y valor simultáneamente.',
    example:   'misiones = ["Alfa", "Beta", "Gamma"]\nfor i, mision in enumerate(misiones):\n    print(f"{i+1}. {mision}")',
    realWorld: 'Procesamiento por lotes, generación de reportes, transformación de datos — el for es el caballo de batalla del análisis.',
  },

  while_loop: {
    title:     'BUCLE CONDICIONAL — while',
    theory:    'El while ejecuta un bloque mientras su condición sea True. No sabe cuántas veces iterará — depende del estado. Requiere que algo dentro del bucle cambie la condición, o se convierte en bucle infinito.',
    example:   'intentos = 0\nwhile intentos < 3:\n    print("Intento", intentos + 1)\n    intentos += 1',
    realWorld: 'Los servidores web usan while True para escuchar peticiones hasta que se apagan.',
  },

  while: {
    title:     'BUCLE CONDICIONAL — while',
    theory:    'while repite mientras la condición sea True. Usalo cuando no sabés de antemano cuántas iteraciones necesitás. El patrón while True con break es común para menús interactivos y loops de servidor.',
    example:   'clave = ""\nwhile clave != "nexo":\n    clave = input("Contraseña: ")\nprint("Acceso concedido")',
    realWorld: 'Reintentos automáticos, polling de APIs, juegos con loop principal.',
  },

  break: {
    title:     'INTERRUPCIÓN DE BUCLE — break',
    theory:    'break sale inmediatamente del bucle que lo contiene. Se usa cuando encontrás lo que buscabas o cuando una condición hace innecesario seguir iterando. Hace el código más eficiente al evitar iteraciones innecesarias.',
    example:   'numeros = [3, 7, 2, 9, 4]\nfor n in numeros:\n    if n > 8:\n        print(f"Encontrado: {n}")\n        break  # para en 9',
    realWorld: 'Búsqueda en listas, validación temprana, salida de loops de reintento cuando la operación tiene éxito.',
  },

  continue: {
    title:     'SALTAR ITERACIÓN — continue',
    theory:    'continue salta el resto del cuerpo del bucle para la iteración actual y pasa a la siguiente. A diferencia de break, no sale del bucle — solo omite lo que queda de esa vuelta.',
    example:   'for i in range(6):\n    if i % 2 == 0:\n        continue  # salta pares\n    print(i)  # 1 3 5',
    realWorld: 'Filtrar datos inválidos, omitir registros con errores, saltar elementos ya procesados.',
  },

  // ── Funciones ─────────────────────────────────────────────────────────────

  function: {
    title:     'MÓDULOS TÁCTICOS — Funciones',
    theory:    'Una función es un bloque de código reutilizable con nombre. def es la directiva de creación. Los parámetros son las entradas, return es la salida. Una función bien definida hace UNA cosa y la hace bien.',
    example:   'def calcular_xp(nivel, bonus):\n    return nivel * 100 + bonus\n\nprint(calcular_xp(5, 50))  # 550',
    realWorld: 'Las APIs que usás cada día (Google Maps, Stripe, Anthropic) son colecciones de funciones expuestas al mundo.',
  },

  def: {
    title:     'DEFINICIÓN DE FUNCIÓN — def',
    theory:    'def declara una función. El nombre debe ser descriptivo (verbo + sustantivo). Los parámetros van entre paréntesis. El cuerpo va indentado. Sin return explícito, la función retorna None automáticamente.',
    example:   'def saludar(nombre, nivel=1):\n    """Genera saludo personalizado."""\n    return f"Bienvenido, {nombre} (Niv. {nivel})"\n\nprint(saludar("Alex", 5))',
    realWorld: 'Toda lógica de negocio que se repite más de una vez debería estar en una función.',
  },

  return_stmt: {
    title:     'PROTOCOLO DE RETORNO — return',
    theory:    'return termina la función y entrega un valor al código que la llamó. Sin return explícito, Python retorna None. Una función puede tener múltiples return en diferentes ramas de if/else.',
    example:   'def clasificar(puntos):\n    if puntos >= 90: return "A"\n    if puntos >= 70: return "B"\n    return "C"\n\nresultado = clasificar(85)  # "B"',
    realWorld: 'Cada función de una API retorna datos al cliente — ese return es el contrato entre servidor y consumidor.',
  },

  return: {
    title:     'VALOR DE RETORNO — return',
    theory:    'return envía un valor desde la función hacia quien la llamó. Puede retornar cualquier tipo: número, string, lista, dict, None. return sin valor retorna None. La función termina al ejecutar cualquier return.',
    example:   'def maximo(a, b):\n    if a > b:\n        return a\n    return b\n\nprint(maximo(3, 7))  # 7',
    realWorld: 'Funciones de cálculo, validadores, transformadores de datos — todos usan return para entregar su resultado.',
  },

  lambda: {
    title:     'FUNCIÓN ANÓNIMA — lambda',
    theory:    'lambda crea funciones de una sola expresión sin nombre. Útil como argumento de sorted(), map(), filter(). La sintaxis es: lambda parámetros: expresión. No puede contener múltiples líneas ni return explícito.',
    example:   'doble = lambda x: x * 2\nprint(doble(5))  # 10\n\nnombres = ["Beta", "Alfa", "Gamma"]\nnombres.sort(key=lambda s: len(s))',
    realWorld: 'Funciones de transformación en pipelines de datos, callbacks en UIs, criterios de ordenamiento dinámico.',
  },

  // ── Colecciones ───────────────────────────────────────────────────────────

  list: {
    title:     'COLECCIONES ORDENADAS — Listas',
    theory:    'Una lista guarda múltiples elementos en orden. Se accede por índice [0], se modifica con .append() y .remove(), se itera con for. Las listas son mutables — podés cambiar su contenido después de crearlas.',
    example:   'mision = ["Alfa", "Beta", "Gamma"]\nmision.append("Delta")\nprint(len(mision))   # 4\nprint(mision[0])     # Alfa',
    realWorld: 'Listas de reproducción, carritos de compra, feeds de redes sociales — son listas en producción.',
  },

  listas: {
    title:     'COLECCIONES ORDENADAS — Listas',
    theory:    'Las listas en Python son dinámicas — crecen y se contraen. .append() agrega al final, .insert(i, x) en posición específica, .pop() elimina el último. sorted() retorna una nueva lista ordenada sin modificar la original.',
    example:   'scores = [85, 92, 67, 88]\nscores.append(95)\nprint(max(scores))     # 95\nprint(sorted(scores))  # [67, 85, 88, 92, 95]',
    realWorld: 'Rankings, historial de acciones, colas de procesamiento — todas son listas con operaciones específicas.',
  },

  dict: {
    title:     'REGISTROS CLAVE-VALOR — Diccionarios',
    theory:    'Un diccionario mapea claves únicas a valores. Acceso en O(1) — instantáneo sin importar el tamaño. Las claves son inmutables (strings, números), los valores pueden ser cualquier tipo.',
    example:   'operador = {"nombre": "Alex", "nivel": 7}\nprint(operador["nombre"])        # Alex\nprint(operador.get("xp", 0))    # 0 (default)',
    realWorld: 'Cada response JSON de una API es un diccionario serializado.',
  },

  diccionarios: {
    title:     'REGISTROS CLAVE-VALOR — Diccionarios',
    theory:    'Los diccionarios son la estructura de datos más versátil de Python. .items() itera clave-valor, .keys() solo claves, .values() solo valores. .get(clave, default) evita KeyError cuando la clave puede no existir.',
    example:   'config = {"debug": True, "nivel": 3}\nfor clave, valor in config.items():\n    print(f"{clave}: {valor}")',
    realWorld: 'Configuraciones de aplicación, respuestas de API, registros de base de datos — todos son diccionarios.',
  },

  tuplas: {
    title:     'SECUENCIAS INMUTABLES — Tuplas',
    theory:    'Las tuplas son como listas pero inmutables — no podés modificar sus elementos una vez creadas. Se usan cuando los datos no deben cambiar: coordenadas, fechas, pares clave-valor. El desempaquetado hace el código más limpio.',
    example:   'punto = (3, 7)\nx, y = punto\nprint(f"X={x}, Y={y}")\n\ndimensiones = (1920, 1080)\nancho, alto = dimensiones',
    realWorld: 'Coordenadas geográficas, dimensiones fijas, pares (clave, valor) que retorna .items() de un dict.',
  },

  sets: {
    title:     'CONJUNTOS ÚNICOS — Sets',
    theory:    'Un set almacena elementos únicos sin orden. Elimina duplicados automáticamente. Las operaciones de conjunto (unión |, intersección &, diferencia -) son extremadamente eficientes. La búsqueda "in" es O(1) como en los dicts.',
    example:   'vistos = {1, 2, 3}\nnuevos = {3, 4, 5}\nprint(vistos & nuevos)  # {3}  intersección\nprint(vistos | nuevos)  # {1,2,3,4,5} unión',
    realWorld: 'Deduplicación de datos, verificación de permisos, análisis de audiencias (usuarios únicos).',
  },

  // ── Comprehensions ────────────────────────────────────────────────────────

  comprehension: {
    title:     'CONSTRUCCIÓN COMPACTA — List Comprehension',
    theory:    'Una list comprehension crea una lista en una sola línea combinando transformación y filtrado. Es más rápida que un bucle for equivalente y más legible. La sintaxis es [expresión for elemento in iterable if condición].',
    example:   'numeros = [1, 2, 3, 4, 5, 6]\npares = [n for n in numeros if n % 2 == 0]\ncuadrados = [n**2 for n in range(5)]\nprint(pares)     # [2, 4, 6]\nprint(cuadrados) # [0, 1, 4, 9, 16]',
    realWorld: 'Transformación de listas de datos, filtrado de registros, generación de estructuras — el estilo Python idiomático.',
  },

  // ── Slicing ───────────────────────────────────────────────────────────────

  slicing: {
    title:     'CORTE DE SECUENCIAS — Slicing',
    theory:    'El slicing extrae partes de listas, strings y tuplas con [inicio:fin:paso]. inicio incluido, fin excluido. Índices negativos cuentan desde el final. Omitir un valor usa el inicio/fin de la secuencia.',
    example:   'datos = [10, 20, 30, 40, 50]\nprint(datos[1:4])   # [20, 30, 40]\nprint(datos[:3])    # [10, 20, 30]\nprint(datos[::-1])  # [50, 40, 30, 20, 10]',
    realWorld: 'Paginación de resultados, extracción de fragmentos de texto, inversión de secuencias.',
  },

  slicing_inverso: {
    title:     'INVERSIÓN POR SLICING — [::-1]',
    theory:    'El paso negativo en slicing recorre la secuencia al revés. [::-1] invierte una lista o string sin modificar el original. Es más eficiente y legible que construir la inversión manualmente con un bucle.',
    example:   'texto = "Python"\nprint(texto[::-1])   # nohtyP\n\nlista = [1, 2, 3, 4, 5]\nprint(lista[::-1])   # [5, 4, 3, 2, 1]',
    realWorld: 'Verificación de palíndromos, procesamiento de secuencias genéticas, análisis de series temporales inversas.',
  },

  // ── Excepciones ───────────────────────────────────────────────────────────

  try_except: {
    title:     'MANEJO DE ERRORES — try / except',
    theory:    'try ejecuta código que puede fallar. except captura el error y permite manejarlo en lugar de que el programa se cierre. Podés capturar tipos específicos (ValueError, TypeError) o usar except Exception para capturar cualquier error.',
    example:   'try:\n    numero = int(input("Ingresa un número: "))\n    print(f"El doble es {numero * 2}")\nexcept ValueError:\n    print("Eso no es un número válido")',
    realWorld: 'Llamadas a APIs externas, lectura de archivos, parseo de datos — todo código de producción maneja excepciones.',
  },

  try: {
    title:     'BLOQUE PROTEGIDO — try',
    theory:    'try delimita el código que puede lanzar una excepción. Si ocurre un error dentro del try, Python salta directamente al except correspondiente. Lo que está fuera del bloque try no está protegido.',
    example:   'try:\n    resultado = 10 / 0\nexcept ZeroDivisionError:\n    print("No se puede dividir por cero")\nprint("El programa continúa")',
    realWorld: 'Operaciones de I/O, llamadas a servicios externos, conversiones de datos que pueden fallar.',
  },

  except: {
    title:     'CAPTURA DE ERRORES — except',
    theory:    'except captura excepciones específicas del try. Podés capturar múltiples tipos: except (ValueError, TypeError). Usar "except Exception as e" captura todo y guarda el error en e. Nunca uses except sin tipo — enmascara errores reales.',
    example:   'try:\n    x = int("no_es_numero")\nexcept ValueError as e:\n    print(f"Error: {e}")\nexcept Exception:\n    print("Error inesperado")',
    realWorld: 'Validación robusta de entradas, conexiones de red con reintentos, parseo de datos externos.',
  },

  raise: {
    title:     'LANZAR EXCEPCIÓN — raise',
    theory:    'raise lanza una excepción manualmente. Usalo para señalar condiciones inválidas en tu código. Podés lanzar excepciones estándar (ValueError, TypeError) o crear clases de error propias heredando de Exception.',
    example:   'def dividir(a, b):\n    if b == 0:\n        raise ValueError("Divisor no puede ser cero")\n    return a / b\n\ndividir(10, 0)  # lanza ValueError',
    realWorld: 'Validación de reglas de negocio, contratos de función, señalización de estados ilegales del sistema.',
  },

  finally: {
    title:     'BLOQUE GARANTIZADO — finally',
    theory:    'finally se ejecuta siempre, ocurra o no una excepción. Se usa para liberar recursos (cerrar archivos, conexiones de base de datos, sockets) independientemente de si el código tuvo éxito o falló.',
    example:   'archivo = None\ntry:\n    archivo = open("datos.txt")\n    contenido = archivo.read()\nexcept FileNotFoundError:\n    print("Archivo no encontrado")\nfinally:\n    if archivo:\n        archivo.close()  # siempre se cierra',
    realWorld: 'Cierre de conexiones a bases de datos, liberación de locks, limpieza de recursos temporales.',
  },

  'valueerror': {
    title:     'EXCEPCIÓN DE VALOR — ValueError',
    theory:    'ValueError se lanza cuando una función recibe un valor de tipo correcto pero con un valor inapropiado. Ejemplo: int("abc") — el argumento es string (tipo correcto para int()), pero su valor no puede convertirse a entero.',
    example:   'try:\n    x = int("abc")\nexcept ValueError:\n    print("Valor no convertible a entero")\n\ntry:\n    [1,2,3].remove(99)\nexcept ValueError:\n    print("Elemento no encontrado")',
    realWorld: 'Validación de formularios, parseo de datos de usuario, verificación de parámetros de función.',
  },

  'typeerror': {
    title:     'EXCEPCIÓN DE TIPO — TypeError',
    theory:    'TypeError ocurre cuando una operación se aplica a un tipo de dato incorrecto. Ejemplo: "hola" + 5 mezcla string con int. Python no hace conversión automática — el programador debe hacerla explícitamente.',
    example:   'try:\n    resultado = "nivel: " + 7\nexcept TypeError:\n    resultado = "nivel: " + str(7)\nprint(resultado)  # nivel: 7',
    realWorld: 'APIs que reciben tipos inesperados, operaciones sobre datos sin validar, interacción entre módulos.',
  },

  'zerodivisionerror': {
    title:     'DIVISIÓN POR CERO — ZeroDivisionError',
    theory:    'ZeroDivisionError se lanza al dividir por cero (a / 0 o a // 0 o a % 0). Es una de las excepciones más comunes. Siempre validá el divisor antes de dividir, o capturá la excepción.',
    example:   'def porcentaje(parte, total):\n    try:\n        return round(parte / total * 100, 1)\n    except ZeroDivisionError:\n        return 0.0\n\nprint(porcentaje(3, 0))  # 0.0',
    realWorld: 'Cálculo de tasas, porcentajes, promedios — siempre pueden recibir denominador cero.',
  },

  'indexerror': {
    title:     'ÍNDICE FUERA DE RANGO — IndexError',
    theory:    'IndexError ocurre al acceder a un índice que no existe en una lista o string. Si la lista tiene 3 elementos (índices 0,1,2), acceder al índice 3 lanza IndexError. Validá len() antes de acceder por índice.',
    example:   'lista = [10, 20, 30]\ntry:\n    print(lista[5])\nexcept IndexError:\n    print(f"Solo hay {len(lista)} elementos")',
    realWorld: 'Paginación, acceso a resultados de búsqueda, procesamiento de listas de tamaño variable.',
  },

  // ── OOP ───────────────────────────────────────────────────────────────────

  'class': {
    title:     'DISEÑO ORIENTADO A OBJETOS — Clases',
    theory:    'Una clase es un plano para crear objetos. Define atributos (datos) y métodos (comportamiento). __init__ es el constructor que se ejecuta al crear cada instancia. self referencia al objeto actual.',
    example:   'class Operador:\n    def __init__(self, nombre, nivel):\n        self.nombre = nombre\n        self.nivel = nivel\n\n    def presentar(self):\n        return f"{self.nombre} — Niv.{self.nivel}"\n\nop = Operador("Alex", 5)\nprint(op.presentar())',
    realWorld: 'Modelos de datos (User, Product, Order), componentes de UI, entidades de juego — todo el software moderno está basado en clases.',
  },

  clases: {
    title:     'DISEÑO ORIENTADO A OBJETOS — Clases',
    theory:    'Las clases agrupan datos y comportamiento relacionados. Cada objeto creado desde la clase (instancia) tiene su propio estado. Los métodos son funciones que operan sobre self — el objeto concreto.',
    example:   'class Rectangulo:\n    def __init__(self, ancho, alto):\n        self.ancho = ancho\n        self.alto = alto\n\n    def area(self):\n        return self.ancho * self.alto\n\nr = Rectangulo(4, 6)\nprint(r.area())  # 24',
    realWorld: 'Frameworks web (Django, FastAPI) modelan usuarios, productos y sesiones como clases.',
  },

  '__init__': {
    title:     'CONSTRUCTOR — __init__',
    theory:    '__init__ es el método especial que Python llama automáticamente al crear un objeto. Recibe self (el objeto nuevo) y los parámetros que definís. Es donde inicializás los atributos del objeto.',
    example:   'class Mision:\n    def __init__(self, nombre, dificultad=1):\n        self.nombre = nombre\n        self.dificultad = dificultad\n        self.completada = False\n\nm = Mision("Protocolo Alfa", dificultad=3)',
    realWorld: 'El constructor inicializa el estado interno de cada objeto — usuarios, sesiones, conexiones de base de datos.',
  },

  self: {
    title:     'REFERENCIA PROPIA — self',
    theory:    'self es la referencia al objeto actual dentro de sus métodos. Python lo pasa automáticamente como primer parámetro. self.atributo accede o modifica el estado del objeto concreto que está ejecutando el método.',
    example:   'class Contador:\n    def __init__(self):\n        self.valor = 0\n\n    def incrementar(self):\n        self.valor += 1\n        return self.valor\n\nc = Contador()\nprint(c.incrementar())  # 1\nprint(c.incrementar())  # 2',
    realWorld: 'Cada objeto mantiene su propio estado a través de self — dos instancias de la misma clase no comparten atributos.',
  },

  herencia: {
    title:     'HERENCIA — Reutilización de Clases',
    theory:    'La herencia permite que una clase (hija) reutilice el código de otra (padre). La clase hija puede agregar atributos y métodos nuevos, o sobreescribir los heredados. super() llama al constructor o método del padre.',
    example:   'class Animal:\n    def __init__(self, nombre):\n        self.nombre = nombre\n    def hablar(self): return "..."\n\nclass Perro(Animal):\n    def hablar(self): return "Guau"\n\np = Perro("Rex")\nprint(p.hablar())  # Guau',
    realWorld: 'Jerarquías de usuarios (Usuario → Operador → Admin), componentes de UI, excepciones personalizadas.',
  },

  encapsulación: {
    title:     'ENCAPSULACIÓN — Control de Acceso',
    theory:    'La encapsulación oculta los detalles internos de un objeto. En Python, el prefijo _ indica "privado por convención" (no es enforcement real). Las propiedades @property permiten acceso controlado con lógica de validación.',
    example:   'class Cuenta:\n    def __init__(self, saldo):\n        self._saldo = saldo  # convención privado\n\n    @property\n    def saldo(self):\n        return self._saldo\n\nc = Cuenta(100)\nprint(c.saldo)  # 100',
    realWorld: 'APIs bien diseñadas exponen solo lo necesario — el estado interno está protegido del uso incorrecto externo.',
  },

  polimorfismo: {
    title:     'POLIMORFISMO — Mismo Mensaje, Distintas Respuestas',
    theory:    'El polimorfismo permite que objetos de distintas clases respondan al mismo método de formas diferentes. En Python es natural gracias al duck typing — si el objeto tiene el método, funciona sin importar la clase.',
    example:   'class Circulo:\n    def area(self): return 3.14 * 5**2\n\nclass Cuadrado:\n    def area(self): return 4**2\n\nformas = [Circulo(), Cuadrado()]\nfor f in formas:\n    print(f.area())  # funciona para ambas',
    realWorld: 'Plugins, adaptadores de bases de datos, renderers de UI — todos usan polimorfismo para intercambiabilidad.',
  },

  // ── Built-ins esenciales ──────────────────────────────────────────────────

  print_fn: {
    title:     'SALIDA DE DATOS — print()',
    theory:    'print() muestra datos en stdout. Acepta múltiples argumentos separados por comas. sep define el separador (default: espacio), end define el terminador (default: nueva línea). Los f-strings son la forma moderna de formatear.',
    example:   'x = 42\nprint("Valor:", x)          # Valor: 42\nprint(f"Resultado: {x * 2}")  # Resultado: 84',
    realWorld: 'Los sistemas de logging en producción funcionan como print() pero con niveles (DEBUG, INFO, ERROR).',
  },

  input_fn: {
    title:     'ENTRADA DEL OPERADOR — input()',
    theory:    'input() detiene la ejecución y espera texto del usuario. SIEMPRE retorna string — aunque el usuario escriba 42, obtienes "42". Para operar numéricamente debés convertir: int(input()) o float(input()).',
    example:   'nombre = input("Callsign: ")\nedad = int(input("Nivel: "))\nprint(f"Operador {nombre}, Nivel {edad}")',
    realWorld: 'Los CLIs profesionales (git, pip, docker) procesan inputs del operador con este mismo principio.',
  },

  range_fn: {
    title:     'GENERADOR DE SECUENCIAS — range()',
    theory:    'range(stop) genera 0..stop-1. range(start, stop) genera start..stop-1. range(start, stop, step) controla el paso — negativo para contar hacia atrás. Es un generador perezoso, no crea la lista en memoria.',
    example:   'list(range(3))        # [0, 1, 2]\nlist(range(1, 4))     # [1, 2, 3]\nlist(range(0, 10, 2)) # [0, 2, 4, 6, 8]',
    realWorld: 'Índices de bases de datos, offsets de paginación, lotes de procesamiento.',
  },

  'range()': {
    title:     'GENERADOR DE SECUENCIAS — range()',
    theory:    'range() es el generador de secuencias más usado de Python. No crea una lista — genera valores uno a uno (eficiente en memoria). Siempre que necesités iterar N veces o sobre una secuencia numérica, usá range().',
    example:   'for i in range(5, 0, -1):\n    print(i, end=" ")  # 5 4 3 2 1\nprint("¡Despegue!")',
    realWorld: 'Countdown timers, índices de procesamiento por lotes, generación de IDs secuenciales.',
  },

  'len()': {
    title:     'LONGITUD DE SECUENCIA — len()',
    theory:    'len() retorna la cantidad de elementos de cualquier secuencia: string (caracteres), lista (elementos), dict (claves), set (miembros). Es O(1) — instantáneo sin importar el tamaño. Esencial para validaciones y loops.',
    example:   'texto = "nexo"\nprint(len(texto))      # 4\n\nlista = [1, 2, 3, 4, 5]\nprint(len(lista))      # 5\nif len(lista) > 3:\n    print("Lista larga")',
    realWorld: 'Validación de longitud de contraseñas, conteo de registros, límites de paginación.',
  },

  'sorted()': {
    title:     'ORDENAMIENTO — sorted()',
    theory:    'sorted() retorna una nueva lista ordenada sin modificar el original. El parámetro key acepta una función para definir el criterio. reverse=True ordena descendente. Funciona sobre cualquier iterable.',
    example:   'nums = [3, 1, 4, 1, 5]\nprint(sorted(nums))           # [1, 1, 3, 4, 5]\nprint(sorted(nums, reverse=True))  # [5, 4, 3, 1, 1]\n\nnombres = ["Beta", "Alfa"]\nprint(sorted(nombres, key=len))',
    realWorld: 'Rankings de usuarios, ordenamiento de resultados de búsqueda, reportes ordenados por criterio.',
  },

  'max()': {
    title:     'VALOR MÁXIMO — max()',
    theory:    'max() retorna el mayor valor de un iterable o entre argumentos separados. Con key puede encontrar el máximo según un criterio personalizado. min() hace lo opuesto. Ambas lanzan ValueError si la secuencia está vacía.',
    example:   'print(max([3, 1, 4, 1, 5]))  # 5\nprint(max(10, 20, 15))       # 20\n\noperadores = [{"nombre": "A", "xp": 500}, {"nombre": "B", "xp": 800}]\nmejor = max(operadores, key=lambda o: o["xp"])',
    realWorld: 'Encontrar el mejor resultado, el registro más reciente, el precio más alto en un catálogo.',
  },

  'round()': {
    title:     'REDONDEO — round()',
    theory:    'round(n) redondea al entero más cercano. round(n, decimales) redondea a la cantidad de decimales especificada. Usa redondeo bancario (half-even) — round(0.5) = 0, round(1.5) = 2. Para precisión financiera, usá Decimal.',
    example:   'print(round(3.7))     # 4\nprint(round(3.14159, 2))  # 3.14\nprecio = 19.995\nprint(round(precio, 2))   # 20.0',
    realWorld: 'Cálculo de precios, presentación de métricas, estadísticas redondeadas.',
  },

  'abs()': {
    title:     'VALOR ABSOLUTO — abs()',
    theory:    'abs() retorna el valor absoluto de un número — siempre positivo. Funciona con int, float y complex. Útil para calcular distancias, diferencias y errores donde el signo no importa.',
    example:   'print(abs(-5))    # 5\nprint(abs(3.7))   # 3.7\n\ntemperatura_actual = 22\ntemperatura_objetivo = 25\ndiferencia = abs(temperatura_actual - temperatura_objetivo)\nprint(f"Diferencia: {diferencia}°C")  # 3°C',
    realWorld: 'Cálculo de distancias, márgenes de error, diferencias entre valores esperados y reales.',
  },

  // ── Módulos & I/O ─────────────────────────────────────────────────────────

  modulo: {
    title:     'OPERADOR MÓDULO — %',
    theory:    'El operador % retorna el resto de la división entera. Es fundamental para detectar pares/impares (n % 2), ciclos (i % n), y dividir en grupos. También se usa en formateo de strings antiguo (ya reemplazado por f-strings).',
    example:   'print(10 % 3)   # 1  (resto de 10÷3)\nprint(8 % 2)    # 0  (8 es par)\nfor i in range(6):\n    if i % 2 == 0: print(i, "par")',
    realWorld: 'Rotación de turnos, paginación, semanas de año, distribución round-robin de carga.',
  },

  'módulo %': {
    title:     'OPERADOR MÓDULO — %',
    theory:    'El % calcula el resto de la división. Si n % 2 == 0, n es par. Si n % k == 0, n es múltiplo de k. Es O(1) — una operación básica del procesador, ultra eficiente.',
    example:   'def es_bisiesto(año):\n    return (año % 4 == 0 and año % 100 != 0) or (año % 400 == 0)\n\nprint(es_bisiesto(2024))  # True\nprint(es_bisiesto(1900))  # False',
    realWorld: 'Años bisiestos, validación de IDs, distribución equitativa de carga, hashing.',
  },

  '//': {
    title:     'DIVISIÓN ENTERA — //',
    theory:    '// realiza división y descarta la parte decimal (trunca hacia abajo). A diferencia de int(a/b), // maneja correctamente los negativos. Usalo cuando necesités saber cuántas veces cabe algo exactamente.',
    example:   'print(17 // 5)   # 3  (17 ÷ 5 = 3.4 → 3)\nprint(-17 // 5)  # -4  (trunca hacia abajo)\n\nminutos = 137\nhoras = minutos // 60\nmins = minutos % 60\nprint(f"{horas}h {mins}m")  # 2h 17m',
    realWorld: 'Conversión de unidades, paginación (página = índice // tamaño), distribución de elementos.',
  },

  'operador **': {
    title:     'POTENCIACIÓN — **',
    theory:    '** eleva un número a una potencia. 2**10 = 1024. También funciona con floats: 2**0.5 es la raíz cuadrada. Python maneja potencias de enteros con precisión exacta (sin overflow). Equivalente a pow(base, exp).',
    example:   'print(2**8)     # 256\nprint(10**3)    # 1000\nprint(9**0.5)   # 3.0  (raíz cuadrada)\nprint(2**-1)    # 0.5',
    realWorld: 'Cálculos de interés compuesto, algoritmos de encriptación (RSA usa potencias enormes), escalas logarítmicas.',
  },

  // ── None ──────────────────────────────────────────────────────────────────

  none_como_sentinel: {
    title:     'VALOR NULO — None',
    theory:    'None es el valor nulo de Python — representa la ausencia de valor. Es el único valor de tipo NoneType. Las funciones sin return retornan None. Usá "is None" para comparar, no "== None".',
    example:   'resultado = None\n\ndef buscar(lista, objetivo):\n    for i, x in enumerate(lista):\n        if x == objetivo:\n            return i\n    return None  # no encontrado\n\nif buscar([1,2,3], 5) is None:\n    print("No encontrado")',
    realWorld: 'Campos opcionales en bases de datos, resultados de búsquedas sin coincidencia, valores por defecto de parámetros.',
  },

  // ── Métodos de string ─────────────────────────────────────────────────────

  '.split': {
    title:     'SEPARAR TEXTO — .split()',
    theory:    '.split() divide un string en una lista usando un separador. Sin argumento, separa por espacios y elimina espacios extras. Con argumento, separa por ese delimitador. .splitlines() separa por saltos de línea.',
    example:   'csv = "alfa,beta,gamma"\npartes = csv.split(",")\nprint(partes)  # ["alfa", "beta", "gamma"]\n\nfrase = "hola mundo"\nprint(frase.split())  # ["hola", "mundo"]',
    realWorld: 'Parseo de CSV, procesamiento de logs, tokenización de comandos CLI.',
  },

  '.join': {
    title:     'UNIR TEXTO — .join()',
    theory:    '.join() une una lista de strings usando el string como separador. Es el inverso de .split(). Es más eficiente que concatenar con + en un bucle — recomendado cuando unís muchos strings.',
    example:   'partes = ["alfa", "beta", "gamma"]\nresultado = ", ".join(partes)\nprint(resultado)  # alfa, beta, gamma\n\nlineas = ["línea1", "línea2"]\nprint("\\n".join(lineas))',
    realWorld: 'Generación de CSV, construcción de queries SQL, formateo de listas para display.',
  },

  '.strip': {
    title:     'LIMPIAR ESPACIOS — .strip()',
    theory:    '.strip() elimina espacios y saltos de línea del inicio y fin del string. .lstrip() solo del inicio (left), .rstrip() solo del final (right). Podés pasar un string de caracteres a eliminar: .strip("abc").',
    example:   'entrada = "   hola mundo   "\nprint(entrada.strip())   # "hola mundo"\nprint(entrada.lstrip())  # "hola mundo   "\nprint(entrada.rstrip())  # "   hola mundo"',
    realWorld: 'Limpieza de input de usuario, parseo de archivos de texto, normalización de datos.',
  },

  '.upper': {
    title:     'MAYÚSCULAS — .upper() / .lower()',
    theory:    '.upper() convierte todos los caracteres a mayúsculas. .lower() a minúsculas. Son útiles para comparaciones case-insensitive: if texto.lower() == "si". Los strings son inmutables — estos métodos retornan un nuevo string.',
    example:   'nombre = "alex"\nprint(nombre.upper())  # ALEX\nprint(nombre.lower())  # alex\n\nrespuesta = input("¿Continuar? ").lower()\nif respuesta in ("s", "si", "sí"): print("OK")',
    realWorld: 'Normalización de datos, comparaciones sin importar mayúsculas, formateo de títulos.',
  },

  '.replace': {
    title:     'REEMPLAZAR TEXTO — .replace()',
    theory:    '.replace(viejo, nuevo) retorna un nuevo string con todas las ocurrencias de "viejo" reemplazadas por "nuevo". El tercer parámetro opcional limita cuántos reemplazos hacer. No modifica el string original.',
    example:   'mensaje = "hola mundo mundo"\nprint(mensaje.replace("mundo", "nexo"))    # hola nexo nexo\nprint(mensaje.replace("mundo", "nexo", 1)) # hola nexo mundo',
    realWorld: 'Sanitización de texto, templates dinámicos, normalización de datos antes de guardar en DB.',
  },

  // ── Importar / modules ───────────────────────────────────────────────────

  import: {
    title:     'MÓDULOS — import',
    theory:    'import trae código externo a tu programa. La biblioteca estándar de Python incluye módulos para casi todo: math (matemáticas), random (aleatoriedad), datetime (fechas), os (sistema operativo). from módulo import función importa directamente.',
    example:   'import math\nprint(math.sqrt(16))     # 4.0\nprint(math.pi)           # 3.14159...\n\nfrom random import randint\nprint(randint(1, 10))    # número aleatorio',
    realWorld: 'Todo programa Python real usa imports — desde cálculos matemáticos hasta peticiones HTTP.',
  },
}

/**
 * Busca la teoría para un array de conceptos.
 * Retorna la primera entrada encontrada o null si ninguna coincide.
 */
export function getConceptTheory(concepts: string[]): ConceptEntry | null {
  for (const c of concepts) {
    const key = c.toLowerCase()
    const entry = CONCEPT_GLOSSARY[key] ?? CONCEPT_GLOSSARY[c]
    if (entry) return entry
  }
  return null
}
