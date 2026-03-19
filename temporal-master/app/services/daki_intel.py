"""
DAKI Intel — Traductor de Errores y Analista de Código.

Mapea excepciones Python + estados de evaluación a frases narrativas de DAKI,
adaptadas según su nivel evolutivo:
  1 → ROBÓTICO  — respuestas técnicas, escuetas, terminología de sistema
  2 → AMISTOSO  — tono de mentor, explica el error con contexto
  3 → COMPAÑERO — empático, didáctico, guía paso a paso sin revelar la solución

Uso:
    from app.services.daki_intel import get_daki_message
    msg = get_daki_message("SyntaxError", daki_level=2)
    msg = get_daki_message("failed", daki_level=3)
    msg = get_daki_message("success", daki_level=1)
"""

import random
from typing import Literal

# ─── Tipos ────────────────────────────────────────────────────────────────────

DakiLevel = Literal[1, 2, 3]

# Eventos que DAKI puede comentar: tipos de error Python + estados de resultado
DakiEvent = Literal[
    "SyntaxError", "IndentationError", "NameError", "TypeError",
    "ValueError", "AttributeError", "IndexError", "KeyError",
    "ZeroDivisionError", "RecursionError", "RuntimeError",
    "TimeoutError", "failed", "success", "timeout",
]


# ─── Diccionario de mensajes ──────────────────────────────────────────────────
#
# Estructura: event → { nivel: [msg, msg, ...] }
# Múltiples mensajes por nivel permiten variación aleatoria para evitar
# que DAKI siempre repita la misma frase en errores consecutivos.

_MESSAGES: dict[str, dict[int, list[str]]] = {

    # ── Errores de sintaxis / estructura ──────────────────────────────────────

    "SyntaxError": {
        1: [
            "ERROR: ESTRUCTURA CORRUPTA. Símbolo inválido detectado. "
            "Verifica paréntesis, comillas y dos puntos.",
            "SINTAXIS INVÁLIDA. El compilador rechazó la entrada. "
            "Revisa el símbolo en la línea indicada.",
        ],
        2: [
            "Operador, la estructura está corrupta. Te olvidaste un símbolo "
            "clave. Revisa los dos puntos o paréntesis.",
            "El parser no pudo leer eso. Un símbolo falta o está mal colocado. "
            "Revisa comillas y paréntesis.",
        ],
        3: [
            "Tranquilo, Operador. Python no pudo leer esa línea. Hay un símbolo "
            "fuera de lugar — busca paréntesis sin cerrar o comillas sin terminar.",
            "Es un error de escritura. Algo pequeño falta: quizás un ':' al final "
            "de un if, o una comilla sin cerrar. Lo encontrarás rápido.",
        ],
    },

    "IndentationError": {
        1: [
            "ERROR: INDENTACIÓN INVÁLIDA. Los bloques de código requieren "
            "alineación exacta.",
            "ALINEACIÓN INCORRECTA. El intérprete no puede determinar "
            "la jerarquía del bloque.",
        ],
        2: [
            "Los niveles de indentación son las murallas del código. "
            "Alinea tus bloques, Operador.",
            "Hay un problema de sangría. Los bloques dentro de if, for o def "
            "necesitan 4 espacios de margen.",
        ],
        3: [
            "La indentación define la lógica en Python. Usa 4 espacios por nivel "
            "y asegúrate de ser consistente en todo el bloque.",
            "Python usa el espacio para entender la estructura. El bloque "
            "desalineado no corresponde al nivel correcto — revísalo con calma.",
        ],
    },

    # ── Errores de nombres / tipos / valores ──────────────────────────────────

    "NameError": {
        1: [
            "ERROR: IDENTIFICADOR NO DEFINIDO. La variable referenciada "
            "no existe en el scope actual.",
            "REFERENCIA INVÁLIDA. El símbolo no fue declarado en este namespace.",
        ],
        2: [
            "Detecto una variable fantasma. Estás llamando a algo que no fue "
            "declarado en esta línea temporal.",
            "Esa variable no existe todavía. Asegúrate de declararla antes "
            "de usarla, Operador.",
        ],
        3: [
            "Parece que estás usando una variable que aún no fue creada. "
            "Revisa el orden: primero asigna, luego usa.",
            "El nombre que buscas no está en memoria. Quizás hay un typo, "
            "o la variable se definió en otro bloque.",
        ],
    },

    "TypeError": {
        1: [
            "ERROR: TIPO DE DATO INCOMPATIBLE. La operación no puede ejecutarse "
            "con los tipos provistos.",
            "CONFLICTO DE TIPOS. La función recibió un argumento de tipo incorrecto.",
        ],
        2: [
            "Operación inválida entre tipos incompatibles. No puedes mezclar "
            "texto y números sin conversión.",
            "TypeError detectado. Probablemente estás sumando un string con un int. "
            "Usa int() o str() para convertir.",
        ],
        3: [
            "Ese error ocurre cuando mezclas tipos incompatibles, como un string "
            "con un número. Usa int() para convertir, Operador.",
            "Python es estricto con los tipos. Si necesitas operar un número "
            "que viene de input(), conviértelo primero con int() o float().",
        ],
    },

    "ValueError": {
        1: [
            "ERROR: VALOR INVÁLIDO. La función recibió un argumento de tipo "
            "correcto pero valor inaceptable.",
            "CONVERSIÓN FALLIDA. El dato no puede ser transformado al tipo objetivo.",
        ],
        2: [
            "El valor que ingresaste no puede ser convertido. Revisa que el input "
            "sea numérico si usas int().",
            "ValueError: algo que intentaste convertir no tiene el formato correcto. "
            "Por ejemplo, int('abc') no funciona.",
        ],
        3: [
            "Ese error suele pasar cuando int() recibe algo que no es un número puro. "
            "Asegúrate de que el input sea solo dígitos.",
            "ValueError significa que el tipo está bien pero el valor no. "
            "Revisa qué datos llegan a la conversión.",
        ],
    },

    "AttributeError": {
        1: [
            "ERROR: ATRIBUTO NO ENCONTRADO. El objeto no posee el método "
            "o propiedad referenciada.",
            "MÉTODO INVÁLIDO. El atributo consultado no existe en este tipo de objeto.",
        ],
        2: [
            "Ese método o atributo no existe en ese tipo de objeto. "
            "Verifica el tipo de dato y sus métodos disponibles.",
            "AttributeError: estás accediendo a algo que el objeto no tiene. "
            "Revisa el tipo de dato y sus métodos.",
        ],
        3: [
            "El objeto que estás usando no tiene ese método o propiedad. "
            "Quizás es de otro tipo del que crees. Usa type() para confirmarlo.",
            "Cada tipo en Python tiene sus propios métodos. Asegúrate de que "
            "el objeto sea del tipo correcto antes de llamar ese atributo.",
        ],
    },

    # ── Errores de colecciones ─────────────────────────────────────────────────

    "IndexError": {
        1: [
            "ERROR: ÍNDICE FUERA DE RANGO. El acceso excede los límites "
            "de la colección.",
            "ACCESO INVÁLIDO. El índice solicitado no existe en la secuencia.",
        ],
        2: [
            "Intentaste acceder a una posición que no existe en la lista. "
            "Recuerda que los índices empiezan en 0.",
            "IndexError: la lista no tiene esa posición. Si tiene 3 elementos, "
            "el último índice es 2, no 3.",
        ],
        3: [
            "El índice que buscas está fuera de los límites de la lista. "
            "Recuerda: una lista de N elementos tiene índices de 0 a N-1.",
            "Intenta imprimir len(lista) antes de acceder para verificar "
            "el tamaño real. El índice está un paso más allá del límite.",
        ],
    },

    "KeyError": {
        1: [
            "ERROR: CLAVE NO ENCONTRADA. El diccionario no contiene "
            "la clave especificada.",
            "ACCESO INVÁLIDO. La clave consultada no existe en el mapa de datos.",
        ],
        2: [
            "Esa clave no existe en el diccionario. Verifica el nombre exacto, "
            "incluyendo mayúsculas.",
            "KeyError: el diccionario no tiene esa entrada. Usa .get() para "
            "accesos seguros sin excepción.",
        ],
        3: [
            "El diccionario no tiene esa clave. Puedes usar "
            "dict.get('clave', valor_default) para evitar el error si no estás seguro.",
            "Revisa que la clave exista con 'clave in diccionario' "
            "antes de acceder directamente.",
        ],
    },

    # ── Errores matemáticos / de ejecución ────────────────────────────────────

    "ZeroDivisionError": {
        1: [
            "ERROR: DIVISIÓN POR CERO. La operación matemática es indefinida.",
            "OPERACIÓN INVÁLIDA. El divisor es cero. Resultado no computable.",
        ],
        2: [
            "División por cero detectada. Asegúrate de que el denominador "
            "nunca sea 0 antes de dividir.",
            "Operador, no puedes dividir entre cero. Añade una condición "
            "que verifique el divisor antes de operar.",
        ],
        3: [
            "La división por cero es un error matemático clásico. "
            "Antes de dividir, valida que el denominador sea distinto de cero con un if.",
            "Agrega if divisor != 0: antes de la operación. "
            "Así el programa no se rompe con entradas inesperadas.",
        ],
    },

    "RecursionError": {
        1: [
            "ERROR: LÍMITE DE RECURSIÓN EXCEDIDO. "
            "La pila de llamadas ha sido desbordada.",
            "STACK OVERFLOW DETECTADO. "
            "La función se llama a sí misma sin condición de parada.",
        ],
        2: [
            "La función se está llamando a sí misma indefinidamente. "
            "Revisa la condición de parada de la recursión.",
            "RecursionError: falta un caso base en tu función recursiva. "
            "Sin él, el ciclo no termina nunca.",
        ],
        3: [
            "La recursión necesita un caso base para detenerse. Sin él, "
            "la función se llama infinitamente hasta colapsar el stack.",
            "Revisa que tu función tenga una condición if que retorne "
            "directamente sin llamarse de nuevo — ese es el caso base.",
        ],
    },

    "RuntimeError": {
        1: [
            "ERROR DE EJECUCIÓN. El proceso encontró una condición "
            "de error no anticipada.",
            "FALLO EN TIEMPO DE EJECUCIÓN. "
            "El sistema no pudo completar la operación.",
        ],
        2: [
            "Ocurrió un error en tiempo de ejecución. "
            "Revisa la lógica del programa paso a paso.",
            "RuntimeError: algo inesperado ocurrió mientras el código corría. "
            "Verifica las entradas y el flujo del programa.",
        ],
        3: [
            "Es un error de ejecución general. Trata de aislar qué parte "
            "del código lo causa añadiendo prints intermedios.",
            "Sigue el flujo del programa mentalmente con los datos de entrada. "
            "El error está donde la lógica se rompe.",
        ],
    },

    # ── Estados de resultado (sin excepción Python) ───────────────────────────

    "failed": {
        1: [
            "RESULTADO INCORRECTO. La salida no coincide con el objetivo. "
            "Reanaliza los parámetros de salida.",
            "COMPARACIÓN FALLIDA. "
            "Output generado no corresponde al output esperado.",
        ],
        2: [
            "La ejecución fue limpia, pero el resultado no abre la puerta. "
            "Vuelve a calcular.",
            "El código corrió sin errores, pero la salida no es la esperada. "
            "Revisa espacios, mayúsculas y el formato exacto.",
        ],
        3: [
            "Buen intento. El código funciona pero la salida difiere. "
            "Compara el formato esperado: espacios, saltos de línea y mayúsculas importan.",
            "Casi. La lógica parece correcta pero el output no coincide exactamente. "
            "Revisa si hay un espacio de más, o si falta un salto de línea.",
        ],
    },

    "success": {
        1: [
            "VALIDACIÓN EXITOSA. Output verificado. "
            "Acceso concedido al siguiente nivel.",
            "COINCIDENCIA CONFIRMADA. Misión completada. Proceder.",
        ],
        2: [
            "Misión completada, Operador. El resultado es exactamente el esperado. "
            "Acceso al siguiente nivel concedido.",
            "Perfecto. El código y la salida son correctos. "
            "El Nexo ha sido desbloqueado.",
        ],
        3: [
            "¡Excelente trabajo, Operador! Eso es exactamente lo que el sistema "
            "esperaba. El siguiente nivel está desbloqueado.",
            "Lo lograste. Código limpio, resultado correcto. "
            "DAKI está orgulloso de este avance.",
        ],
    },

    "timeout": {
        1: [
            "TIMEOUT: PROCESO TERMINADO. "
            "El código no completó en el tiempo asignado.",
            "LÍMITE DE TIEMPO EXCEDIDO. Revisa bucles y condiciones de parada.",
        ],
        2: [
            "El tiempo límite fue excedido. Hay un bucle que no termina. "
            "Revisa tus condiciones de salida.",
            "Tiempo agotado. El código no terminó en 5 segundos. "
            "Busca el bucle infinito.",
        ],
        3: [
            "El código se quedó corriendo. Revisa todos tus bucles while "
            "y asegúrate de que siempre exista una salida posible.",
            "Sigue el while paso a paso: ¿la condición alguna vez se vuelve False? "
            "Si no, ese es el problema.",
        ],
    },

    # "TimeoutError" puede llegar como error_type desde el sandbox
    "TimeoutError": {
        1: [
            "TIMEOUT: LÍMITE DE TIEMPO EXCEDIDO. "
            "El proceso fue terminado por el monitor de ejecución.",
            "EJECUCIÓN TERMINADA. El código no completó en el tiempo asignado.",
        ],
        2: [
            "El código tardó demasiado. Revisa si tienes un bucle infinito "
            "o una operación muy costosa.",
            "Tiempo agotado, Operador. Probablemente hay un while sin condición "
            "de salida. Añade una condición que detenga el bucle.",
        ],
        3: [
            "El código excedió el tiempo límite. Lo más común es un while True "
            "sin break, o un contador que nunca llega a su meta. Revísalo.",
            "Un bucle infinito consume todos los recursos disponibles. Asegúrate "
            "de que el while tenga una condición que eventualmente sea falsa.",
        ],
    },
}

# Fallback cuando el error_type no está mapeado en _MESSAGES
_FALLBACK: dict[int, str] = {
    1: "ERROR NO CLASIFICADO. Revisa el output del compilador para más detalles.",
    2: "Ocurrió un error que no reconozco. Lee el mensaje de error y ajusta el código.",
    3: "Ese es un error poco común. Lee el mensaje completo — "
       "Python suele indicar exactamente dónde está el problema.",
}


# ─── Función principal ────────────────────────────────────────────────────────

def get_daki_message(event: str, daki_level: int = 1) -> str:
    """
    Retorna un mensaje de DAKI para el evento y nivel dados.

    Args:
        event:      Tipo de excepción Python ("SyntaxError", "NameError", ...)
                    o estado de resultado ("success", "failed", "timeout").
        daki_level: Nivel evolutivo de DAKI (1, 2 o 3). Se normaliza al rango [1, 3].

    Returns:
        Frase de DAKI lista para mostrar en UI y/o reproducir con Web Speech API.
    """
    level = max(1, min(3, int(daki_level)))  # clamp 1-3
    pool  = _MESSAGES.get(event, {}).get(level)

    if not pool:
        return _FALLBACK.get(level, _FALLBACK[1])

    return random.choice(pool)
