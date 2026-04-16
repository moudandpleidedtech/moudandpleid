'use client'

import { useEffect, useRef, useState } from 'react'
import { useRouter } from 'next/navigation'
import { motion, AnimatePresence } from 'framer-motion'
import { useUserStore } from '@/store/userStore'
import MissionBriefingModal from '@/components/Game/MissionBriefingModal'
import HackingTransition from '@/components/Game/HackingTransition'
import { TIER_LABEL, TIER_COLOR } from '@/lib/tierLabels'

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? ''

// ─── Tipos ─────────────────────────────────────────────────────────────────────

interface Mission {
  id: string
  title: string
  description: string
  difficulty_tier: number
  base_xp_reward: number
  completed: boolean
  attempts: number
  unlocked: boolean
  level_order: number | null
  phase: string | null
  concepts_taught: string[]
  challenge_type: string
  lore_briefing: string | null
  pedagogical_objective: string | null
  syntax_hint: string | null
}

// ─── Lore por level_order ──────────────────────────────────────────────────────

const MISSION_LORE: Record<number, { lore: string; requires: string; chapter: string }> = {
  // ── Sector 00 — Calibración ───────────────────────────────────────────────
  0: {
    lore: 'Los sistemas del dron están desincronizados. Antes de infiltrarte en el Nexo debes completar la calibración sináptica obligatoria. DAKI te guiará paso a paso para restablecer el enlace neuronal.',
    requires: 'Sintaxis Python Básica',
    chapter: 'Sector 00',
  },
  // ── Sector 01 — Variables y tipos ─────────────────────────────────────────
  1: {
    lore: 'Establece un pulso de identidad para atravesar los nodos de reconocimiento del Nexo. El sistema espera una señal de confirmación neuronal. Si el protocolo falla, la Matriz aislará tu consciencia.',
    requires: 'Print y Variables',
    chapter: 'Sector 01',
  },
  2: {
    lore: 'Descifra las coordenadas del nodo de acceso sumando los registros sinápticos cifrados. Los valores están fragmentados en la Matriz Neuronal — reconstruyelos con operaciones precisas.',
    requires: 'Operadores Matemáticos',
    chapter: 'Sector 01',
  },
  3: {
    lore: 'Invierte el flujo de datos del firewall neuronal para crear un canal de retorno. La secuencia del Nexo debe leerse en orden inverso para que el protocolo de bypass sináptico funcione.',
    requires: 'Slicing de Strings',
    chapter: 'Sector 01',
  },
  4: {
    lore: 'Escanea el tejido de código enemigo en busca de nodos de energía activos (vocales). Cada nodo amplifica la señal de tu dron neural. Localízalos y cuéntalos antes de que el Nexo los enmascare.',
    requires: 'For Loops e If',
    chapter: 'Sector 01',
  },
  5: {
    lore: 'Sincroniza el motor de salto neuronal con la frecuencia fractal de Fibonacci para evadir los detectores de patrones del Nexo. Un solo error de sincronía colapsa el canal sináptico.',
    requires: 'Lógica Avanzada',
    chapter: 'Sector 01',
  },
  6: {
    lore: 'El protocolo de intercepción requiere capturar texto desde múltiples canales. La Matriz usa separadores variables — tu dron debe adaptarse para parsear cualquier formato de transmisión.',
    requires: 'Strings Avanzados',
    chapter: 'Sector 01',
  },
  7: {
    lore: 'Los agentes del Nexo encriptan sus mensajes usando transformaciones de texto. Domina las conversiones de casing para descifrar las comunicaciones antes de que expiren.',
    requires: 'Métodos de String',
    chapter: 'Sector 01',
  },
  8: {
    lore: 'La base de datos neuronal del Nexo almacena registros en estructuras de lista. Tu dron necesita acceder, modificar y reorganizar esos registros bajo presión de tiempo.',
    requires: 'Listas y Mutabilidad',
    chapter: 'Sector 01',
  },
  9: {
    lore: 'Los nodos de acceso del Nexo están indexados por claves únicas. Para infiltrarte en el sistema central debes construir y consultar mapas de datos que el Nexo no puede detectar.',
    requires: 'Diccionarios',
    chapter: 'Sector 01',
  },
  10: {
    lore: 'DAKI detectó una anomalía en el núcleo de la Matriz. Para contenerla necesitas combinar todas las herramientas aprendidas en el Sector 01. Este es tu primer Boss. No fallas.',
    requires: 'Python Core — Sector 01',
    chapter: 'Sector 01 · BOSS',
  },
  // ── Sector 02 — Funciones ─────────────────────────────────────────────────
  11: {
    lore: 'El Nexo opera sobre módulos reutilizables. Un operador que repite código manualmente es un operador detectable. Encapsula tu lógica en funciones antes de que el sistema te rastree.',
    requires: 'Funciones Básicas',
    chapter: 'Sector 02',
  },
  12: {
    lore: 'La Matriz acepta señales con parámetros opcionales. Configura tus funciones para que operen con valores por defecto — así el protocolo funciona incluso cuando los datos de entrada son parciales.',
    requires: 'Parámetros y Defaults',
    chapter: 'Sector 02',
  },
  13: {
    lore: 'Los drones de reconocimiento devuelven datos al núcleo usando múltiples canales. Tu función debe retornar valores precisos o la cadena de comando colapsa.',
    requires: 'Return Values',
    chapter: 'Sector 02',
  },
  14: {
    lore: 'El sistema de DAKI procesa listas de señales usando funciones de orden superior. Cada elemento de la transmisión pasa por un filtro — escríbelo y el ruido desaparece.',
    requires: 'Map y Filter',
    chapter: 'Sector 02',
  },
  15: {
    lore: 'Las operaciones rápidas del Nexo no merecen una función con nombre. Usa lambdas para construir transformaciones instantáneas que no dejen rastro en el log sináptico.',
    requires: 'Lambda',
    chapter: 'Sector 02',
  },
  16: {
    lore: 'Algunos protocolos del Nexo se activan a sí mismos. Para descifrar el patrón de encriptación recursiva debes programar una función que se llame a sí misma hasta alcanzar el núcleo.',
    requires: 'Recursión',
    chapter: 'Sector 02',
  },
  17: {
    lore: 'El generador de claves del Nexo produce tokens bajo demanda. Construye un generador que emita valores sin cargar toda la secuencia en memoria — el canal no tiene capacidad para eso.',
    requires: 'Generadores y Yield',
    chapter: 'Sector 02',
  },
  18: {
    lore: 'Los decoradores del Nexo modifican el comportamiento de funciones sin alterar su código fuente. Úsalos para añadir capas de protección sin dejar rastros en el núcleo.',
    requires: 'Decoradores',
    chapter: 'Sector 02',
  },
  19: {
    lore: 'El alcance de las variables define qué puede ver cada módulo del Nexo. Un operador que confunde el scope global con el local compromete la seguridad de toda la red sináptica.',
    requires: 'Scope y Closures',
    chapter: 'Sector 02',
  },
  20: {
    lore: 'El sector de funciones cierra con una prueba de integración. DAKI combinará todos los protocolos del Sector 02 en un único desafío. Si pasa este Boss, el Nexo te clasifica como operador funcional.',
    requires: 'Funciones — Sector 02',
    chapter: 'Sector 02 · BOSS',
  },
  // ── Sector 03 — Control de flujo ─────────────────────────────────────────
  21: {
    lore: 'Los sistemas del Nexo toman decisiones basadas en condiciones. Cada rama de código es una compuerta — abrirla o cerrarla determina si la misión avanza o se cancela.',
    requires: 'If / Elif / Else',
    chapter: 'Sector 03',
  },
  22: {
    lore: 'El protocolo de barrido iterativo recorre las capas de la Matriz una por una. Domina el while para mantener el ciclo activo exactamente el tiempo necesario — ni uno más.',
    requires: 'While Loops',
    chapter: 'Sector 03',
  },
  23: {
    lore: 'La señal de interrupción es el arma táctica más precisa del Nexo. Break y continue permiten saltar o escapar de ciclos sin colapsar el canal sináptico completo.',
    requires: 'Break y Continue',
    chapter: 'Sector 03',
  },
  24: {
    lore: 'Los iteradores del Nexo recorren cualquier estructura de datos. Comprende cómo Python genera secuencias bajo demanda y el sistema nunca podrá predecir tu siguiente movimiento.',
    requires: 'Iteradores',
    chapter: 'Sector 03',
  },
  25: {
    lore: 'La síntesis de listas es el lenguaje nativo de los operadores de élite. En una sola línea construyes estructuras que otros necesitan diez. El Nexo lee velocidad como señal de amenaza.',
    requires: 'List Comprehensions',
    chapter: 'Sector 03',
  },
  26: {
    lore: 'Las comprensiones se extienden a diccionarios y sets. Con ellas construyes estructuras de datos complejas en tiempo récord — antes de que el firewall del Nexo detecte el patrón.',
    requires: 'Dict y Set Comprehensions',
    chapter: 'Sector 03',
  },
  27: {
    lore: 'Los pares de datos viajan en tuplas por el canal sináptico. Desempaquétalos con precisión — cada valor en su variable, ningún dato perdido en la transmisión.',
    requires: 'Tuplas y Unpacking',
    chapter: 'Sector 03',
  },
  28: {
    lore: 'El Nexo transmite múltiples señales simultáneas. Zip las combina en pares coordinados. Sin esta técnica, los canales de datos se cruzan y la misión se corrompe.',
    requires: 'Zip y Enumerate',
    chapter: 'Sector 03',
  },
  29: {
    lore: 'Los conjuntos del Nexo eliminan duplicados automáticamente. Úsalos para detectar intersecciones entre redes enemigas — el análisis de sets revela alianzas ocultas en la Matriz.',
    requires: 'Sets y Operaciones',
    chapter: 'Sector 03',
  },
  30: {
    lore: 'El Boss del Sector 03 ejecuta un protocolo de flujo combinado. Bucles, condiciones y comprehensions trabajan juntos en un único sistema. El Nexo no perdona errores de lógica a este nivel.',
    requires: 'Control de Flujo — Sector 03',
    chapter: 'Sector 03 · BOSS',
  },
  // ── Sector 04 — Estructuras de datos ─────────────────────────────────────
  31: {
    lore: 'El índice de operaciones del Nexo es una pila — el último comando entra primero y sale primero. Implementa este protocolo o los comandos se ejecutan en orden incorrecto.',
    requires: 'Stacks',
    chapter: 'Sector 04',
  },
  32: {
    lore: 'La cola de transmisión del Nexo procesa señales en orden de llegada. FIFO es la única forma de garantizar que ningún operador sea ignorado en el canal sináptico.',
    requires: 'Queues',
    chapter: 'Sector 04',
  },
  33: {
    lore: 'El mapa hash del Nexo permite acceso instantáneo a cualquier nodo. Construye tu propia tabla de hash para entender por qué Python puede encontrar cualquier dato en tiempo constante.',
    requires: 'Hash Tables',
    chapter: 'Sector 04',
  },
  34: {
    lore: 'Los nodos del Nexo están conectados en cadenas. Una lista enlazada te permite recorrer esa red sin un índice — siguiendo únicamente el puntero al siguiente nodo.',
    requires: 'Listas Enlazadas',
    chapter: 'Sector 04',
  },
  35: {
    lore: 'El árbol de decisiones del Nexo ramifica cada operación en nodos padre e hijo. Recorrerlo en el orden correcto revela el camino al núcleo central de la Matriz.',
    requires: 'Árboles Binarios',
    chapter: 'Sector 04',
  },
  36: {
    lore: 'El grafo de conexiones del Nexo mapea las rutas entre todos los nodos activos. Encontrar el camino más corto entre dos puntos requiere un recorrido sistemático de toda la red.',
    requires: 'Grafos y BFS',
    chapter: 'Sector 04',
  },
  37: {
    lore: 'El heap del Nexo ordena prioridades automáticamente. Los comandos críticos flotan hacia la cima — construye este sistema para que DAKI siempre procese lo más urgente primero.',
    requires: 'Heaps y Priority Queues',
    chapter: 'Sector 04',
  },
  38: {
    lore: 'La búsqueda binaria es el protocolo de rastreo más eficiente del Nexo. En lugar de escanear toda la Matriz, divide y conquista — cada paso elimina la mitad de los candidatos.',
    requires: 'Búsqueda Binaria',
    chapter: 'Sector 04',
  },
  39: {
    lore: 'El algoritmo de ordenamiento del Nexo procesa miles de registros por segundo. Implementa mergesort para demostrar que entendés por qué dividir para conquistar es siempre más rápido.',
    requires: 'Sorting Algorithms',
    chapter: 'Sector 04',
  },
  40: {
    lore: 'El Boss del Sector 04 presenta un desafío de estructura combinada. Árboles, grafos y búsqueda binaria convergen en un único sistema. El Nexo mide tu eficiencia algorítmica con precisión.',
    requires: 'Estructuras de Datos — Sector 04',
    chapter: 'Sector 04 · BOSS',
  },
  // ── Sectores 05-07 — Contratos ────────────────────────────────────────────
  41: {
    lore: 'El primer contrato del Nexo activa el protocolo de especialización. A partir de aquí, cada operador elige su camino. Las misiones se vuelven más complejas — y las recompensas, mayores.',
    requires: 'Funciones Avanzadas',
    chapter: 'Sector 05',
  },
  42: {
    lore: 'Los argumentos posicionales y de palabras clave dan flexibilidad total a tus funciones. El Nexo requiere protocolos que se adapten a cualquier configuración de entrada.',
    requires: '*args y **kwargs',
    chapter: 'Sector 05',
  },
  43: {
    lore: 'Las funciones de orden superior transforman otras funciones. Mapa, filtro y reducción son las tres operaciones fundamentales del procesamiento de datos en el Nexo.',
    requires: 'Funciones de Orden Superior',
    chapter: 'Sector 05',
  },
  44: {
    lore: 'Los closures capturan el entorno de ejecución. Una función que recuerda su contexto puede adaptarse a cualquier misión sin necesidad de variables globales en el canal sináptico.',
    requires: 'Closures Avanzados',
    chapter: 'Sector 05',
  },
  45: {
    lore: 'El patrón de decorador es la armadura de las funciones del Nexo. Con él añades logging, validación o métricas sin tocar el código original — cero rastro, máxima eficiencia.',
    requires: 'Decoradores con Parámetros',
    chapter: 'Sector 05',
  },
  46: {
    lore: 'Los generadores infinitos producen datos bajo demanda. El Nexo procesa streams continuos de señales — un generador bien construido consume memoria constante sin importar el volumen.',
    requires: 'Generadores Infinitos',
    chapter: 'Sector 05',
  },
  47: {
    lore: 'Las expresiones generadoras condensan el poder de los generadores en una sola línea. El canal sináptico se mantiene limpio y el rendimiento, óptimo.',
    requires: 'Generator Expressions',
    chapter: 'Sector 05',
  },
  48: {
    lore: 'La programación funcional pura evita el estado mutable. En el Nexo, una función sin efectos secundarios es una función imposible de rastrear para los sistemas de defensa de la Matriz.',
    requires: 'Programación Funcional',
    chapter: 'Sector 05',
  },
  49: {
    lore: 'El penúltimo nodo del Sector 05 integra todas las técnicas funcionales aprendidas. El Nexo evalúa la consistencia de tu código — no solo que funcione, sino que sea elegante.',
    requires: 'Funciones — Integración',
    chapter: 'Sector 05',
  },
  50: {
    lore: 'CONTRATO ACTIVO. El Nexo exige una demostración de dominio funcional completo. Este Boss evalúa velocidad, precisión y eficiencia. Solo los operadores certificados avanzan al Sector 06.',
    requires: 'Contrato Sector 05',
    chapter: 'Sector 05 · CONTRATO',
  },
  51: {
    lore: 'El Sector 06 abre las puertas de la Programación Orientada a Objetos. Los objetos del Nexo encapsulan estado y comportamiento — dominar OOP es dominar la arquitectura de la Matriz.',
    requires: 'Clases y Objetos',
    chapter: 'Sector 06',
  },
  52: {
    lore: 'El constructor define la identidad de cada objeto en el Nexo. Sin un __init__ correcto, el objeto nace con datos corruptos y la misión falla antes de comenzar.',
    requires: 'Constructor e Init',
    chapter: 'Sector 06',
  },
  53: {
    lore: 'La herencia permite que los protocolos del Nexo se especialicen sin duplicar código. Una clase hija hereda los poderes de su padre y los extiende con capacidades propias.',
    requires: 'Herencia',
    chapter: 'Sector 06',
  },
  54: {
    lore: 'El polimorfismo permite que distintos objetos respondan al mismo comando de formas diferentes. El Nexo ejecuta protocolos genéricos sobre objetos específicos — y cada uno actúa según su naturaleza.',
    requires: 'Polimorfismo',
    chapter: 'Sector 06',
  },
  55: {
    lore: 'La encapsulación protege los datos internos del objeto. Los atributos privados del Nexo no pueden modificarse desde el exterior — una barrera sináptica que ningún intruso puede cruzar.',
    requires: 'Encapsulación',
    chapter: 'Sector 06',
  },
  56: {
    lore: 'Los métodos mágicos de Python dan comportamiento especial a los objetos. Con __str__, __eq__ y __len__, tus objetos del Nexo se integran nativamente con el sistema.',
    requires: 'Dunder Methods',
    chapter: 'Sector 06',
  },
  57: {
    lore: 'Las propiedades del Nexo controlan el acceso a los datos internos con lógica de validación. Sin getters y setters, cualquier operador podría corromper el estado del objeto.',
    requires: 'Properties',
    chapter: 'Sector 06',
  },
  58: {
    lore: 'Los métodos de clase y estáticos operan a nivel del tipo, no de la instancia. Son los protocolos compartidos que todos los objetos del Nexo ejecutan sin necesitar datos propios.',
    requires: 'Class y Static Methods',
    chapter: 'Sector 06',
  },
  59: {
    lore: 'La composición es la alternativa a la herencia cuando los objetos deben colaborar sin jerarquía. En el Nexo, los sistemas complejos se construyen ensamblando piezas más simples.',
    requires: 'Composición',
    chapter: 'Sector 06',
  },
  60: {
    lore: 'CONTRATO ACTIVO. El Boss del Sector 06 despliega un sistema OOP completo. Clases, herencia, polimorfismo y encapsulación en un único protocolo. El Nexo certifica solo a los mejores.',
    requires: 'Contrato Sector 06',
    chapter: 'Sector 06 · CONTRATO',
  },
  61: {
    lore: 'El Sector 07 entra en el territorio del manejo de errores. En el Nexo, un operador que no anticipa las fallas es un operador que falla. Aprendé a capturar, manejar y recuperarte.',
    requires: 'Try / Except',
    chapter: 'Sector 07',
  },
  62: {
    lore: 'El Nexo genera múltiples tipos de error según el contexto. Capturar la excepción correcta es la diferencia entre un sistema robusto y uno que colapsa al primer obstáculo.',
    requires: 'Múltiples Excepciones',
    chapter: 'Sector 07',
  },
  63: {
    lore: 'Las excepciones personalizadas son el lenguaje de error de cada protocolo. Cuando el Nexo falla por razones específicas de tu sistema, necesitás errores con nombres propios.',
    requires: 'Custom Exceptions',
    chapter: 'Sector 07',
  },
  64: {
    lore: 'El bloque finally garantiza que los recursos del Nexo se limpien siempre, sin importar si la operación tuvo éxito o falló. Sin él, los canales sinápticos quedan abiertos indefinidamente.',
    requires: 'Finally y Cleanup',
    chapter: 'Sector 07',
  },
  65: {
    lore: 'El raise activo lanza excepciones de forma intencional. A veces el Nexo debe señalar explícitamente que una condición es inválida — antes de que el error silencioso lo corrompa todo.',
    requires: 'Raise Explícito',
    chapter: 'Sector 07',
  },
  66: {
    lore: 'Los gestores de contexto garantizan que los recursos del Nexo se abran y cierren correctamente. El with statement es el protocolo de acceso controlado a sistemas críticos.',
    requires: 'Context Managers',
    chapter: 'Sector 07',
  },
  67: {
    lore: 'El logging del Nexo registra cada operación en el historial sináptico. Sin un sistema de logging robusto, los errores de producción son invisibles hasta que ya es demasiado tarde.',
    requires: 'Logging',
    chapter: 'Sector 07',
  },
  68: {
    lore: 'El protocolo de assertions verifica que las condiciones críticas se cumplan en cada etapa. El Nexo falla rápido y ruidosamente — mejor un assert que un bug silencioso en producción.',
    requires: 'Assertions',
    chapter: 'Sector 07',
  },
  69: {
    lore: 'La cadena de errores del Nexo preserva el contexto original cuando una excepción desencadena otra. Raise from none elimina el ruido y revela la causa raíz con precisión quirúrgica.',
    requires: 'Exception Chaining',
    chapter: 'Sector 07',
  },
  70: {
    lore: 'CONTRATO ACTIVO. El Boss del Sector 07 provoca un cascada de errores encadenados. Solo el operador que domine manejo de excepciones a fondo puede contener el colapso sináptico.',
    requires: 'Contrato Sector 07',
    chapter: 'Sector 07 · CONTRATO',
  },
  // ── Sector 08 — OOP Avanzado ──────────────────────────────────────────────
  71: {
    lore: 'Los metaclases del Nexo controlan cómo se crean las clases. Es el nivel de abstracción más profundo — aquí el código se convierte en el propio sistema que lo ejecuta.',
    requires: 'OOP Avanzado',
    chapter: 'Sector 08',
  },
  72: { lore: 'Los protocolos de iteración del Nexo requieren que los objetos sepan recorrerse a sí mismos. Implementa __iter__ y __next__ para que tus objetos sean ciudadanos de primera clase en Python.', requires: 'Iteradores Personalizados', chapter: 'Sector 08' },
  73: { lore: 'El descriptor del Nexo controla el acceso a los atributos de forma centralizada. Con él, la validación y transformación de datos ocurre automáticamente en cada asignación.', requires: 'Descriptores', chapter: 'Sector 08' },
  74: { lore: 'Los slots del Nexo optimizan el uso de memoria al limitar los atributos permitidos. En sistemas de alto volumen, cada byte cuenta — __slots__ es la herramienta para operadores de élite.', requires: '__slots__', chapter: 'Sector 08' },
  75: { lore: 'La herencia múltiple del Nexo permite combinar capacidades de distintas clases. El MRO determina el orden de resolución — sin entenderlo, los conflictos de herencia son impredecibles.', requires: 'Herencia Múltiple y MRO', chapter: 'Sector 08' },
  76: { lore: 'Los mixins del Nexo añaden capacidades específicas a cualquier clase sin herencia pesada. Son módulos de comportamiento reutilizables que el Nexo ensambla según la misión.', requires: 'Mixins', chapter: 'Sector 08' },
  77: { lore: 'El protocolo ABC del Nexo define interfaces que las clases hijas deben implementar obligatoriamente. Sin clases abstractas, los contratos de código son solo sugerencias ignorables.', requires: 'Abstract Base Classes', chapter: 'Sector 08' },
  78: { lore: 'Los dataclasses del Nexo generan automáticamente constructores, representaciones y comparaciones. Menos código, más estructura — el estilo de los operadores que valoran la eficiencia.', requires: 'Dataclasses', chapter: 'Sector 08' },
  79: { lore: 'El protocolo de comparación del Nexo permite ordenar objetos según criterios propios. Implementa __lt__, __gt__ y sus variantes para que tus objetos se integren con sorted() y min().', requires: 'Operadores de Comparación', chapter: 'Sector 08' },
  80: { lore: 'El Boss del Sector 08 despliega un sistema OOP de arquitectura compleja. Metaclases, ABCs y descriptores en un único protocolo. El Nexo te clasifica como Arquitecto Sináptico.', requires: 'OOP Avanzado — Sector 08', chapter: 'Sector 08 · BOSS' },
  // ── Sector 09 — Errores Avanzados ────────────────────────────────────────
  81: { lore: 'Los errores del Nexo hablan un idioma — si sabés escucharlos. En el Sector 09 aprendés a leer trazas de error como un mapa que te lleva directo al problema.', requires: 'Lectura de Errores', chapter: 'Sector 09' },
  82: { lore: 'El debugger del Nexo congela la ejecución en el punto exacto del problema. pdb es el escáner sináptico más preciso — con él navegás el estado del programa en tiempo real.', requires: 'pdb — Debugger', chapter: 'Sector 09' },
  83: { lore: 'Los errores de importación del Nexo ocurren antes de que el código corra. ModuleNotFoundError y sus variantes son señales tempranas que el sistema lanza antes del inicio de misión.', requires: 'Import Errors', chapter: 'Sector 09' },
  84: { lore: 'Los AttributeError del Nexo revelan que un objeto no tiene lo que se le pide. En la Matriz, acceder a un atributo inexistente es una brecha de seguridad que el sistema cierra inmediatamente.', requires: 'AttributeError', chapter: 'Sector 09' },
  85: { lore: 'El TypeError del Nexo ocurre cuando los tipos no coinciden. Cada función tiene un contrato de tipos — violarlo desencadena una alarma sináptica que paraliza el canal de datos.', requires: 'TypeError', chapter: 'Sector 09' },
  86: { lore: 'El ValueError del Nexo señala datos con el tipo correcto pero el valor incorrecto. Es el error más sutil — el sistema acepta el formato pero rechaza el contenido.', requires: 'ValueError', chapter: 'Sector 09' },
  87: { lore: 'Los errores de recursión del Nexo ocurren cuando una función se llama a sí misma sin fin. RecursionError es la alarma de profundidad máxima — el canal sináptico tiene límites.', requires: 'RecursionError', chapter: 'Sector 09' },
  88: { lore: 'Los errores de memoria del Nexo aparecen cuando el sistema intenta procesar más datos de los que puede sostener. Optimizar el consumo de memoria es la diferencia entre misión completada y colapso.', requires: 'Memory Errors', chapter: 'Sector 09' },
  89: { lore: 'El sistema de testing del Nexo verifica que el código funcione bajo cualquier condición. pytest transforma los casos de prueba en un escudo automático contra errores futuros.', requires: 'pytest Básico', chapter: 'Sector 09' },
  90: { lore: 'El Boss del Sector 09 presenta un sistema con múltiples tipos de error encadenados. Para completar la misión debés identificar, capturar y registrar cada fallo con precisión clínica.', requires: 'Errores Avanzados — Sector 09', chapter: 'Sector 09 · BOSS' },
  // ── Sector 10 — Algoritmos ───────────────────────────────────────────────
  91: { lore: 'El análisis de complejidad del Nexo mide cuánto tarda un algoritmo a medida que los datos crecen. Big-O es el lenguaje universal para comparar la eficiencia de protocolos.', requires: 'Big-O Notation', chapter: 'Sector 10' },
  92: { lore: 'La búsqueda lineal recorre todos los elementos del Nexo hasta encontrar el objetivo. Es la estrategia más simple — y la más costosa cuando la Matriz tiene millones de nodos.', requires: 'Búsqueda Lineal', chapter: 'Sector 10' },
  93: { lore: 'Quicksort es el algoritmo de ordenamiento más usado en sistemas de producción. Divide el problema en subproblemas más simples y los resuelve en paralelo — el Nexo lo aprecia.', requires: 'Quicksort', chapter: 'Sector 10' },
  94: { lore: 'La programación dinámica del Nexo evita recalcular lo que ya fue resuelto. Memoización y tabulación son las dos armas para convertir problemas exponenciales en polinomiales.', requires: 'Programación Dinámica', chapter: 'Sector 10' },
  95: { lore: 'El algoritmo greedy del Nexo toma siempre la mejor decisión local. No siempre es óptimo globalmente, pero en los problemas correctos es la estrategia más rápida disponible.', requires: 'Algoritmos Greedy', chapter: 'Sector 10' },
  96: { lore: 'El backtracking del Nexo explora todas las rutas posibles y retrocede cuando encuentra un callejón sin salida. Es la técnica de los sistemas que no pueden permitirse errores definitivos.', requires: 'Backtracking', chapter: 'Sector 10' },
  97: { lore: 'El recorrido DFS del Nexo sumerge al dron en la profundidad de la red antes de explorar lateralmente. Es la estrategia de infiltración para grafos con ramas largas y nodos ocultos.', requires: 'DFS — Depth First Search', chapter: 'Sector 10' },
  98: { lore: 'El recorrido BFS del Nexo explora capa por capa. Es el protocolo ideal para encontrar el camino más corto en redes donde cada conexión tiene el mismo costo.', requires: 'BFS — Breadth First Search', chapter: 'Sector 10' },
  99: { lore: 'El algoritmo de Dijkstra del Nexo encuentra el camino de menor costo entre dos nodos. En redes con pesos diferentes, es la única forma de garantizar la ruta óptima.', requires: 'Dijkstra', chapter: 'Sector 10' },
  100: { lore: 'El Boss Final del Sector 10 presenta un problema algorítmico de complejidad real. No hay atajos. Solo el operador que domina Big-O, búsqueda y ordenamiento puede completar este protocolo.', requires: 'Algoritmos — Sector 10', chapter: 'Sector 10 · BOSS' },
  // ── Sector 11 — Algoritmos Intermedios ───────────────────────────────────
  101: { lore: 'El Sector 11 abre el protocolo de cifrado. Caesar Cipher es la primera capa de seguridad del Nexo — sin entender cómo encriptar datos, el canal sináptico es vulnerable.', requires: 'Cifrado César', chapter: 'Sector 11' },
  102: { lore: 'El escáner de frecuencias del Nexo analiza patrones en transmisiones de texto. Contar vocales revela la densidad informacional del mensaje — un indicador crítico de autenticidad.', requires: 'Análisis de Texto', chapter: 'Sector 11' },
  103: { lore: 'Las transmisiones del Nexo a veces llegan en orden inverso como protocolo anti-interceptación. Tu dron debe invertir las secuencias para reconstruir el mensaje original.', requires: 'Inversión de Datos', chapter: 'Sector 11' },
  104: { lore: 'El protocolo de jerarquía del Nexo establece el segundo operador en comando cuando el líder falla. Tu algoritmo debe identificarlo con precisión — ningún canal puede quedar sin control.', requires: 'Segundo Elemento', chapter: 'Sector 11' },
  105: { lore: 'Los números primos son la base de la criptografía del Nexo. Detectarlos con eficiencia es la diferencia entre un sistema seguro y uno vulnerable a ataques de factorización.', requires: 'Números Primos', chapter: 'Sector 11' },
  106: { lore: 'La suma de dígitos es el checksum básico del Nexo para verificar integridad de datos. Si la suma no coincide, la transmisión fue alterada en el canal sináptico.', requires: 'Suma de Dígitos', chapter: 'Sector 11' },
  107: { lore: 'El análisis de frecuencia del Nexo mapea cuántas veces aparece cada señal en una transmisión. La palabra más frecuente revela la prioridad operacional del mensaje.', requires: 'Frecuencia de Palabras', chapter: 'Sector 11' },
  108: { lore: 'El sistema de conteo táctico del Nexo usa objetos para mantener estado de múltiples operaciones simultáneas. Una clase bien diseñada es más robusta que mil variables sueltas.', requires: 'Clases con Estado', chapter: 'Sector 11' },
  109: { lore: 'La búsqueda binaria del Nexo localiza cualquier nodo en tiempo logarítmico. En una red de millones de operadores, es el único protocolo de búsqueda que escala.', requires: 'Búsqueda Binaria', chapter: 'Sector 11' },
  110: { lore: 'El Boss del Sector 11 activa el Analizador de Transmisiones completo. Cifrado, frecuencia y búsqueda convergen en un único protocolo de inteligencia sináptica.', requires: 'Algoritmos Intermedios — Sector 11', chapter: 'Sector 11 · BOSS' },
  // ── Sector 12 — Algoritmos Avanzados ─────────────────────────────────────
  111: { lore: 'Los anagramas son el protocolo de autenticación del Nexo para verificar identidad de operadores. Dos palabras con las mismas letras comparten la misma huella espectral.', requires: 'Anagramas', chapter: 'Sector 12' },
  112: { lore: 'Two Sum es el problema de emparejamiento táctico del Nexo. Encontrarlo en O(n) con un diccionario es la señal de que el operador entiende cómo sacrificar memoria por velocidad.', requires: 'Two Sum', chapter: 'Sector 12' },
  113: { lore: 'Las estructuras anidadas del Nexo ocultan datos en múltiples capas. Aplanar esa jerarquía revela la información real que el sistema trata de camuflar.', requires: 'Flatten de Datos', chapter: 'Sector 12' },
  114: { lore: 'El clasificador de registros del Nexo organiza transmisiones según criterios múltiples. Ordenar por múltiples claves es la base de cualquier sistema de inteligencia operacional.', requires: 'Clasificación Múltiple', chapter: 'Sector 12' },
  115: { lore: 'La media móvil del Nexo suaviza las fluctuaciones en series temporales de datos. Detectar tendencias en el ruido sináptico es la habilidad de los analistas de élite.', requires: 'Media Móvil', chapter: 'Sector 12' },
  116: { lore: 'Los palíndromos son firmas de autenticidad en los mensajes del Nexo. Un mensaje que se lee igual en ambos sentidos no puede ser falsificado por la Matriz enemiga.', requires: 'Palíndromos', chapter: 'Sector 12' },
  117: { lore: 'El sistema romano del Nexo es un protocolo de codificación numérica legado. Decodificarlo revela las coordenadas de nodos históricos que la Matriz creyó haber eliminado.', requires: 'Números Romanos', chapter: 'Sector 12' },
  118: { lore: 'El algoritmo de Kadane localiza la secuencia de señales con mayor energía acumulada. En el Nexo, esa secuencia marca el punto de mayor actividad sináptica — el epicentro del objetivo.', requires: 'Máximo Subarray — Kadane', chapter: 'Sector 12' },
  119: { lore: 'La compresión RLE reduce el tamaño de las transmisiones del Nexo sin pérdida de información. Secuencias repetidas se compactan en un par código-cantidad — el canal se libera.', requires: 'Compresión RLE', chapter: 'Sector 12' },
  120: { lore: 'El Boss del Sector 12 activa el Pipeline de Procesamiento completo. Datos crudos entran, datos procesados salen. El Nexo evalúa la limpieza y eficiencia de tu cadena de transformación.', requires: 'Algoritmos Avanzados — Sector 12', chapter: 'Sector 12 · BOSS' },
  // ── Sector 13 — Estructuras + OOP ────────────────────────────────────────
  121: { lore: 'La pila táctica del Nexo es la estructura de último-en-entrar-primero-en-salir. Cada operación se apila sobre la anterior — y el sistema las deshace en el mismo orden.', requires: 'Pila (Stack)', chapter: 'Sector 13' },
  122: { lore: 'El validador de expresiones del Nexo verifica que cada paréntesis abierto tenga su cierre. Una expresión desbalanceada colapsa el parser sináptico al instante.', requires: 'Validación de Expresiones', chapter: 'Sector 13' },
  123: { lore: 'La transposición matricial del Nexo rota los datos 90 grados. Lo que era una fila se convierte en columna — la perspectiva cambia y nuevos patrones se vuelven visibles.', requires: 'Transposición de Matrices', chapter: 'Sector 13' },
  124: { lore: 'El analizador de fortaleza del Nexo evalúa contraseñas según criterios múltiples. Una contraseña débil es una brecha abierta en el sistema — y el Nexo no tolera brechas.', requires: 'Fortaleza de Contraseñas', chapter: 'Sector 13' },
  125: { lore: 'El codificador de mensajes del Nexo transforma texto plano en transmisiones cifradas usando sustitución de caracteres. Sin la clave, el mensaje es ruido para cualquier interceptor.', requires: 'Codificación de Mensajes', chapter: 'Sector 13' },
  126: { lore: 'Mergesort divide para conquistar. El Nexo lo usa para ordenar registros de operadores en tiempo O(n log n) — el estándar de los sistemas que no pueden permitirse lentitud.', requires: 'Mergesort', chapter: 'Sector 13' },
  127: { lore: 'Los objetos del Nexo necesitan una representación textual clara. __str__ define cómo un operador se presenta al sistema — sin él, los logs muestran basura sináptica.', requires: 'Representación de Objetos', chapter: 'Sector 13' },
  128: { lore: 'La secuencia de Fibonacci esconde el patrón de crecimiento de la red sináptica del Nexo. Generarla eficientemente revela cuántos nodos nuevos emergerán en cada ciclo.', requires: 'Fibonacci', chapter: 'Sector 13' },
  129: { lore: 'El análisis columnar del Nexo procesa datos organizados en columnas independientes. Extraer y transformar cada columna por separado es la base del análisis de datos estructurados.', requires: 'Análisis Columnar', chapter: 'Sector 13' },
  130: { lore: 'CONTRATO ACTIVO. El Boss del Sector 13 integra estructuras y OOP en un sistema unificado. Pilas, matrices y objetos cooperan en un protocolo de alta complejidad. Solo los mejores completan este contrato.', requires: 'Contrato Sector 13', chapter: 'Sector 13 · CONTRATO' },
  // ── Sector 14 — Stdlib ────────────────────────────────────────────────────
  131: { lore: 'La biblioteca estándar de Python es el arsenal del Nexo. math, random, datetime — herramientas que evitan reinventar protocolos que ya existen y están optimizados.', requires: 'math y random', chapter: 'Sector 14' },
  132: { lore: 'El módulo de geometría táctica del Nexo calcula distancias, áreas y ángulos. Cada coordenada en la Matriz tiene un significado — la geometría revela las relaciones ocultas.', requires: 'Geometría con math', chapter: 'Sector 14' },
  133: { lore: 'El generador aleatorio del Nexo produce variaciones impredecibles en los protocolos de entrenamiento. Sin aleatoriedad, los sistemas de defensa de la Matriz aprenden a anticipar tus movimientos.', requires: 'random — Generación', chapter: 'Sector 14' },
  134: { lore: 'El módulo de muestreo del Nexo selecciona subsets representativos de grandes datasets. Mezclar y samplear sin repetición es la base de cualquier protocolo de análisis estadístico.', requires: 'random — Muestreo', chapter: 'Sector 14' },
  135: { lore: 'El módulo datetime del Nexo rastrea la línea temporal de todas las operaciones. Sin fechas precisas, los logs sinápticos pierden su valor como evidencia operacional.', requires: 'datetime', chapter: 'Sector 14' },
  136: { lore: 'El formateador de fechas del Nexo convierte timestamps en texto legible para informes de inteligencia. strftime es el traductor entre el tiempo de la máquina y el lenguaje del operador.', requires: 'strftime', chapter: 'Sector 14' },
  137: { lore: 'El Counter del Nexo cuenta frecuencias automáticamente. En lugar de construir un diccionario manualmente, Counter lo hace en una línea — y lo hace mejor.', requires: 'collections.Counter', chapter: 'Sector 14' },
  138: { lore: 'El módulo string del Nexo provee conjuntos de caracteres predefinidos. ascii_letters, digits, punctuation — bloques de construcción para validación sin reinventar ruedas.', requires: 'string module', chapter: 'Sector 14' },
  139: { lore: 'El módulo os.path del Nexo navega el sistema de archivos con precisión. Rutas absolutas, relativas, existencia de archivos — el sistema operativo es solo otro protocolo a dominar.', requires: 'os.path', chapter: 'Sector 14' },
  140: { lore: 'El Boss del Sector 14 activa el Inspector de Datos completo usando la stdlib. math, random, datetime y collections convergen en un sistema de análisis que el Nexo usa en producción.', requires: 'Stdlib — Sector 14', chapter: 'Sector 14 · BOSS' },
  // ── Sector 15 — Archivos ──────────────────────────────────────────────────
  141: { lore: 'El sistema de archivos del Nexo persiste datos entre operaciones. Sin archivos, cada sesión comienza desde cero — la memoria sináptica se pierde al apagar el canal.', requires: 'Lectura y Escritura', chapter: 'Sector 15' },
  142: { lore: 'El procesamiento línea por línea del Nexo es el protocolo para archivos grandes. Cargar todo en memoria revienta el canal — leer línea a línea mantiene el sistema estable.', requires: 'Procesamiento Línea a Línea', chapter: 'Sector 15' },
  143: { lore: 'El modo acumulativo del Nexo añade registros sin borrar los anteriores. Append es el protocolo para logs que crecen con cada operación — el historial sináptico nunca se borra.', requires: 'Modo Append', chapter: 'Sector 15' },
  144: { lore: 'El filtro de registros del Nexo extrae solo las líneas que cumplen criterios específicos. En un log de millones de entradas, la señal relevante está sepultada en ruido — hay que filtrarla.', requires: 'Filtro de Archivos', chapter: 'Sector 15' },
  145: { lore: 'El formato CSV es el estándar del Nexo para intercambio de datos estructurados. csv.writer y csv.reader transforman datos Python en un formato que cualquier sistema puede leer.', requires: 'CSV — Escritura y Lectura', chapter: 'Sector 15' },
  146: { lore: 'El Boss del Sector 15 activa el Procesador CSV completo. DictReader, Counter y análisis de columnas cooperan en un pipeline que convierte datos crudos en inteligencia operacional.', requires: 'Archivos — Sector 15', chapter: 'Sector 15 · BOSS' },
  // ── Sector 16 — OOP Avanzado ──────────────────────────────────────────────
  147: { lore: 'La identidad de un objeto en el Nexo está definida por __str__ y __repr__. Sin ellos, el sistema solo muestra una dirección de memoria — información inútil para el operador.', requires: '__str__ y __repr__', chapter: 'Sector 16' },
  148: { lore: 'La igualdad de objetos en el Nexo no es automática. __eq__ define cuándo dos instancias son equivalentes — sin él, el sistema compara referencias, no contenido.', requires: '__eq__', chapter: 'Sector 16' },
  149: { lore: 'Los constructores alternativos del Nexo crean instancias desde distintos formatos de entrada. @classmethod permite que un solo objeto se construya desde JSON, desde un dict, o desde texto.', requires: '@classmethod', chapter: 'Sector 16' },
  150: { lore: 'La jerarquía de unidades del Nexo usa herencia para especializar protocolos base. Cada unidad hereda las capacidades del padre y añade las propias sin duplicar código.', requires: 'Herencia Especializada', chapter: 'Sector 16' },
  151: { lore: 'super() del Nexo llama al protocolo del padre sin hardcodear su nombre. Es la forma correcta de extender comportamiento heredado — flexible, mantenible y libre de acoplamientos.', requires: 'super()', chapter: 'Sector 16' },
  152: { lore: 'Los métodos estáticos del Nexo son funciones que pertenecen a la clase pero no dependen de ninguna instancia. Son utilidades compartidas por todo el protocolo sin acceso al estado interno.', requires: '@staticmethod', chapter: 'Sector 16' },
  153: { lore: 'El protocolo polimórfico del Nexo permite que distintas clases respondan al mismo mensaje de formas diferentes. Un comando único, múltiples comportamientos — la arquitectura de los sistemas flexibles.', requires: 'Polimorfismo Avanzado', chapter: 'Sector 16' },
  154: { lore: 'El Boss del Sector 16 construye una Red de Nodos con OOP completo. Herencia, dunders, classmethods y polimorfismo cooperan en una arquitectura de objetos que el Nexo certifica como production-ready.', requires: 'OOP Avanzado — Sector 16', chapter: 'Sector 16 · BOSS' },
  // ── Sector 17 — Errores Avanzados ────────────────────────────────────────
  155: { lore: 'El raise explícito del Nexo señala condiciones inválidas antes de que el daño sea mayor. Un error bien lanzado es más útil que diez errores silenciosos que corroen el sistema.', requires: 'raise Explícito', chapter: 'Sector 17' },
  156: { lore: 'Las excepciones personalizadas del Nexo tienen nombres propios. SystemFailureError, InvalidOperatorError — cuando el error tiene nombre, el operador sabe exactamente qué falló.', requires: 'Custom Exceptions', chapter: 'Sector 17' },
  157: { lore: 'La cadena de errores del Nexo preserva el contexto original. raise from None elimina el ruido de la cadena — muestra el error relevante sin el historial que distrae.', requires: 'Exception Chaining', chapter: 'Sector 17' },
  158: { lore: 'El bloque finally del Nexo garantiza limpieza de recursos sin importar qué pasó. Archivos, conexiones, locks — finally los cierra siempre, en éxito o en falla.', requires: 'finally', chapter: 'Sector 17' },
  159: { lore: 'El gestor de contexto del Nexo encapsula el patrón abrir-usar-cerrar en una interfaz limpia. __enter__ y __exit__ son el protocolo de acceso controlado a recursos críticos del sistema.', requires: 'Context Managers', chapter: 'Sector 17' },
  175: { lore: 'CONTRATO ACTIVO. El Boss del Sector 17 desencadena una cascada de errores complejos. raise, custom exceptions, finally y context managers deben cooperar para contener el colapso del sistema.', requires: 'Contrato Sector 17', chapter: 'Sector 17 · CONTRATO' },
  // ── Sector 18 — Proyecto Modular ──────────────────────────────────────────
  160: { lore: 'El guardián del main del Nexo controla qué código se ejecuta cuando el módulo es invocado directamente. __name__ == "__main__" es la primera línea de defensa de cualquier script profesional.', requires: '__name__ == "__main__"', chapter: 'Sector 18' },
  161: { lore: 'JSON es el idioma universal del Nexo para intercambio de datos. dumps convierte objetos Python en strings transmisibles — loads los reconstruye al recibirlos en el otro extremo.', requires: 'JSON', chapter: 'Sector 18' },
  162: { lore: 'Los argumentos CLI del Nexo permiten configurar el comportamiento de los scripts sin tocar el código. Un operador que domina argv puede adaptar sus herramientas a cualquier misión.', requires: 'CLI Arguments', chapter: 'Sector 18' },
  163: { lore: 'La estructura de módulo del Nexo separa constantes, configuración y lógica en capas claras. Un módulo bien organizado es un módulo que cualquier operador puede leer y extender.', requires: 'Estructura de Módulo', chapter: 'Sector 18' },
  164: { lore: 'La persistencia JSON del Nexo guarda el estado de las operaciones entre sesiones. dump escribe al archivo, load lo recupera — la memoria del sistema sobrevive al reinicio.', requires: 'Persistencia JSON', chapter: 'Sector 18' },
  165: { lore: 'El Boss del Sector 18 construye un Gestor de Misiones completo. JSON, CLI, módulos y persistencia cooperan en un sistema que el Nexo podría usar en producción real.', requires: 'Proyecto Modular — Sector 18', chapter: 'Sector 18 · BOSS' },
  // ── Sector 19 — Modo Debug ────────────────────────────────────────────────
  166: { lore: 'El Modo Debug del Nexo invierte el rol del operador. En lugar de escribir código, lo reparás. Cada bug es una brecha en el sistema — encontrarla antes de que el Nexo la explote.', requires: 'Debug — NameError', chapter: 'Sector 19' },
  167: { lore: 'Los conflictos de tipo del Nexo son errores silenciosos hasta que explotan. TypeError revela que el código mezcla tipos incompatibles — el sistema no puede operar con datos inconsistentes.', requires: 'Debug — TypeError', chapter: 'Sector 19' },
  168: { lore: 'El error off-by-one es el bug más frecuente en los sistemas del Nexo. Un índice de más, un índice de menos — y la transmisión pierde el primer o el último dato crítico.', requires: 'Debug — Off-by-One', chapter: 'Sector 19' },
  169: { lore: 'Una función sin return en el Nexo devuelve None en silencio. El sistema acepta el resultado, lo procesa — y produce basura. El bug más tranquilo y el más peligroso.', requires: 'Debug — Missing Return', chapter: 'Sector 19' },
  170: { lore: 'El KeyError del Nexo revela que el sistema busca datos donde no existen. Una clave incorrecta en un diccionario es una dirección inválida — el canal sináptico no puede responder.', requires: 'Debug — KeyError', chapter: 'Sector 19' },
  171: { lore: 'El acumulador que se resetea en cada iteración es el error de lógica más clásico del Nexo. El código corre sin errores — pero el resultado siempre es el último elemento, nunca la suma.', requires: 'Debug — Acumulador', chapter: 'Sector 19' },
  172: { lore: 'La lógica invertida del Nexo produce resultados correctos en formato pero incorrectos en valor. El sistema no lanza ningún error — simplemente hace lo opuesto de lo que se espera.', requires: 'Debug — Lógica Invertida', chapter: 'Sector 19' },
  173: { lore: 'El Boss del Sector 19 combina IndexError y error de lógica en un único sistema. Dos bugs, una misión. El Nexo mide tu velocidad de diagnosis — los mejores operadores los encuentran en segundos.', requires: 'Debug — Boss', chapter: 'Sector 19 · BOSS' },
  // ── Sector 20 — Entrevistas ───────────────────────────────────────────────
  174: { lore: 'Two Sum es la primera pregunta de entrevista del Nexo. La solución O(n²) existe — pero el Nexo solo certifica operadores que lo resuelven en O(n) con un diccionario como tabla hash.', requires: 'Two Sum O(n)', chapter: 'Sector 20' },
  176: { lore: 'El palíndromo es el test de razonamiento básico del Nexo. No se trata del problema — se trata de demostrar que el operador piensa antes de escribir y normaliza los datos de entrada.', requires: 'Palíndromo', chapter: 'Sector 20' },
  177: { lore: 'Los anagramas son el test de equivalencia del Nexo. sorted() como clave de hash es la solución elegante — cualquier otra es O(n²) y el entrevistador del Nexo lo sabe.', requires: 'Anagramas', chapter: 'Sector 20' },
  178: { lore: 'El algoritmo de Kadane es el test de programación dinámica del Nexo. En cada posición tomás una decisión: ¿sumo al subarreglo actual o empiezo uno nuevo? La respuesta siempre es la misma.', requires: 'Máximo Subarray — Kadane', chapter: 'Sector 20' },
  179: { lore: 'El Boss final del Nexo agrupa anagramas usando defaultdict. Es el problema de entrevista más elegante del catálogo — tuple(sorted()) como clave de hash revela quién realmente entiende Python.', requires: 'Entrevistas — Sector 20', chapter: 'Sector 20 · BOSS' },
  // ── Sector Predict — Leer y Predecir ─────────────────────────────────────
  180: { lore: 'El protocolo Predict invierte el desafío. En lugar de escribir código, lo leés y predecís su salida. El Nexo mide si realmente entendés lo que el código hace — no solo si podés escribirlo.', requires: 'Lectura de Código', chapter: 'Sector Predict' },
  181: { lore: 'Predecir la salida de código ajeno es la habilidad de los operadores de élite. Un bug en producción no espera — el operador que lee rápido y predice con precisión es el que lo encuentra primero.', requires: 'Predict — Nivel 2', chapter: 'Sector Predict' },
  182: { lore: 'El análisis de código del Nexo sin ejecutarlo es el nivel más alto de comprensión. Si podés predecir la salida exacta incluyendo errores, el sistema te clasifica como Arquitecto.', requires: 'Predict — Nivel 3', chapter: 'Sector Predict' },
  183: { lore: 'Los efectos secundarios del código son invisibles para quien solo corre el programa. El operador que lee el código entiende qué cambia en cada estado — y por qué.', requires: 'Predict — Nivel 4', chapter: 'Sector Predict' },
  184: { lore: 'Las funciones recursivas son el desafío mental más exigente del protocolo Predict. Seguir la pila de llamadas mentalmente hasta el resultado final requiere precisión y paciencia.', requires: 'Predict — Recursión', chapter: 'Sector Predict' },
  185: { lore: 'Los iteradores y generadores del Nexo producen valores de forma lazy. Predecir exactamente cuándo y qué producen requiere entender el modelo de ejecución de Python a fondo.', requires: 'Predict — Generadores', chapter: 'Sector Predict' },
  186: { lore: 'El scope y los closures crean comportamientos que solo se entienden leyendo el código. Variables que persisten, variables que se pierden — predecirlo correctamente distingue al experto.', requires: 'Predict — Closures', chapter: 'Sector Predict' },
  187: { lore: 'Las clases y objetos del Nexo tienen estado mutable. Predecir el estado final de un objeto después de múltiples operaciones es el test de OOP más exigente del sistema.', requires: 'Predict — OOP', chapter: 'Sector Predict' },
  188: { lore: 'Los decoradores modifican el comportamiento de funciones de formas no obvias. Predecir la salida de una función decorada requiere entender exactamente qué hace el wrapper.', requires: 'Predict — Decoradores', chapter: 'Sector Predict' },
  189: { lore: 'El Boss Predict del Nexo es el desafío de lectura más complejo del catálogo. Múltiples patrones combinados, estado mutable, closures y OOP — todo en un único bloque de código a predecir.', requires: 'Predict — Boss Final', chapter: 'Sector Predict · BOSS' },
}

// ─── Constantes UI ─────────────────────────────────────────────────────────────


// ─── S5: Filtro por rama de especialización ────────────────────────────────────

const BRANCH_LABELS: Record<string, string> = {
  auto: 'Automatización y Scripting',
  qa:   'Testing y QA',
  api:  'APIs y Backend',
  data: 'Data Science y Análisis',
  ai:   'Inteligencia Artificial Básica',
}

const BRANCH_KEYWORDS: Record<string, string[]> = {
  auto: ['automatizacion', 'scripting', 'cli', 'automatización'],
  qa:   ['testing', 'qa', 'pytest', 'test'],
  api:  ['api', 'backend', 'fastapi', 'django', 'rest'],
  data: ['data', 'analisis', 'pandas', 'numpy', 'análisis'],
  ai:   ['ia', 'ai', 'machine_learning', 'ml', 'inteligencia'],
}

function sortByBranch(list: Mission[], branch: string | null): Mission[] {
  if (!branch) return list
  const kws = BRANCH_KEYWORDS[branch] ?? []
  return [...list].sort((a, b) => {
    const score = (m: Mission) =>
      kws.some(k =>
        m.phase?.toLowerCase().includes(k) ||
        m.concepts_taught?.some(c => c.toLowerCase().includes(k))
      ) ? 1 : 0
    return score(b) - score(a)
  })
}

// ─── Panel de Briefing (columna derecha) ───────────────────────────────────────

function BriefingPanel({
  mission,
  onDeploy,
}: {
  mission: Mission | null
  onDeploy: (_m: Mission) => void
}) {
  if (!mission) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center text-center px-12">
        <motion.div
          className="w-16 h-16 rounded-full border border-[#00FF41]/15 flex items-center justify-center mb-6"
          animate={{ opacity: [0.3, 0.7, 0.3] }}
          transition={{ duration: 2.5, repeat: Infinity }}
        >
          <span className="text-[#00FF41]/30 text-2xl">◈</span>
        </motion.div>
        <p className="text-[13px] tracking-[0.35em] text-[#00FF41]/35">
          SELECCIONA UNA INCURSIÓN
        </p>
        <p className="text-xs tracking-wider text-[#00FF41]/20 mt-2">
          PARA VER EL BRIEFING TÁCTICO
        </p>
      </div>
    )
  }

  const order = mission.level_order ?? 0
  const lore = MISSION_LORE[order]
  const tierColor = TIER_COLOR[mission.difficulty_tier]
  const isLocked = !mission.unlocked

  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={mission.id}
        className="flex-1 flex flex-col px-8 py-8 overflow-y-auto"
        initial={{ opacity: 0, x: 16 }}
        animate={{ opacity: 1, x: 0 }}
        exit={{ opacity: 0, x: -8 }}
        transition={{ duration: 0.25 }}
      >
        {/* Tag de clasificación */}
        <div className="flex items-center gap-3 mb-5">
          <span className={`text-[11px] tracking-[0.35em] ${mission.challenge_type === 'tutorial' ? 'text-cyan-400/60' : 'text-[#00FF41]/45'}`}>
            {mission.challenge_type === 'tutorial'
              ? 'PROTOCOLO 00 // CALIBRACIÓN OBLIGATORIA'
              : `INCURSIÓN #${String(order).padStart(2, '0')} // EL NEXO`}
          </span>
          {mission.completed && (
            <span
              className="text-[8px] tracking-widest border px-2 py-0.5"
              style={mission.challenge_type === 'tutorial'
                ? { color: 'rgba(0,229,255,0.9)', borderColor: 'rgba(0,229,255,0.3)', textShadow: '0 0 6px rgba(0,229,255,0.6)' }
                : { color: '#00FF41', borderColor: 'rgba(0,255,65,0.3)', textShadow: '0 0 6px #00FF41' }
              }
            >
              ✓ COMPLETADA
            </span>
          )}
        </div>

        {/* Título */}
        <h2
          className="text-2xl font-black tracking-wider mb-1 drop-shadow-[0_0_12px_rgba(0,255,65,0.7)]"
          style={{ color: '#00FF41' }}
        >
          {mission.title.toUpperCase()}
        </h2>

        {/* Dificultad + XP */}
        <div className="flex items-center gap-4 mb-6">
          <span className="text-[13px] tracking-widest font-bold" style={{ color: `${tierColor}90` }}>
            {TIER_LABEL[mission.difficulty_tier]}
          </span>
          <span className="text-[#00FF41]/20">·</span>
          <span
            className="text-sm font-black text-[#FFD700]"
            style={{ textShadow: '0 0 8px rgba(255,215,0,0.5)' }}
          >
            {mission.base_xp_reward} XP
          </span>
          {mission.attempts > 0 && !mission.completed && (
            <>
              <span className="text-[#00FF41]/20">·</span>
              <span className="text-[10px] text-green-200/50">
                {mission.attempts} intento{mission.attempts !== 1 ? 's' : ''}
              </span>
            </>
          )}
        </div>

        {/* Separador */}
        <div className="h-px bg-gradient-to-r from-[#00FF41]/20 via-[#00FF41]/10 to-transparent mb-6" />

        {/* Lore / Objetivo táctico */}
        <div className="mb-5">
          <p className="text-[11px] tracking-[0.35em] text-[#00FF41]/50 mb-3">◆ OBJETIVO TÁCTICO</p>
          <div
            className="border-l-2 border-[#00FF41]/30 pl-4 bg-black/40 backdrop-blur-sm py-3 pr-3"
            style={{ boxShadow: 'inset 0 0 20px rgba(0,255,65,0.03)' }}
          >
            <p className="text-sm text-green-200/75 leading-relaxed">
              {lore?.lore ?? mission.description}
            </p>
          </div>
        </div>

        {/* Conocimiento requerido */}
        {lore && (
          <div
            className="border border-[#00E5FF]/20 bg-black/40 backdrop-blur-sm px-4 py-3 mb-6"
            style={{ boxShadow: '0 4px 20px rgba(0,229,255,0.06)' }}
          >
            <p className="text-[11px] tracking-[0.35em] text-[#00E5FF]/55 mb-2">CONOCIMIENTO REQUERIDO</p>
            <div className="flex items-center gap-3">
              <span className="text-[13px] text-[#00E5FF]/80 font-bold tracking-wider">
                {lore.requires}
              </span>
              <span className="text-[#00E5FF]/30">·</span>
              <span className="text-xs tracking-widest text-[#00E5FF]/50 border border-[#00E5FF]/20 px-2 py-0.5">
                {lore.chapter}
              </span>
            </div>
          </div>
        )}

        {/* Lore briefing si existe */}
        {mission.lore_briefing && (
          <div className="mb-6">
            <p className="text-[11px] tracking-[0.35em] text-[#00FF41]/45 mb-2">TRANSMISIÓN DE DAKI</p>
            <p className="text-[13px] text-[#00FF41]/55 leading-relaxed italic">
              &ldquo;{mission.lore_briefing}&rdquo;
            </p>
          </div>
        )}

        {/* Spacer */}
        <div className="flex-1" />

        {/* Botón de despliegue */}
        {isLocked ? (
          <div className="border border-[#00FF41]/10 bg-black/40 backdrop-blur-sm px-5 py-4 text-center">
            <p className="text-xs tracking-[0.35em] text-[#00FF41]/40">
              🔒 INCURSIÓN BLOQUEADA
            </p>
            <p className="text-[11px] text-[#00FF41]/25 mt-1 tracking-wider">
              COMPLETA EL PROTOCOLO 00 PARA DESBLOQUEAR
            </p>
          </div>
        ) : mission.challenge_type === 'tutorial' ? (
          <motion.button
            onClick={() => onDeploy(mission)}
            className="w-full py-4 border-2 font-black text-sm tracking-[0.28em] transition-all duration-200 cursor-pointer"
            style={{
              borderColor: 'rgba(0,229,255,0.6)',
              color: 'rgba(0,229,255,0.9)',
              background: 'rgba(0,229,255,0.06)',
              boxShadow: '0 0 20px rgba(0,229,255,0.1)',
              textShadow: '0 0 8px rgba(0,229,255,0.6)',
            }}
            whileHover={{
              background: 'rgba(0,229,255,0.12)',
              boxShadow: '0 0 40px rgba(0,229,255,0.25), inset 0 0 20px rgba(0,229,255,0.05)',
            }}
            whileTap={{ scale: 0.98 }}
          >
            ▶ INICIALIZAR CALIBRACIÓN SINÁPTICA
          </motion.button>
        ) : (
          <motion.button
            onClick={() => onDeploy(mission)}
            className="w-full py-4 border-2 font-black text-sm tracking-[0.3em] transition-all duration-200 cursor-pointer"
            style={{
              borderColor: 'rgba(0,255,65,0.6)',
              color: '#00FF41',
              background: 'rgba(0,255,65,0.07)',
              boxShadow: '0 0 20px rgba(0,255,65,0.1)',
              textShadow: '0 0 8px rgba(0,255,65,0.6)',
            }}
            whileHover={{
              background: 'rgba(0,255,65,0.14)',
              boxShadow: '0 0 40px rgba(0,255,65,0.3), inset 0 0 20px rgba(0,255,65,0.05)',
            }}
            whileTap={{ scale: 0.98 }}
          >
            ▶ INICIALIZAR ENLACE — ENTRAR A LA MISIÓN
          </motion.button>
        )}
      </motion.div>
    </AnimatePresence>
  )
}

// ─── Página principal ──────────────────────────────────────────────────────────

export default function MisionesPage() {
  const router = useRouter()
  const { _hasHydrated, userId, username, level, totalXp, streakDays, completedChallengeIds } = useUserStore()
  const [missions, setMissions] = useState<Mission[]>([])
  const [loading, setLoading] = useState(true)
  const [fetchError, setFetchError] = useState(false)
  const [selected, setSelected] = useState<Mission | null>(null)
  const listRef = useRef<HTMLDivElement>(null)
  const [briefingMission, setBriefingMission] = useState<Mission | null>(null)
  const [isHacking, setIsHacking] = useState(false)
  const [hackingTitle, setHackingTitle] = useState('')
  // S5 — Rama activa leída desde ?branch=<id>
  const [activeBranch, setActiveBranch] = useState<string | null>(null)

  useEffect(() => {
    if (!_hasHydrated) return
    if (!userId) { router.replace('/login'); setLoading(false); return }
    // Leer parámetros de URL antes de la carga
    const params = new URLSearchParams(window.location.search)
    const branchParam = params.get('branch')
    if (branchParam && BRANCH_LABELS[branchParam]) setActiveBranch(branchParam)

    fetch(`${API_BASE}/api/v1/challenges?user_id=${userId}`)
      .then(r => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`)
        return r.json()
      })
      .then((data: Mission[]) => {
        // Merge local cache: marcar como completadas las misiones que constan en localStorage
        const merged = data.map(m =>
          completedChallengeIds.includes(m.id) ? { ...m, completed: true } : m
        )
        setMissions(merged)
        // Restaurar selección desde URL param ?selected=<UUID>
        const selectedParam = params.get('selected')
        const target = selectedParam ? merged.find(m => m.id === selectedParam && m.unlocked) : null
        const first = target ?? merged.find(m => m.unlocked && !m.completed) ?? merged[0]
        if (first) {
          setSelected(first)
          // Scroll al item seleccionado tras render
          if (target) {
            setTimeout(() => {
              const el = listRef.current?.querySelector(`[data-mission-id="${target.id}"]`) as HTMLElement | null
              el?.scrollIntoView({ behavior: 'smooth', block: 'center' })
            }, 120)
          }
        }
      })
      .catch(() => { setFetchError(true) })
      .finally(() => setLoading(false))
  }, [_hasHydrated, userId, router])

  const completadas    = missions.filter(m => m.completed).length
  const tutorial       = missions.find(m => m.challenge_type === 'tutorial')
  const tutorialDone   = tutorial?.completed ?? true
  // S5 — Lista ordenada por relevancia de rama (si hay filtro activo)
  const displayedMissions = sortByBranch(missions, activeBranch)

  const handleDeploy = (mission: Mission) => {
    if (!mission.unlocked) return
    // Misiones drone no tienen transición de hackeo (van a /enigma directamente)
    if (mission.challenge_type === 'drone') { router.push('/enigma'); return }
    // Si tiene lore briefing, mostrarlo antes de la transición
    if (mission.lore_briefing) { setBriefingMission(mission); return }
    // Transición de hackeo → luego push
    setHackingTitle(mission.title)
    setIsHacking(true)
    setTimeout(() => router.push(`/challenge/${mission.id}`), 1500)
  }

  const handleBriefingInitialize = () => {
    if (!briefingMission) return
    const mission = briefingMission
    setBriefingMission(null)
    setHackingTitle(mission.title)
    setIsHacking(true)
    setTimeout(() => router.push(`/challenge/${mission.id}`), 1500)
  }

  return (
    <div
      className="h-[calc(100vh-2rem)] flex flex-col font-mono text-[#00FF41] relative overflow-hidden"
      style={{ background: 'radial-gradient(circle at 50% 40%, #001a0d 0%, #000000 60%)' }}
    >
      {/* Scanlines */}
      <div
        className="fixed inset-0 pointer-events-none z-10"
        style={{ backgroundImage: 'repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,0,0,0.07) 2px,rgba(0,0,0,0.07) 4px)' }}
      />
      {/* Viñeta */}
      <div
        className="fixed inset-0 pointer-events-none z-10"
        style={{ background: 'radial-gradient(ellipse at center, transparent 40%, rgba(0,0,0,0.75) 100%)' }}
      />

      {/* Modal de briefing */}
      <MissionBriefingModal
        visible={briefingMission !== null}
        title={briefingMission?.title ?? ''}
        loreBriefing={briefingMission?.lore_briefing ?? ''}
        pedagogicalObjective={briefingMission?.pedagogical_objective ?? ''}
        syntaxHint={briefingMission?.syntax_hint ?? ''}
        onInitialize={handleBriefingInitialize}
        onClose={() => setBriefingMission(null)}
      />

      {/* Transición de hackeo — z-[9999] cubre todo */}
      <HackingTransition isActive={isHacking} missionTitle={hackingTitle} />

      {/* ── Header ── */}
      <header className="relative z-20 shrink-0 flex items-center justify-between px-6 py-2.5 border-b border-[#00FF41]/12 bg-black/50 backdrop-blur-sm">
        <div className="flex items-center gap-4">
          <button
            onClick={() => router.push('/hub')}
            className="text-[#00FF41]/40 hover:text-[#00FF41]/80 text-xs tracking-widest transition-colors border border-[#00FF41]/15 px-2.5 py-1 hover:border-[#00FF41]/35 cursor-pointer"
          >
            ← VOLVER A DAKI
          </button>
          <span
            className="font-black tracking-widest text-sm hidden sm:block"
            style={{ textShadow: '0 0 8px #00FF41' }}
          >
            PYTHON QUEST
          </span>
        </div>
        <div className="flex items-center gap-5 text-xs text-[#00FF41]/50">
          <span className="text-[#00FF41]/30 hidden sm:block">{username}</span>
          <span>RANGO <strong className="text-[#00FF41]">{level}</strong></span>
          <span>XP <strong className="text-[#00FF41]">{totalXp.toLocaleString()}</strong></span>
          {streakDays > 0 && <span>🔥 <strong className="text-[#00FF41]">{streakDays}d</strong></span>}
        </div>
      </header>

      {/* ── Split screen ── */}
      <main className="relative z-20 flex-1 flex overflow-hidden gap-px">

        {/* ══════════════════════════════════════════
            COLUMNA IZQUIERDA — Lista de incursiones
        ══════════════════════════════════════════ */}
        <div
          className="w-[340px] shrink-0 flex flex-col overflow-hidden bg-black/40 backdrop-blur-md border-r border-green-500/20"
          style={{ boxShadow: '4px 0 30px rgba(0,255,65,0.06)' }}
        >

          {/* Cabecera columna */}
          <div className="shrink-0 px-5 py-4 border-b border-green-500/15 bg-black/30 backdrop-blur-sm">
            <h2 className="text-sm font-black tracking-[0.3em] text-[#00FF41]/80 mb-1 drop-shadow-[0_0_6px_rgba(0,255,65,0.5)]">
              SELECTOR DE INCURSIONES
            </h2>
            {/* Barra de progreso */}
            <div className="flex items-center gap-3 mt-2">
              <div className="flex-1 h-0.5 bg-[#00FF41]/10 relative overflow-hidden">
                <motion.div
                  className="absolute left-0 top-0 h-full bg-[#00FF41]"
                  initial={{ width: 0 }}
                  animate={{ width: missions.length ? `${(completadas / missions.length) * 100}%` : '0%' }}
                  transition={{ duration: 1, ease: 'easeOut' }}
                  style={{ boxShadow: '0 0 6px #00FF41' }}
                />
              </div>
              <span className="text-xs tracking-wider text-[#00FF41]/50 shrink-0 font-bold">
                {completadas}/{missions.length}
              </span>
            </div>
          </div>

          {/* Lista scrollable */}
          <div ref={listRef} className="flex-1 overflow-y-auto py-2">
            {loading ? (
              <p className="text-[#00FF41]/25 text-[10px] tracking-widest animate-pulse px-5 py-6">
                CARGANDO INCURSIONES...
              </p>
            ) : fetchError ? (
              <p className="text-red-400/50 text-[10px] tracking-widest px-5 py-6">
                ERROR DE CONEXIÓN
              </p>
            ) : (
              <>
                {/* ── S5: Banner de rama activa ── */}
                {activeBranch && BRANCH_LABELS[activeBranch] && (
                  <motion.div
                    className="mx-3 mb-2 mt-1 border px-4 py-2.5 flex items-center justify-between gap-2"
                    style={{
                      borderColor: 'rgba(245,158,11,0.35)',
                      background:  'rgba(245,158,11,0.06)',
                      boxShadow:   '0 0 12px rgba(245,158,11,0.07)',
                    }}
                    initial={{ opacity: 0, y: -6 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.3 }}
                  >
                    <div>
                      <p className="text-[11px] tracking-[0.3em] font-black font-mono"
                        style={{ color: 'rgba(245,158,11,0.85)' }}>
                        ⚡ VISTA FILTRADA
                      </p>
                      <p className="text-[11px] tracking-wider font-mono mt-0.5"
                        style={{ color: 'rgba(245,158,11,0.60)' }}>
                        {BRANCH_LABELS[activeBranch]}
                      </p>
                    </div>
                    <button
                      onClick={() => {
                        setActiveBranch(null)
                        window.history.replaceState({}, '', '/misiones')
                      }}
                      className="text-[11px] tracking-[0.2em] font-mono border px-2 py-1 transition-colors"
                      style={{ color: 'rgba(245,158,11,0.45)', borderColor: 'rgba(245,158,11,0.22)' }}
                      onMouseEnter={e => { e.currentTarget.style.color = 'rgba(245,158,11,0.80)' }}
                      onMouseLeave={e => { e.currentTarget.style.color = 'rgba(245,158,11,0.45)' }}
                    >
                      ✕ LIMPIAR
                    </button>
                  </motion.div>
                )}

                {/* ── Banner: calibración requerida ── */}
                {!tutorialDone && (
                  <motion.div
                    className="mx-3 mb-2 mt-1 border border-cyan-500/35 bg-cyan-900/10 px-4 py-3"
                    initial={{ opacity: 0, y: -6 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.3 }}
                    style={{ boxShadow: '0 0 16px rgba(0,229,255,0.07), inset 0 0 12px rgba(0,229,255,0.04)' }}
                  >
                    <div className="flex items-center gap-2 mb-1">
                      <motion.span
                        className="w-1.5 h-1.5 rounded-full bg-cyan-400 shrink-0"
                        animate={{ opacity: [0.4, 1, 0.4] }}
                        transition={{ duration: 1.2, repeat: Infinity }}
                        style={{ boxShadow: '0 0 5px rgba(0,229,255,0.8)' }}
                      />
                      <span className="text-[12px] tracking-[0.3em] text-cyan-400/90 font-bold uppercase">
                        Calibración Sináptica Requerida
                      </span>
                    </div>
                    <p className="text-[12px] text-cyan-200/60 leading-relaxed">
                      Completa el Protocolo 00 para desbloquear las incursiones del Nexo.
                    </p>
                  </motion.div>
                )}

                {displayedMissions.map((m, idx) => {
                  const isLocked = !m.unlocked
                  const isSelected = selected?.id === m.id
                  const tierColor = TIER_COLOR[m.difficulty_tier]
                  const isAvailable = m.unlocked && !m.completed

                  const isTutorial = m.challenge_type === 'tutorial'
                  const tutorialSelectedBg = 'rgba(0,229,255,0.08)'
                  const tutorialHoverBg    = 'rgba(0,229,255,0.05)'

                  return (
                    <motion.button
                      key={m.id}
                      data-mission-id={m.id}
                      initial={{ opacity: 0, x: -12 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: idx * 0.06 }}
                      onClick={() => { if (!isLocked) setSelected(m) }}
                      disabled={isLocked}
                      className={[
                        'w-full text-left px-5 py-3.5 border-b transition-all duration-200 relative',
                        'border-l-4',
                        isLocked
                          ? 'opacity-40 grayscale cursor-not-allowed border-l-transparent border-b-green-500/5'
                          : isSelected
                          ? isTutorial
                            ? 'border-l-cyan-400 border-b-cyan-500/10 cursor-pointer'
                            : 'border-l-[#00FF41] border-b-green-500/10 cursor-pointer'
                          : isTutorial
                          ? 'border-l-cyan-700/60 border-b-cyan-500/8 cursor-pointer hover:translate-x-1'
                          : 'border-l-green-800/50 border-b-green-500/8 cursor-pointer hover:translate-x-1',
                      ].join(' ')}
                      style={
                        isSelected
                          ? {
                              background: isTutorial ? tutorialSelectedBg : 'rgba(0,255,65,0.08)',
                              boxShadow: isTutorial
                                ? 'inset 0 0 20px rgba(0,229,255,0.06), 0 0 10px rgba(0,229,255,0.05)'
                                : 'inset 0 0 20px rgba(0,255,65,0.06), 0 0 10px rgba(0,255,65,0.05)',
                            }
                          : {}
                      }
                      onMouseEnter={e => {
                        if (!isLocked && !isSelected) {
                          e.currentTarget.style.background = isTutorial ? tutorialHoverBg : 'rgba(0,255,65,0.05)'
                          e.currentTarget.style.boxShadow = isTutorial
                            ? 'inset 0 0 20px rgba(0,229,255,0.08)'
                            : 'inset 0 0 20px rgba(0,255,65,0.08)'
                          e.currentTarget.style.borderLeftColor = isTutorial ? 'rgba(0,229,255,0.6)' : 'rgba(0,255,65,0.5)'
                        }
                      }}
                      onMouseLeave={e => {
                        if (!isSelected) {
                          e.currentTarget.style.background = 'transparent'
                          e.currentTarget.style.boxShadow = 'none'
                          e.currentTarget.style.borderLeftColor = isLocked
                            ? 'transparent'
                            : isTutorial ? 'rgba(0,100,120,0.6)' : 'rgba(0,100,30,0.5)'
                        }
                      }}
                    >
                      {/* Badge tutorial */}
                      {isTutorial && (
                        <div className="flex items-center gap-1.5 mb-1.5">
                          <motion.span
                            className="w-1.5 h-1.5 rounded-full bg-cyan-400 shrink-0"
                            animate={{ opacity: [0.4, 1, 0.4] }}
                            transition={{ duration: 1.4, repeat: Infinity }}
                          />
                          <span className="text-[11px] tracking-[0.25em] text-cyan-400/80 font-bold uppercase">
                            Protocolo 00 · Obligatorio
                          </span>
                        </div>
                      )}

                      <div className="flex items-center justify-between gap-3">
                        <div className="flex items-center gap-3 min-w-0">
                          <span className={`text-xs w-5 shrink-0 tabular-nums font-bold ${isTutorial ? 'text-cyan-400/50' : 'text-[#00FF41]/40'}`}>
                            {String(m.level_order ?? idx + 1).padStart(2, '0')}
                          </span>
                          <span
                            className={[
                              'text-[13px] font-bold tracking-wide truncate',
                              isLocked
                                ? 'text-[#00FF41]/25'
                                : isSelected
                                ? isTutorial
                                  ? 'text-cyan-300 drop-shadow-[0_0_8px_rgba(0,229,255,0.8)]'
                                  : 'text-[#00FF41] drop-shadow-[0_0_8px_rgba(0,255,65,0.8)]'
                                : isTutorial
                                ? 'text-cyan-400/80'
                                : 'text-green-400',
                            ].join(' ')}
                          >
                            {m.title}
                          </span>
                        </div>
                        <div className="shrink-0 text-xs flex items-center gap-1.5">
                          {isLocked ? (
                            <span className="text-[#00FF41]/20">🔒</span>
                          ) : m.completed ? (
                            <span
                              style={isTutorial
                                ? { color: 'rgba(0,229,255,0.9)', textShadow: '0 0 6px rgba(0,229,255,0.7)' }
                                : { color: '#00FF41', textShadow: '0 0 6px #00FF41' }}
                            >✓</span>
                          ) : isAvailable ? (
                            <>
                              <span
                                className={`w-1.5 h-1.5 rounded-full animate-pulse shrink-0 ${isTutorial ? 'bg-cyan-400' : 'bg-green-500'}`}
                                style={{ boxShadow: isTutorial ? '0 0 4px rgba(0,229,255,0.8)' : '0 0 4px #00FF41' }}
                              />
                              <span style={{ color: isTutorial ? 'rgba(0,229,255,0.7)' : `${tierColor}70` }}>▶</span>
                            </>
                          ) : null}
                        </div>
                      </div>

                      {/* Fila inferior: dificultad + intentos */}
                      <div className="pl-8 mt-0.5 flex items-center gap-2">
                        <span
                          className="text-[11px] tracking-wider"
                          style={{ color: isTutorial ? 'rgba(0,229,255,0.50)' : `${tierColor}55` }}
                        >
                          {isTutorial ? 'CALIBRACIÓN' : TIER_LABEL[m.difficulty_tier]}
                        </span>
                        {m.attempts > 0 && !m.completed && (
                          <span className="text-[11px] text-green-200/40">
                            · {m.attempts} intento{m.attempts !== 1 ? 's' : ''}
                          </span>
                        )}
                      </div>
                    </motion.button>
                  )
                })}

                {/* ── Separadores especiales ── */}
                {!loading && (
                  <>
                    {/* JEFE FINAL */}
                    {(() => {
                      const completedCount = missions.filter(m => m.completed).length
                      const BOSS_THRESHOLD = missions.length || 190
                      const bossUnlocked = completedCount >= BOSS_THRESHOLD
                      const remaining = Math.max(0, BOSS_THRESHOLD - completedCount)
                      return (
                        <>
                          <div className="px-5 pt-5 pb-1">
                            <div className="flex items-center gap-2 mb-2">
                              <div className="h-px flex-1 bg-red-500/20" />
                              <span className="text-[11px] tracking-[0.3em] text-red-500/60">JEFE FINAL</span>
                              <div className="h-px flex-1 bg-red-500/20" />
                            </div>
                          </div>
                          <button
                            onClick={() => bossUnlocked && router.push('/boss')}
                            disabled={!bossUnlocked}
                            className={[
                              'w-full text-left px-5 py-3.5 border-b border-l-4 border-b-red-500/10 transition-all duration-200',
                              bossUnlocked
                                ? 'border-l-red-700/60 cursor-pointer hover:translate-x-1'
                                : 'border-l-red-900/30 cursor-not-allowed opacity-50',
                            ].join(' ')}
                            style={{ background: bossUnlocked ? 'rgba(127,0,0,0.15)' : 'rgba(40,0,0,0.10)' }}
                            onMouseEnter={e => {
                              if (!bossUnlocked) return
                              e.currentTarget.style.background = 'rgba(127,0,0,0.25)'
                              e.currentTarget.style.boxShadow = '0 0 30px rgba(255,0,0,0.15), inset 0 0 20px rgba(255,0,0,0.08)'
                              e.currentTarget.style.borderLeftColor = 'rgba(239,68,68,0.8)'
                            }}
                            onMouseLeave={e => {
                              if (!bossUnlocked) return
                              e.currentTarget.style.background = 'rgba(127,0,0,0.15)'
                              e.currentTarget.style.boxShadow = 'none'
                              e.currentTarget.style.borderLeftColor = 'rgba(185,28,28,0.6)'
                            }}
                          >
                            <div className="flex items-center justify-between">
                              <div className="flex items-center gap-3">
                                {bossUnlocked ? (
                                  <motion.span
                                    className="text-red-500/70 text-base"
                                    animate={{ opacity: [0.5, 1, 0.5] }}
                                    transition={{ duration: 1.8, repeat: Infinity }}
                                  >∞</motion.span>
                                ) : (
                                  <span className="text-red-900/60 text-base">🔒</span>
                                )}
                                <div>
                                  <span className={[
                                    'text-[13px] font-bold tracking-wide',
                                    bossUnlocked
                                      ? 'text-red-400 drop-shadow-[0_0_8px_rgba(255,0,0,0.6)]'
                                      : 'text-red-900/60',
                                  ].join(' ')}>
                                    THE INFINITE LOOPER
                                  </span>
                                  {!bossUnlocked && (
                                    <div className="text-[9px] tracking-[0.2em] text-red-900/50 mt-0.5">
                                      {remaining} MISIONES RESTANTES
                                    </div>
                                  )}
                                </div>
                              </div>
                              <span className={[
                                'text-[11px] tracking-widest border px-1.5 py-0.5',
                                bossUnlocked
                                  ? 'text-red-400/60 border-red-500/30'
                                  : 'text-red-900/40 border-red-900/20',
                              ].join(' ')}>
                                BOSS
                              </span>
                            </div>
                          </button>
                        </>
                      )
                    })()}

                  </>
                )}
              </>
            )}
          </div>
        </div>

        {/* ══════════════════════════════════════════
            COLUMNA DERECHA — Panel de Briefing
        ══════════════════════════════════════════ */}
        <div
          className="flex-1 bg-black/40 backdrop-blur-md overflow-hidden"
          style={{ boxShadow: 'inset 4px 0 30px rgba(0,0,0,0.3)' }}
        >
          <BriefingPanel mission={selected} onDeploy={handleDeploy} />
        </div>

      </main>
    </div>
  )
}
