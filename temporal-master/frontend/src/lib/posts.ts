export interface Post {
  slug:          string
  title:         string
  description:   string
  publishedAt:   string   // 'YYYY-MM-DD'
  readTime:      string   // '8 min'
  category:      'python' | 'carrera' | 'metodologia'
  categoryLabel: string
  content:       string   // HTML string rendered via dangerouslySetInnerHTML
}

// ─── Contenido de los posts ───────────────────────────────────────────────────

const POST_APRENDER_PYTHON: Post = {
  slug:          'aprender-python-desde-cero-2026',
  title:         'Cómo aprender Python desde cero en 2026 (y conseguir trabajo en LATAM)',
  description:   'La guía que nadie escribió: ruta de aprendizaje real, métricas que importan y lo que las empresas tech buscan en LATAM. Sin teoría muerta.',
  publishedAt:   '2026-04-24',
  readTime:      '9 min',
  category:      'python',
  categoryLabel: 'Python',
  content: `
<p>Si estás leyendo esto, ya sabés que Python es el lenguaje más demandado del mercado tech en 2026. Lo que nadie te dice claramente es <strong>cómo aprenderlo de verdad</strong> — sin caer en el loop eterno de tutoriales incompletos y teoría que no sirve para nada en producción.</p>

<p>Esta guía no es otro tutorial de Python. Es el mapa que debería existir desde el primer día.</p>

<h2>Por qué Python y no otro lenguaje</h2>

<p>La pregunta más común cuando alguien empieza: ¿Python, JavaScript o Java? Depende de qué querés hacer, pero si el objetivo es conseguir trabajo o freelancear en el corto plazo, Python gana por goleada.</p>

<ul>
<li><strong>Demanda laboral:</strong> Python aparece en más del 70% de las ofertas de trabajo tech en LATAM que requieren un lenguaje específico.</li>
<li><strong>Versatilidad real:</strong> Un solo lenguaje cubre backend, automatización, data science, scripting y desarrollo de IA. No tenés que elegir una especialidad antes de aprender.</li>
<li><strong>Curva de entrada:</strong> La sintaxis es deliberadamente legible. Podés escribir código que hace cosas reales en la primera semana.</li>
<li><strong>Ecosistema:</strong> FastAPI, Django, Pandas, NumPy, LangChain — el ecosistema de librerías de Python no tiene rival en amplitud.</li>
</ul>

<h2>El error más grande de los principiantes</h2>

<p>La mayoría empieza con videos de YouTube. No está mal. El problema es lo que hacen con ese contenido.</p>

<p>Miran el video, entienden lo que explica, reproducen el código mientras lo miran, y asumen que aprendieron. No funciona así. El cerebro crea una ilusión de competencia cuando procesa información pasivamente. El momento en que cerrás el video y tratás de replicarlo desde cero, aparece el bloqueo.</p>

<blockquote>
<p>La comprensión pasiva y la capacidad de producción son habilidades distintas. Solo se desarrolla la segunda escribiendo código real con errores reales.</p>
</blockquote>

<p>La solución es simple pero ignorada: <strong>escribir código incorrecto, debuggearlo, y entender por qué falló</strong>. Eso es aprender Python. No es cómodo. No es rápido. Es lo único que funciona.</p>

<h2>La ruta de aprendizaje que realmente funciona</h2>

<p>Hay un orden que maximiza la retención y minimiza el tiempo hasta ser empleable. No es el orden en que la mayoría enseña Python.</p>

<h3>Fase 1 — Variables, tipos y control de flujo (semanas 1-2)</h3>

<p>No es glamoroso, pero sin esto no hay nada. Strings, enteros, listas, diccionarios, condicionales y loops. El objetivo no es memorizar — es saber qué herramienta usar para qué problema.</p>

<pre><code>nombres = ["Ana", "Luis", "Mario"]
for nombre in nombres:
    if len(nombre) > 4:
        print(f"{nombre} tiene un nombre largo")</code></pre>

<p>Si podés leer ese código y saber exactamente qué imprime sin ejecutarlo, pasaste la Fase 1.</p>

<h3>Fase 2 — Funciones y manejo de errores (semanas 3-4)</h3>

<p>Las funciones son el primer salto de complejidad real. No solo escribirlas — entender cuándo crear una y cuándo no. El manejo de errores con <code>try/except</code> es lo que separa el código que funciona en tu computadora del código que funciona en producción.</p>

<pre><code>def dividir(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None</code></pre>

<h3>Fase 3 — Estructuras de datos (semanas 5-6)</h3>

<p>Listas, diccionarios, sets, tuplas — no como definición sino como herramientas. Cuándo usar cada una. Cómo buscar, filtrar y transformar colecciones de datos sin escribir código innecesariamente complejo.</p>

<h3>Fase 4 — POO y módulos (semanas 7-8)</h3>

<p>Programación Orientada a Objetos en Python es una de las cosas más sobrecomplicadas por materiales mal diseñados. En la práctica, necesitás entender clases, herencia básica y encapsulamiento. No más. El resto se aprende con el proyecto.</p>

<h3>Fase 5 — Un proyecto real (semanas 9-12)</h3>

<p>Esta es la fase que más se saltean y la más importante. Un proyecto real — una API simple con FastAPI, un script de automatización, una herramienta de análisis de datos — integra todo lo anterior de una forma que ningún tutorial puede replicar.</p>

<h2>Cómo medir tu progreso</h2>

<p>La mayoría de los cursos miden progreso con porcentajes de completado o videos vistos. Ninguno de esos números importa al mercado laboral.</p>

<p>Las únicas métricas que importan al aprender Python desde cero:</p>

<ul>
<li><strong>¿Podés escribir código que resuelve un problema nuevo sin buscar la solución?</strong> Eso es competencia real.</li>
<li><strong>¿Podés leer el código de otra persona y entender qué hace?</strong> Eso es lo que hacés el 70% de tu tiempo en un trabajo real.</li>
<li><strong>¿Podés debuggear un error que nunca viste antes?</strong> Eso define si sobrevivís en producción.</li>
</ul>

<h2>Lo que las empresas tech buscan en LATAM en 2026</h2>

<p>Las empresas que contratan devs remotos en LATAM no buscan desarrolladores senior con 10 años de experiencia. Buscan perfiles específicos con habilidades demostrables.</p>

<ul>
<li><strong>Python Backend Developer:</strong> FastAPI o Django, bases de datos relacionales, autenticación básica, deploy en la nube. Rango: $40k-$80k USD/año remoto.</li>
<li><strong>Automatización / scripting:</strong> Python para automatizar procesos internos, integrar APIs, procesar datos. El perfil más accesible para alguien que aprendió en 3-6 meses.</li>
<li><strong>Data Analyst con Python:</strong> Pandas, visualizaciones, limpieza de datos, reportes automatizados. Alta demanda en fintech y ecommerce de LATAM.</li>
</ul>

<p>El patrón es claro: no necesitás saber todo Python. Necesitás saber <strong>una cosa bien</strong> y poder demostrarlo con código.</p>

<h2>El paso siguiente</h2>

<p>Hay un momento específico en el aprendizaje de Python donde el progreso se desacelera. Generalmente ocurre después de las primeras 4-6 semanas. Entendés los conceptos, podés resolver ejercicios simples, pero los proyectos reales se sienten inalcanzables.</p>

<p>Ese es exactamente el punto donde necesitás cambiar cómo aprendés: pasar de consumir contenido a escribir código que recibe feedback inmediato sobre sus errores específicos.</p>

<p>DAKI entrena exactamente ese gap — no con videos, sino con 195 misiones de código ejecutable y una IA que analiza tu lógica en tiempo real y construye la pregunta exacta que te fuerza a resolver el problema vos mismo.</p>
`,
}

const POST_PYTHON_TRABAJO: Post = {
  slug:          'python-para-trabajo-remoto-latam',
  title:         'Python para conseguir trabajo remoto en LATAM: lo que realmente te piden en 2026',
  description:   'Las skills concretas, los rangos salariales y el tipo de código que separa a los que consiguen trabajo de los que siguen estudiando.',
  publishedAt:   '2026-04-17',
  readTime:      '7 min',
  category:      'carrera',
  categoryLabel: 'Carrera',
  content: `
<p>Hay una diferencia enorme entre <em>aprender Python</em> y <em>ser contratable con Python</em>. Esta guía es sobre la segunda parte.</p>

<p>Trabajé con decenas de devs que llevan meses estudiando Python pero no saben qué mostrar en una entrevista. No porque les falte conocimiento — porque nadie les dijo qué conocimiento importa en el mercado real de LATAM.</p>

<h2>Qué buscan las empresas que contratan remoto desde LATAM</h2>

<p>Las empresas tech que contratan en LATAM (tanto startups locales como empresas de EEUU/Europa con equipos distribuidos) tienen necesidades muy concretas.</p>

<h3>Perfil 1 — Python Backend Developer</h3>

<p>El perfil más demandado y mejor pagado para alguien aprendiendo desde cero.</p>

<ul>
<li>FastAPI o Django (FastAPI tiene más demanda en 2026)</li>
<li>PostgreSQL o SQLite — queries básicas, ORM</li>
<li>Autenticación con JWT</li>
<li>Git y GitHub — no solo commits, sino pull requests y code review</li>
<li>Deploy básico: Docker + Render o Railway</li>
</ul>

<p>Rango salarial: <strong>$35k-$80k USD/año</strong> dependiendo de experiencia y empresa.</p>

<h3>Perfil 2 — Automatización y scripting</h3>

<p>El perfil más accesible para alguien con 3-5 meses de Python. No requiere conocimiento de frameworks.</p>

<ul>
<li>Requests y BeautifulSoup (scraping básico)</li>
<li>Selenium o Playwright para automatización de browsers</li>
<li>Pandas para procesar archivos CSV, Excel, JSON</li>
<li>Integración con APIs REST (REST, webhooks, OAuth básico)</li>
<li>Scheduling con cron o APScheduler</li>
</ul>

<p>Rango salarial: <strong>$20k-$45k USD/año</strong> o freelance por proyecto.</p>

<h3>Perfil 3 — Data Analyst con Python</h3>

<p>Alta demanda en fintech, ecommerce y healthtech de LATAM. Generalmente combinado con SQL.</p>

<ul>
<li>Pandas y NumPy para manipulación de datos</li>
<li>Matplotlib o Plotly para visualizaciones</li>
<li>SQL intermedio (joins, subqueries, window functions)</li>
<li>Jupyter Notebooks para análisis reproducible</li>
</ul>

<p>Rango salarial: <strong>$25k-$60k USD/año</strong>.</p>

<h2>El código que te contrata vs el código que te descarta</h2>

<p>En una entrevista técnica o en la revisión de tu portfolio, hay patrones que inmediatamente señalizan si alguien sabe trabajar en equipo o no.</p>

<h3>Señales de un dev contratable</h3>

<pre><code>from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Usuario(BaseModel):
    nombre: str
    email: str

@app.post("/usuarios")
def crear_usuario(usuario: Usuario):
    if not usuario.email:
        raise HTTPException(status_code=400, detail="Email requerido")
    return {"mensaje": f"Usuario {usuario.nombre} creado"}</code></pre>

<p>Validación de inputs. Manejo explícito de errores. Tipado claro.</p>

<h3>Señales de un dev no contratable</h3>

<pre><code># El mismo endpoint sin validación
@app.post("/usuarios")
def crear_usuario(nombre, email):
    # si falla, falla — ya veremos
    db.save(nombre, email)
    return "ok"</code></pre>

<p>Sin tipos. Sin validación. Sin manejo de errores. Código que funciona en local pero explota en producción.</p>

<h2>Lo que el mercado no te dice explícitamente</h2>

<p>Las ofertas de trabajo dicen "buscamos Python developer". Lo que no dicen es que esperan que el candidato entienda <strong>por qué</strong> el código falla, no solo <strong>cómo</strong> hacerlo funcionar.</p>

<p>Esa diferencia se construye con práctica deliberada: escribir código que falla, leer el traceback completo, entender qué causó el error, y arreglarlo sin copiar la solución.</p>

<p>En DAKI cada misión está diseñada exactamente para eso: código que corre en un sandbox real, errores reales que DAKI analiza, y feedback específico sobre tu lógica particular — no respuestas genéricas.</p>
`,
}

const POST_CODE_REVIEW: Post = {
  slug:          'errores-python-code-review',
  title:         'Los 7 errores de Python que destruyen tu primer code review',
  description:   'El 73% de los devs junior falla su primer code review. Estos son los errores concretos que lo causan — y cómo entrenarlos antes de que cuenten.',
  publishedAt:   '2026-04-10',
  readTime:      '6 min',
  category:      'python',
  categoryLabel: 'Python',
  content: `
<p>El 73% de los desarrolladores junior falla su primer code review real. No por falta de conocimiento teórico — por patrones específicos que nadie les señaló durante el aprendizaje.</p>

<p>Acá están los 7 errores más comunes, con el código que los produce y la versión correcta.</p>

<h2>Error 1 — No validar inputs</h2>

<p>El error más frecuente y el más costoso en producción. Código que asume que los datos de entrada siempre vienen en el formato esperado.</p>

<pre><code># ❌ Sin validación
def calcular_descuento(precio, porcentaje):
    return precio * (1 - porcentaje / 100)

# ✓ Con validación
def calcular_descuento(precio: float, porcentaje: float) -> float:
    if precio < 0 or porcentaje < 0 or porcentaje > 100:
        raise ValueError("Precio y porcentaje deben ser positivos")
    return precio * (1 - porcentaje / 100)</code></pre>

<h2>Error 2 — Variables sin nombres descriptivos</h2>

<p>El código con variables de una letra se escribe rápido y se lee lento. En un equipo, el tiempo de lectura importa más que el de escritura.</p>

<pre><code># ❌ Ilegible
def p(x, y):
    r = []
    for i in x:
        if i > y:
            r.append(i)
    return r

# ✓ Auto-documenta
def filtrar_mayores(numeros: list, umbral: float) -> list:
    return [n for n in numeros if n > umbral]</code></pre>

<h2>Error 3 — Atrapar excepciones en blanco</h2>

<p>El <code>except Exception as e: pass</code> silencia errores reales. Es el equivalente a apagar la alarma de incendio en lugar de apagar el fuego.</p>

<pre><code># ❌ Silencia todo
try:
    resultado = procesar_datos(datos)
except:
    pass

# ✓ Manejo específico con logging
try:
    resultado = procesar_datos(datos)
except ValueError as e:
    logger.error(f"Datos inválidos: {e}")
    raise
except ConnectionError as e:
    logger.error(f"Error de conexión: {e}")
    return None</code></pre>

<h2>Error 4 — Queries SQL sin parámetros</h2>

<p>La vulnerabilidad de inyección SQL más clásica. Si el code reviewer lo ve, el PR muere ahí.</p>

<pre><code># ❌ Vulnerable a SQL injection
query = f"SELECT * FROM usuarios WHERE email = '{email}'"
cursor.execute(query)

# ✓ Con parámetros parametrizados
query = "SELECT * FROM usuarios WHERE email = %s"
cursor.execute(query, (email,))</code></pre>

<h2>Error 5 — Lógica duplicada en lugar de funciones</h2>

<p>Copiar y pegar código que hace lo mismo en varios lugares. Cuando hay que cambiar algo, hay que cambiarlo en todos los lugares — y siempre se olvida uno.</p>

<pre><code># ❌ Duplicación
if usuario_tipo == "admin":
    nombre = usuario.nombre.strip().lower()
    email = usuario.email.strip().lower()

if usuario_tipo == "editor":
    nombre = usuario.nombre.strip().lower()
    email = usuario.email.strip().lower()

# ✓ Función reutilizable
def normalizar_usuario(usuario):
    return {
        "nombre": usuario.nombre.strip().lower(),
        "email": usuario.email.strip().lower(),
    }</code></pre>

<h2>Error 6 — No usar type hints</h2>

<p>En equipos que usan mypy o Pyright, el código sin type hints genera warnings inmediatos. Más importante: las funciones sin tipos son más difíciles de usar correctamente.</p>

<pre><code># ❌ Sin tipos
def procesar_pedido(pedido, usuario, descuento):
    ...

# ✓ Con tipos
from typing import Optional

def procesar_pedido(
    pedido: Pedido,
    usuario: Usuario,
    descuento: Optional[float] = None
) -> ResultadoPedido:
    ...</code></pre>

<h2>Error 7 — Lógica de negocio en el endpoint</h2>

<p>Poner toda la lógica directamente en el handler de la API. Imposible de testear, difícil de modificar, imposible de reusar.</p>

<pre><code># ❌ Todo en el endpoint
@app.post("/pedidos")
def crear_pedido(datos: dict):
    # 80 líneas de lógica de negocio mezclada con HTTP
    ...

# ✓ Separación de responsabilidades
@app.post("/pedidos")
def crear_pedido(datos: PedidoSchema):
    resultado = servicio_pedidos.crear(datos)
    return {"id": resultado.id}</code></pre>

<h2>Cómo entrenár estos patrones antes del primer trabajo</h2>

<p>Conocer los errores no es suficiente — hay que desarrollar el hábito de evitarlos bajo presión. Eso requiere escribir código real que es evaluado por algo más que "funciona o no funciona".</p>

<p>En DAKI, las misiones están diseñadas para detectar exactamente estos patrones. DAKI analiza tu código y te señala el gap específico — no el error genérico, sino la lógica incorrecta tuya en particular.</p>

<p>El objetivo no es memorizár esta lista. Es que la próxima vez que escribas <code>except: pass</code>, algo en tu cabeza diga "no".</p>
`,
}

// ─── La Matriz de Aprendizaje — 10 artículos ────────────────────────────────

const POST_SOBRECARGA_PROGRESIVA: Post = {
  slug:          'sobrecarga-progresiva-en-el-codigo',
  title:         'La Sobrecarga Progresiva en el Código: Por Qué Repetir el Mismo Tutorial No Sirve',
  description:   'Levantar la misma pesa de 5kg todos los días no genera hipertrofia. Hacer el mismo tutorial básico de Python 20 veces tampoco. Cómo aplicar incrementos de dificultad reales para forzar al cerebro a adaptarse.',
  publishedAt:   '2026-04-22',
  readTime:      '8 min',
  category:      'metodologia',
  categoryLabel: 'Metodología',
  content: `
<p>En 1956, el médico deportivo Theodore Hettinger publicó un estudio que cambió para siempre la ciencia del entrenamiento: el músculo solo crece cuando se le exige más de lo que puede hacer cómodamente. No un poco más. Lo suficiente como para forzar micro-roturas en la fibra muscular. La recuperación de esas roturas es el crecimiento.</p>

<p>El cerebro funciona exactamente igual. Y la mayoría de las personas que aprenden a programar lo hacen completamente ignorando este principio.</p>

<h2>El loop del tutorial eterno</h2>

<p>Hay un patrón que se repite con una regularidad alarmante entre quienes aprenden Python. Empieza con un video introductorio. Termina, entiende, se siente bien. Busca otro video del mismo nivel. Lo termina. Busca otro. Seis meses después, conoce la sintaxis básica pero no puede construir nada real.</p>

<p>El problema no es la falta de dedicación. Es que cada nuevo tutorial está diseñado para ser completado — no para forzar el límite. Son confortables por diseño.</p>

<blockquote>
<p>El aprendizaje ocurre en la zona de máximo esfuerzo sostenible, no en la zona de comodidad. Estar cómodo mientras aprendés es una señal de que no estás progresando.</p>
</blockquote>

<p>El cerebro, como el músculo, solo genera nuevas conexiones neuronales cuando encuentra resistencia genuina. La neurociencia lo llama <em>dificultad deseable</em>: el nivel óptimo de dificultad que maximiza la retención y la transferencia de conocimiento.</p>

<h2>Qué es la sobrecarga progresiva aplicada al código</h2>

<p>En el gimnasio, la sobrecarga progresiva es simple: cuando podés hacer 3 series de 10 repeticiones sin dificultad, aumentás el peso. No lo duplicás — lo incrementás lo suficiente para que las últimas 2-3 repeticiones requieran esfuerzo real.</p>

<p>En programación, el principio es idéntico pero más difícil de medir. ¿Cómo sabés cuándo aumentar la dificultad?</p>

<p>Hay una señal inequívoca: <strong>cuando podés completar el ejercicio sin pensar en los pasos, es hora de cambiar el ejercicio</strong>. No el tema — el nivel de complejidad dentro del tema.</p>

<h3>Ejemplos concretos de progresión</h3>

<p>Supongamos que estás trabajando en funciones con Python. Esta es una progresión correcta:</p>

<pre><code># Nivel 1 — función simple
def saludar(nombre):
    return f"Hola, {nombre}"

# Nivel 2 — parámetros con validación
def saludar(nombre: str, veces: int = 1) -> str:
    if not nombre.strip():
        raise ValueError("El nombre no puede estar vacío")
    return "\n".join([f"Hola, {nombre}"] * veces)

# Nivel 3 — función que recibe y retorna funciones
def repetir(n: int):
    def decorador(func):
        def wrapper(*args, **kwargs):
            for _ in range(n):
                func(*args, **kwargs)
        return wrapper
    return decorador

@repetir(3)
def saludar(nombre: str) -> None:
    print(f"Hola, {nombre}")</code></pre>

<p>Cada nivel usa el mismo concepto base — una función que saluda — pero el incremento cognitivo es sustancial. El nivel 3 requiere entender closures, decoradores y *args. Para alguien que recién terminó el nivel 1, el nivel 3 es inaccesible. Para alguien que dominó el nivel 2, el nivel 3 es difícil pero alcanzable.</p>

<p>Esa franja — difícil pero alcanzable — es la zona donde ocurre el crecimiento.</p>

<h2>La ilusión de competencia</h2>

<p>Existe un fenómeno cognitivo que los investigadores llaman <em>fluency illusion</em>: cuando procesamos información que ya conocemos, la facilidad con la que la entendemos nos hace creer que la dominamos.</p>

<p>Ver un video de Python sobre listas y pensar "esto ya lo sé" mientras lo mirás es exactamente la fluency illusion. El problema aparece 10 minutos después, cuando intentás construir algo con esas listas desde cero.</p>

<p>La única forma de romper la ilusión es intentar recuperar el conocimiento sin apoyo — sin el video, sin el tutorial, sin la solución a la vista. Si podés hacerlo, lo sabés. Si no podés, lo reconocés pero no lo sabés.</p>

<h2>Cómo aplicar la sobrecarga progresiva en la práctica</h2>

<p>Hay tres principios operativos:</p>

<ul>
<li><strong>Medir por dificultad, no por tiempo.</strong> No "estudiar 2 horas". Estudiar hasta llegar a un problema que genuinamente no podés resolver. Ese punto es donde empieza el entrenamiento real.</li>
<li><strong>Incrementos pequeños y frecuentes.</strong> No saltar de funciones básicas a metaprogramación. Agregar una capa de complejidad por vez. La adaptación es incremental, no exponencial.</li>
<li><strong>Recuperación obligatoria.</strong> Después de una sesión de trabajo en el límite de tu capacidad, el cerebro necesita tiempo para consolidar. El progreso no ocurre durante el entrenamiento — ocurre durante el descanso.</li>
</ul>

<p>La paradoja del aprendizaje efectivo es esta: las sesiones que se sienten más duras y producen más errores son las más valiosas. Las sesiones cómodas, donde todo fluye, son las que menos aportan.</p>

<h2>El rol del error en la progresión</h2>

<p>El error no es una señal de fracaso. Es la señal de que el nivel de dificultad es el correcto. Un programa de entrenamiento sin errores es un programa mal calibrado — demasiado fácil para generar adaptación.</p>

<p>Cada <code>TypeError</code>, cada <code>IndentationError</code>, cada resultado incorrecto que no entendés por qué aparece es una micro-rotura muscular. La recuperación — entender qué salió mal y por qué — es el crecimiento.</p>

<p>Los mejores programadores no son los que cometen menos errores. Son los que extraen más información de cada error que cometen.</p>
`,
}

const POST_MEMORIA_MUSCULAR: Post = {
  slug:          'memoria-muscular-sintaxis-kata',
  title:         'Memoria Muscular y Sintaxis: La Kata del Desarrollador',
  description:   'Por qué tipear a mano hasta el código más simple, una y otra vez, es vital. La transición de tener que pensar dónde va cada coma a que los dedos ejecuten el patrón de forma automática.',
  publishedAt:   '2026-04-15',
  readTime:      '7 min',
  category:      'metodologia',
  categoryLabel: 'Metodología',
  content: `
<p>En las artes marciales japonesas existe el concepto de <em>kata</em>: secuencias de movimientos codificados que se repiten miles de veces hasta que dejan de ser movimientos conscientes y se convierten en reflejos. Un practicante de karate no piensa en la posición de cada dedo cuando bloquea un golpe. Su cuerpo lo hace solo.</p>

<p>La sintaxis de Python funciona igual. Y la mayoría de las personas aprenden Python de la manera incorrecta por exactamente la misma razón: no entrenan la kata.</p>

<h2>El cuello de botella de la memoria de trabajo</h2>

<p>La memoria de trabajo — el espacio cognitivo donde procesamos información activamente — tiene una capacidad limitada. Los estudios del psicólogo George Miller la establecieron en aproximadamente 7 elementos simultáneos, con variaciones individuales.</p>

<p>Cuando un programador novato escribe código, una porción significativa de esa memoria de trabajo está ocupada en preguntas de sintaxis: ¿va el dos puntos antes o después del paréntesis? ¿El <code>else</code> va indentado o no? ¿Cómo era la sintaxis del list comprehension?</p>

<p>Cada pregunta de sintaxis ocupa un slot de memoria de trabajo que podría estar dedicado al problema real: la lógica, el algoritmo, la arquitectura.</p>

<blockquote>
<p>Mientras pensás en la sintaxis, no podés pensar en el problema. La automatización de la sintaxis libera capacidad cognitiva para lo que importa.</p>
</blockquote>

<h2>Qué es la memoria muscular en el código</h2>

<p>La memoria muscular — técnicamente llamada memoria procedimental — es el tipo de memoria que almacena secuencias motoras ejecutadas de forma automática. No reside en el córtex prefrontal (donde vive el pensamiento consciente) sino en el cerebelo y los ganglios basales.</p>

<p>Cuando un pianista toca una pieza que conoce, sus dedos ejecutan las notas sin que el cerebro consciente intervenga. El aprendizaje lo hizo el hemisferio derecho y el cerebelo durante cientos de horas de práctica repetitiva.</p>

<p>Lo mismo ocurre con la sintaxis de programación. Después de tipear suficientes veces la estructura de una función:</p>

<pre><code>def nombre_funcion(parametro: tipo) -> tipo_retorno:
    # lógica
    return resultado</code></pre>

<p>...tus dedos ejecutan el patrón sin intervención consciente. La mente queda libre para pensar en qué hace la función, no en cómo se escribe.</p>

<h2>El problema con copiar y pegar</h2>

<p>El copiar y pegar es el enemigo de la kata. Cuando copiás un bloque de código — incluso si lo entendés perfectamente — no estás entrenando los circuitos motores que automatizarán la escritura.</p>

<p>El ojo procesa el código de forma completamente distinta al movimiento de los dedos al tipearlo. Ver es pasivo. Escribir es activo. La construcción de la memoria procedimental requiere la ejecución motora, no la observación.</p>

<p>Esto parece trivial. No lo es. Es la diferencia entre un pianista que escucha una pieza y uno que la toca.</p>

<h3>El ejercicio de la kata en Python</h3>

<p>Estas son las estructuras fundamentales que un Operador debería poder escribir sin pensar:</p>

<pre><code># Comprensiones de lista, diccionario y generadores
cuadrados    = [x**2 for x in range(10) if x % 2 == 0]
conteos      = {palabra: len(palabra) for palabra in lista}
generador    = (x**2 for x in range(1000))

# Context managers
with open("archivo.txt", "r", encoding="utf-8") as f:
    contenido = f.read()

# Decoradores
from functools import wraps

def log_llamada(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Llamando a {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

# Manejo de errores específico
try:
    resultado = operacion_riesgosa()
except ValueError as e:
    logger.error("Valor inválido: %s", e)
    raise
except ConnectionError:
    return None</code></pre>

<p>El ejercicio es simple y brutal: escribir cada uno de estos patrones a mano, desde cero, sin mirar la solución, hasta que el error sea imposible. No entenderlos — ejecutarlos.</p>

<h2>Cuánto tiempo lleva la automatización</h2>

<p>Los estudios sobre adquisición de habilidades motoras sugieren que la automatización de un patrón nuevo requiere entre 400 y 1.000 ejecuciones deliberadas. Para la sintaxis de Python, esto se traduce en semanas de práctica diaria, no horas de lectura.</p>

<p>El indicador concreto de que un patrón está automatizado es este: podés mantener una conversación sobre el problema mientras escribís el código. Si tenés que pausar la conversación para pensar en la sintaxis, no está automatizada todavía.</p>

<h2>La diferencia entre saber y poder</h2>

<p>Hay programadores que saben qué es un decorador. Pueden explicarlo con precisión. Pero cuando tienen que escribir uno desde cero, tardan 5 minutos en la estructura antes de llegar al problema real.</p>

<p>Hay programadores que escriben decoradores en 15 segundos sin pensar y dedican los siguientes minutos al problema que el decorador resuelve.</p>

<p>La diferencia entre ambos no es inteligencia. Es kata.</p>
`,
}

const POST_ACONDICIONAMIENTO_PESADO: Post = {
  slug:          'acondicionamiento-pesado-hojo-undo',
  title:         'El Acondicionamiento Pesado: Los Ejercicios que Ningún Dev Quiere Hacer',
  description:   'En el aprendizaje, como en el combate, hay ejercicios crudos, aburridos y pesados que nadie quiere hacer. Desarmar algoritmos línea por línea con lápiz y papel. La resistencia estructural se forma en la incomodidad.',
  publishedAt:   '2026-04-08',
  readTime:      '7 min',
  category:      'metodologia',
  categoryLabel: 'Metodología',
  content: `
<p>En el karate Goju-Ryu existe el <em>Hojo Undo</em>: entrenamiento suplementario con herramientas de madera y piedra — el nigiri game (jarras de cerámica llenas de arena), el chi ishi (piedra con mango), el ishi sashi (pesas de mano). Ejercicios lentos, repetitivos, sin el glamour del combate. Los practicantes avanzados los hacen. Los que buscan emoción los saltan.</p>

<p>El Hojo Undo no es opcional. Es la diferencia entre tener el movimiento y tener la fuerza estructural para ejecutar ese movimiento cuando el cuerpo está bajo presión real.</p>

<p>En programación existe el equivalente exacto. Y casi nadie lo hace.</p>

<h2>Los ejercicios que el tutorial nunca te va a pedir</h2>

<p>Hay una categoría de ejercicios de aprendizaje que generan resistencia en casi todos los estudiantes cuando los describo: son aburridos, no generan dopamina inmediata y sus beneficios no son visibles en el corto plazo. Por eso funcionan.</p>

<p>El primero y más efectivo es el más detestado: <strong>trazar algoritmos a mano, en papel, línea por línea.</strong></p>

<p>No debuggear con el IDE. No agregar print statements. No buscar en Stack Overflow. Tomar un bloque de código que no entendés del todo y simular su ejecución con papel, lápiz y una tabla de variables.</p>

<pre><code># Algoritmo a trazar: inversión de cadena con recursión
def invertir(s: str) -> str:
    if len(s) <= 1:
        return s
    return invertir(s[1:]) + s[0]</code></pre>

<p>Trazar <code>invertir("hola")</code> manualmente:</p>

<pre><code>llamada 1: s = "hola"  → invertir("ola") + "h"
llamada 2: s = "ola"   → invertir("la")  + "o"
llamada 3: s = "la"    → invertir("a")   + "l"
llamada 4: s = "a"     → return "a"
retorno:   "a" + "l" + "o" + "h" = "aloh"</code></pre>

<p>Este ejercicio, hecho con papel y lápiz, construye algo que el debugger no puede construir: la capacidad de modelar la ejecución de código en tu cabeza sin herramientas externas. Eso es lo que hace un programador senior cuando lee código ajeno y entiende instantáneamente qué pasa.</p>

<h2>Por qué el papel y el lápiz son mejores que el debugger para aprender</h2>

<p>El debugger es una herramienta de producción. Como todas las herramientas, amplifica capacidades que ya existen. Si no tenés el modelo mental del flujo de ejecución, el debugger te muestra valores que no entendés por qué cambian.</p>

<p>El tracing manual fuerza al cerebro a construir ese modelo interno. No lo consulta — lo construye. La diferencia es la misma que entre consultar el GPS y aprender el mapa.</p>

<blockquote>
<p>Después de trazar 50 algoritmos a mano, el código empieza a tener peso físico en tu cabeza. Las estructuras se vuelven predecibles. El flujo se vuelve evidente. Eso no se aprende leyendo sobre programación.</p>
</blockquote>

<h2>El segundo ejercicio pesado: reescribir código sin mirarlo</h2>

<p>Tomar un fragmento de código que entendés (o creés que entendés), cerrarlo, y reescribirlo desde cero sin referencia. Solo con lo que recordás.</p>

<p>Lo que este ejercicio revela es brutal: la distancia entre reconocer código y producir código. Reconocer es pasivo y fácil. Producir requiere haber internalizado la estructura a un nivel que el reconocimiento no mide.</p>

<p>Cuando no podés reescribir algo que acabás de leer, no lo sabés. Lo reconocés, que es un nivel cognitivo completamente diferente.</p>

<h2>El tercero: implementar sin librerías</h2>

<p>Python tiene módulos para casi todo. El estudiante que solo aprende usando librerías está usando muletas cognitivas sin saberlo.</p>

<p>Implementar estructuras de datos y algoritmos clásicos desde cero — no para usarlos en producción, sino como ejercicio — construye una comprensión estructural que el import nunca va a dar:</p>

<pre><code># No usar collections.deque — implementar la cola
class Cola:
    def __init__(self):
        self._datos: list = []

    def encolar(self, item) -> None:
        self._datos.append(item)

    def desencolar(self):
        if not self._datos:
            raise IndexError("Cola vacía")
        return self._datos.pop(0)

    def __len__(self) -> int:
        return len(self._datos)</code></pre>

<p>¿Vas a usar esta implementación en un proyecto real? No. ¿Va a cambiar fundamentalmente tu comprensión de cómo funciona una cola? Sí.</p>

<h2>La resistencia estructural y por qué importa bajo presión</h2>

<p>El Hojo Undo en las artes marciales no entrena movimientos bonitos para la demostración. Entrena la estructura corporal que permite ejecutar cualquier movimiento cuando el cuerpo está bajo estrés, cansancio o impacto.</p>

<p>Los ejercicios cognitivos pesados hacen lo mismo: construyen la estructura mental que permite entender código nuevo, debuggear problemas desconocidos y diseñar soluciones bajo la presión de un deadline real.</p>

<p>El entrenamiento cómodo produce habilidades cómodas. El entrenamiento incómodo produce resistencia estructural.</p>
`,
}

const POST_TENSION_ISOMETRICA: Post = {
  slug:          'tension-isometrica-frente-al-bug',
  title:         'Tensión Isométrica frente al Bug: El Arte de No Rendirse',
  description:   'El poder de quedarse sosteniendo el problema. La ciencia de mantener la tensión mental frente al error sin rendirse — y por qué los mejores debuggers son los más pacientes.',
  publishedAt:   '2026-04-01',
  readTime:      '8 min',
  category:      'python',
  categoryLabel: 'Python',
  content: `
<p>La contracción isométrica en el entrenamiento físico ocurre cuando el músculo genera fuerza sin cambiar de longitud. Sostener una pesa en el punto de máxima tensión, sin bajarla ni subirla. Es el ejercicio más incómodo y uno de los más efectivos para construir fuerza funcional.</p>

<p>Hay un equivalente directo en programación. Ocurre cuando estás frente a un bug que no entendés, con el impulso de buscar inmediatamente la solución en Google, y en lugar de ceder, sostenés la tensión. Seguís mirando el código. Seguís pensando. No aflojás.</p>

<p>Ese momento es donde se construye el programador real.</p>

<h2>La respuesta de huida ante el error</h2>

<p>Cuando la consola imprime un error, especialmente uno extenso y en rojo, el cerebro activa respuestas de estrés similares a las que activaría ante una amenaza física. La amígdala interpreta la situación como adversa. El cortisol sube. El impulso es alejarse del problema.</p>

<p>En el contexto del aprendizaje de programación, "alejarse" tiene una forma muy concreta: abrir Google y buscar el mensaje de error exacto. Stack Overflow tiene la respuesta. Copiarla y pegarla hace que el error desaparezca. El cerebro interpreta eso como resolución del problema y genera una dosis de alivio.</p>

<p>Pero no resolviste el problema. Copiaste la solución de alguien que lo resolvió.</p>

<blockquote>
<p>La diferencia entre el programador junior y el senior no es que el senior comete menos errores. Es que el senior pasó más tiempo sosteniendo la tensión frente a errores que no entendía.</p>
</blockquote>

<h2>El protocolo de los 15 minutos</h2>

<p>Hay una regla no escrita en equipos de desarrollo senior: antes de pedir ayuda o buscar la solución, dedicar al menos 15 minutos de esfuerzo genuino al problema. No 15 minutos mirando el error. 15 minutos de investigación activa.</p>

<p>El procedimiento de tensión isométrica frente a un bug tiene pasos concretos:</p>

<ul>
<li><strong>Leer el traceback completo, desde abajo hacia arriba.</strong> Python imprime el traceback con la causa raíz al final. La mayoría de los novatos lee solo la última línea.</li>
<li><strong>Reproducir el error en el contexto mínimo.</strong> Aislar el fragmento de código que falla. Crear un ejemplo mínimo que reproduzca el problema.</li>
<li><strong>Formular hipótesis antes de probar.</strong> Antes de cambiar cualquier línea, hacer una predicción explícita: "creo que el error está aquí porque..."</li>
<li><strong>Probar la hipótesis, no la solución.</strong> Cambiar una sola variable a la vez para confirmar o refutar la hipótesis.</li>
</ul>

<pre><code># El traceback que asusta al novato:
Traceback (most recent call last):
  File "app.py", line 45, in procesar_datos
    resultado = calcular(entrada["valor"])
  File "app.py", line 23, in calcular
    return suma / len(datos)
ZeroDivisionError: division by zero

# Lo que revela cuando se lee correctamente:
# 1. El error es ZeroDivisionError en la línea 23
# 2. Ocurre en calcular(), llamada desde procesar_datos()
# 3. len(datos) es 0 — datos está vacío
# 4. La pregunta es: ¿por qué datos llega vacío a calcular()?</code></pre>

<p>Esa secuencia de lectura tarda 2 minutos y resuelve el 60% de los errores sin necesitar Stack Overflow. Pero requiere sostener la tensión lo suficiente como para leer en lugar de reaccionar.</p>

<h2>La construcción de la tolerancia a la frustración</h2>

<p>La tolerancia a la frustración no es una característica de personalidad fija. Es una habilidad entrenada. Cada vez que sostenés la tensión frente a un problema difícil y llegás a la solución por tu cuenta, el umbral de frustración sube un poco.</p>

<p>Cada vez que cedés y buscás la respuesta antes de tiempo, el umbral baja.</p>

<p>Los programadores con más de 5 años de experiencia tienen, en general, una tolerancia a la frustración mucho mayor que los novatos. No porque sean más tranquilos de naturaleza. Porque entrenaron esa tolerancia resolviendo miles de problemas que en algún momento parecían irresolubles.</p>

<h2>Cuándo soltar la tensión</h2>

<p>La tensión isométrica tiene un límite. En el gimnasio, llega un punto donde mantener el peso daña el músculo en lugar de entrenarlo. En el debugging, llega un punto donde seguir solo es menos eficiente que buscar orientación.</p>

<p>La regla práctica: si después de 15-20 minutos de investigación activa no tenés ninguna hipótesis sobre la causa del error, es momento de buscar. No la solución — información sobre el tipo de error. La distinción es importante.</p>

<p>Buscar "ZeroDivisionError Python cuando" es investigación. Buscar "ZeroDivisionError line 23 app.py fix" y copiar lo que aparece es evasión.</p>

<h2>El músculo que estás construyendo</h2>

<p>Cada sesión de tensión isométrica frente a un bug construye algo que ningún tutorial puede enseñar: la capacidad de mantenerse funcional bajo incertidumbre.</p>

<p>En producción, los problemas no vienen con solución adjunta. Los sistemas fallan de maneras inesperadas, en momentos inoportunos, con errores que nadie ha documentado. La única herramienta disponible es la capacidad de sostener la presión y pensar con claridad.</p>

<p>Esa capacidad se entrena en el estudio. Un bug a la vez.</p>
`,
}

const POST_CONTROL_PANICO: Post = {
  slug:          'control-de-panico-bajo-fuego',
  title:         'Control de Pánico bajo Fuego: La Respiración del Operador',
  description:   'Qué le pasa a tu amígdala cuando la consola escupe 50 líneas de error en rojo. Técnicas de anclaje y control para mantener el córtex prefrontal activo frente al caos.',
  publishedAt:   '2026-03-25',
  readTime:      '9 min',
  category:      'metodologia',
  categoryLabel: 'Metodología',
  content: `
<p>A las 2:47 AM, el sistema de pagos de una plataforma con 40,000 usuarios activos deja de procesar transacciones. La consola muestra 200 líneas de error en rojo. Los mensajes de Slack suenan cada 30 segundos. El CTO acaba de entrar al canal.</p>

<p>En ese momento, la mayoría de los desarrolladores junior cometen el error más costoso del incident response: actúan reactivamente. Empiezan a cambiar código sin entender el problema. Reinician servicios aleatoriamente. Hacen revertes de commits que no tienen relación con el error.</p>

<p>El pánico desactiva exactamente las capacidades cognitivas que el problema requiere.</p>

<h2>Lo que le pasa al cerebro bajo presión</h2>

<p>Cuando percibimos una amenaza — y un sistema en producción cayendo es una amenaza genuina para el cerebro — la amígdala activa el eje hipotalámico-hipofisario-suprarrenal. Cortisol y adrenalina inundan el sistema. El flujo sanguíneo se redistribuye hacia los músculos. La frecuencia cardíaca sube.</p>

<p>El córtex prefrontal — la región responsable del pensamiento analítico, la planificación y el control de impulsos — recibe menos sangre y funciona con capacidad reducida. El cerebro entra en modo de respuesta rápida, no de análisis profundo.</p>

<p>Este mecanismo fue útil evolutivamente para escapar de depredadores. Para debuggear un sistema distribuido en producción, es devastador.</p>

<blockquote>
<p>El pánico es biológicamente incompatible con el debugging efectivo. No es una cuestión de actitud — es una cuestión de neurobiología. El control del pánico es una habilidad técnica.</p>
</blockquote>

<h2>La respiración como interruptor del sistema nervioso</h2>

<p>El sistema nervioso autónomo tiene dos modos: simpático (activación, lucha/huida) y parasimpático (descanso, recuperación). La respiración es uno de los pocos procesos fisiológicos que puede activarse conscientemente para cambiar entre estos modos.</p>

<p>La respiración táctica — utilizada por unidades militares de élite, equipos de cirugía de emergencia y bomberos — consiste en un patrón específico que activa el sistema nervioso parasimpático independientemente del nivel de estrés del entorno:</p>

<ul>
<li>Inhalar por 4 segundos</li>
<li>Sostener 4 segundos</li>
<li>Exhalar por 4 segundos</li>
<li>Sostener 4 segundos</li>
</ul>

<p>Dos ciclos de este patrón (32 segundos en total) reducen la frecuencia cardíaca y aumentan el flujo sanguíneo al córtex prefrontal de manera medible. Parece trivial. Funciona.</p>

<h2>El protocolo de incident response del Operador</h2>

<p>Antes de tocar una sola línea de código en un sistema con problemas activos, hay un protocolo de 5 pasos:</p>

<h3>1. Detener. Respirar.</h3>
<p>Sin excepción. No importa qué tan crítica sea la situación. 32 segundos de respiración táctica no van a hundir el sistema. El pánico sí puede.</p>

<h3>2. Definir el problema con precisión</h3>
<pre><code># Pregunta incorrecta: "¿Por qué no funciona?"
# Pregunta correcta: "¿Qué cambió entre el último deploy exitoso y ahora?"

# Información útil:
# - ¿Cuándo empezó el error exactamente?
# - ¿Qué deploy/cambio ocurrió más cercano a ese momento?
# - ¿Afecta a todos los usuarios o a un subconjunto?
# - ¿El error es consistente o intermitente?</code></pre>

<h3>3. Observar sin modificar</h3>
<p>Los primeros 3-5 minutos deben ser solo de observación. Logs, métricas, traces. No tocar nada. Entender el estado actual antes de intentar cambiarlo.</p>

<h3>4. Hipótesis antes de acción</h3>
<p>Formular explícitamente la hipótesis: "Creo que el problema es X porque Y". Escribirla. Si la hipótesis es incorrecta, el proceso de falsificarla enseña más que una búsqueda aleatoria de soluciones.</p>

<h3>5. Un cambio a la vez, con revertibilidad</h3>
<p>Nunca hacer múltiples cambios simultáneamente bajo presión. Si el sistema empeora, no vas a saber cuál de los cambios lo causó. Cada cambio debe ser reversible y probado antes del siguiente.</p>

<h2>El anclaje cognitivo</h2>

<p>Los pilotos militares entrenan el <em>tunnel vision</em> — la tendencia bajo estrés extremo a fijarse en un solo elemento del problema ignorando el contexto completo. El antídoto es el anclaje: una pregunta formulada conscientemente que obliga a ampliar el foco.</p>

<p>En el contexto del desarrollo, la pregunta de anclaje estándar es: <strong>"¿Qué sé con certeza y qué estoy asumiendo?"</strong></p>

<p>Bajo estrés, el cerebro mezcla hechos con inferencias. Separar lo que se sabe con certeza (el log dice X, el error ocurre en Y función, el último deploy fue a las Z) de lo que se asume (probablemente es el deploy, probablemente es la base de datos) clarifica enormemente el problema.</p>

<h2>El entrenamiento del control en condiciones normales</h2>

<p>El control del pánico no se aprende durante el incidente. Se entrena en condiciones normales para que esté disponible cuando se necesita.</p>

<p>La práctica concreta: cuando encuentres un bug en tu código de práctica, aplicar el protocolo completo aunque no sea necesario. Pausar. Respirar. Definir. Observar. Hipótesis. Un cambio.</p>

<p>Hacerlo 100 veces en condiciones de bajo estrés lo convierte en hábito. El hábito es lo único que sobrevive al estrés extremo.</p>
`,
}

const POST_NEUROPLASTICIDAD: Post = {
  slug:          'neuroplasticidad-dolor-aprender-codigo',
  title:         'Neuroplasticidad: El Dolor de Aprender a Programar es Físico',
  description:   'La ciencia detrás de por qué aprender a programar literalmente agota. Esa sensación de "cerebro frito" es el proceso biológico de crear nuevas conexiones neuronales. El dolor como métrica de avance.',
  publishedAt:   '2026-03-18',
  readTime:      '8 min',
  category:      'metodologia',
  categoryLabel: 'Metodología',
  content: `
<p>Después de 3 horas intentando entender la recursión por primera vez, hay una sensación muy específica: el cerebro duele. No metafóricamente. Hay fatiga cognitiva real, dificultad para concentrarse, una especie de presión detrás de los ojos.</p>

<p>La mayoría de las personas interpreta esa sensación como señal de que llegó al límite de su capacidad. "No estoy hecho para esto." "Mi cerebro no lo entiende."</p>

<p>La interpretación correcta es la opuesta: esa sensación es la evidencia biológica de que el aprendizaje está ocurriendo.</p>

<h2>Qué es la neuroplasticidad y por qué importa</h2>

<p>El cerebro adulto no es una estructura fija. Cada vez que aprendemos algo nuevo, se forman nuevas conexiones sinápticas entre neuronas. Las conexiones existentes se refuerzan o debilitan según el uso. Nuevas neuronas pueden generarse en regiones específicas como el hipocampo.</p>

<p>Este proceso — la neuroplasticidad — tiene un costo energético real. El cerebro consume aproximadamente 20% del gasto calórico total del cuerpo en reposo. Durante el aprendizaje intensivo, ese consumo aumenta. La glucosa se agota. Las neuronas producen metabolitos de desecho que generan sensación de fatiga.</p>

<p>El "cerebro frito" que sentís después de 3 horas de programación difícil no es una limitación. Es el proceso biológico de construcción de nueva arquitectura neural.</p>

<blockquote>
<p>La sensación de fatiga cognitiva intensa durante el aprendizaje de programación no indica que llegaste al límite. Indica que el proceso está funcionando. El dolor es la obra en construcción.</p>
</blockquote>

<h2>El error de parar cuando duele</h2>

<p>La respuesta intuitiva a la fatiga cognitiva es parar. Tiene sentido: el cuerpo señala incomodidad, el cerebro procesa esa señal como "detente". En el contexto físico, parar cuando duele previene lesiones.</p>

<p>En el contexto del aprendizaje cognitivo, la relación es más compleja. Hay dos tipos de fatiga que se sienten similares pero tienen consecuencias opuestas:</p>

<ul>
<li><strong>Fatiga productiva:</strong> Generada por el procesamiento activo de información nueva, la construcción de conexiones neurales, el esfuerzo de comprensión genuino. Es la señal de que el aprendizaje está ocurriendo.</li>
<li><strong>Fatiga contraproducente:</strong> Generada por intentar procesar más información de la que el sistema puede manejar en ese estado. Continuar en este estado reduce la retención y puede crear confusión adicional.</li>
</ul>

<p>La diferencia práctica: la fatiga productiva ocurre durante el trabajo en el borde del límite de comprensión. La fatiga contraproducente ocurre cuando seguís empujando después de que la comprensión se desconecta completamente.</p>

<h2>Las ventanas de máxima neuroplasticidad</h2>

<p>Los estudios de neurociencia del aprendizaje han identificado ventanas temporales óptimas para la formación sináptica. El estado de mayor neuroplasticidad no ocurre durante el estudio intensivo — ocurre durante el descanso inmediatamente posterior.</p>

<p>Una sesión de aprendizaje intensivo de 90-120 minutos seguida de un descanso de 15-20 minutos (sin pantallas, sin input activo) genera más retención a largo plazo que 3-4 horas continuas de estudio.</p>

<p>El cerebro no consolida la información mientras la procesa. La consolida cuando deja de procesarla activamente.</p>

<h2>Medir el avance con el dolor correcto</h2>

<p>En el entrenamiento físico, hay una distinción clásica entre el dolor muscular de la adaptación (DOMS — delayed onset muscle soreness) y el dolor agudo de una lesión. El primero es una señal de progreso. El segundo es una señal de daño.</p>

<p>En el aprendizaje de programación, la distinción análoga es:</p>

<ul>
<li><strong>Señal de progreso:</strong> Fatiga cognitiva después de trabajar en un problema que genuinamente no entendías. Sensación de "no termino de cerrar" — la mente sigue trabajando en el problema después de que paraste de estudiar.</li>
<li><strong>Señal de problema:</strong> Confusión sin anclaje — no sabés qué no entendés. Sensación de que cuanto más leés, menos entendés. Incapacidad de formular una pregunta específica sobre el problema.</li>
</ul>

<p>La primera señal es incómoda pero productiva. La segunda indica que el nivel de dificultad excede la capacidad actual de comprensión — necesitás material más básico antes de continuar.</p>

<h2>El rol del sueño en la neuroplasticidad del programador</h2>

<p>Durante el sueño, especialmente en las fases de sueño profundo y REM, el cerebro realiza la consolidación activa de lo aprendido durante el día. Las conexiones sinápticas se estabilizan. La información se transfiere de la memoria de trabajo a la memoria a largo plazo.</p>

<p>La evidencia es consistente: aprender algo difícil la noche antes de dormir genera mayor retención a largo plazo que aprender lo mismo a primera hora de la mañana. El sueño posterior actúa como catalizador de la consolidación.</p>

<p>Lo que esto implica para el Operador: las sesiones de aprendizaje de material nuevo son más valiosas cuando están seguidas de una noche completa de sueño. No aprender, dormir, repasar — aprender, dormir, avanzar.</p>

<h2>La conclusión que cambia la perspectiva</h2>

<p>El dolor cognitivo de aprender a programar no es un obstáculo. Es el mecanismo. La incomodidad de no entender, la fatiga de trabajar en el límite, la frustración de los errores — todo eso es el proceso biológico de reconstruir la arquitectura de tu cerebro.</p>

<p>Los programadores que llegan lejos no son los que encontraron el camino sin dolor. Son los que aprendieron a interpretar el dolor correctamente y a trabajar con él en lugar de contra él.</p>
`,
}

const POST_TRAMPA_DOPAMINA: Post = {
  slug:          'trampa-dopamina-barata-cursos-vs-realidad',
  title:         'La Trampa de la Dopamina Barata: Por Qué Los Cursos de Video Te Dejan Vacío',
  description:   'Por qué las plataformas de video te hacen sentir inteligente pero te dejan vacío. El contraste entre la dopamina de completar un módulo y la dopamina real de compilar tu primera herramienta autónoma.',
  publishedAt:   '2026-03-11',
  readTime:      '7 min',
  category:      'metodologia',
  categoryLabel: 'Metodología',
  content: `
<p>Hay una sensación muy específica después de completar un módulo en una plataforma de cursos online. El círculo de progreso llega al 100%. Aparece una animación. "¡Módulo completado!" Un badge. El porcentaje de completado del curso sube de 24% a 31%.</p>

<p>Esa sensación es real. Es dopamina. El problema es de dónde viene y qué compra.</p>

<h2>El sistema de recompensa y el aprendizaje</h2>

<p>El sistema dopaminérgico del cerebro recompensa la consecución de objetivos. Evolutivamente, este sistema evolucionó para motivar comportamientos que aumentan la supervivencia — encontrar comida, agua, refugio, conexión social. Cuando lograr un objetivo, el cerebro libera dopamina. La sensación es de satisfacción y competencia.</p>

<p>El problema es que el cerebro no distingue de forma innata entre objetivos valiosos y objetivos diseñados para triggear la recompensa sin el trabajo que normalmente la justifica.</p>

<p>Las plataformas de video están diseñadas, con precisión industrial, para maximizar la liberación de dopamina. Progreso visible, badges, streaks, porcentajes, certificados. Todo el aparato visual del logro, disociado del logro real.</p>

<blockquote>
<p>Sentirse inteligente y serlo son dos experiencias completamente distintas. Las plataformas de video optimizan para la primera porque eso es lo que retiene usuarios. El mercado laboral mide la segunda.</p>
</blockquote>

<h2>La ilusión del progreso medible</h2>

<p>El porcentaje de completado de un curso es una métrica de consumo, no de aprendizaje. Mide cuántos videos miraste, no qué podés hacer después de mirarlos.</p>

<p>Existe una brecha sistemática entre estos dos números que las plataformas de cursos no tienen incentivo en reducir. Un usuario que llega al 100% y se siente preparado para el mercado laboral (aunque no lo esté) es más probable que deje una reseña positiva y recomiende el curso que un usuario que sabe con precisión qué brechas de conocimiento todavía tiene.</p>

<p>La retroalimentación honesta sobre el estado de tu aprendizaje es incómoda. Las plataformas de video no la dan porque no las beneficia.</p>

<h2>La diferencia entre el "completar módulo" y el "ejecutar código real"</h2>

<p>Hay dos momentos específicos de liberación de dopamina en el aprendizaje de programación. El primero es artificial. El segundo es genuino.</p>

<p>El primero: ver el check verde en el ejercicio guiado de una plataforma, donde el sistema verifica que tu código hace exactamente lo que el tutorial dijo que hiciera.</p>

<p>El segundo: construir una herramienta desde cero — un script que automatiza algo real, una API que responde a una request tuya, un parser que procesa datos reales — y ver que funciona.</p>

<pre><code># La dopamina del tutorial:
# El sistema espera exactamente este código:
def saludar(nombre):
    return f"Hola, {nombre}"
# ✓ ¡Correcto! +10 XP

# La dopamina real:
# Construiste algo que no existía antes
import requests
from datetime import datetime

def precio_dolar_blue() -> dict:
    respuesta = requests.get("https://dolarito.ar/api/dolar/blue")
    data = respuesta.json()
    return {
        "compra": data["compra"],
        "venta": data["venta"],
        "timestamp": datetime.now().isoformat()
    }

# Tu script acaba de obtener información real del mundo real.
# Nadie te dijo exactamente cómo hacerlo.
# Lo construiste vos.</code></pre>

<p>La diferencia neurológica entre estos dos momentos es sustancial. El primero es una recompensa predecible por seguir instrucciones. El segundo es una recompensa por resolver un problema con las herramientas que construiste.</p>

<h2>El diseño deliberado del engagement</h2>

<p>No es accidental que las plataformas de cursos estén estructuradas como juegos. Streaks diarios, leaderboards, niveles, badges — el lenguaje es exactamente el de los videojuegos diseñados para maximizar el tiempo en pantalla.</p>

<p>La gamificación del aprendizaje no es inherentemente mala. La gamificación que optimiza el engagement sobre el aprendizaje genuino sí lo es. Y la mayoría de las plataformas de video están en el segundo campo porque el modelo de negocio lo requiere: más tiempo en la plataforma, más probabilidad de renovar la suscripción.</p>

<h2>Qué hace la dopamina genuina del aprendizaje</h2>

<p>Cuando un programador resuelve un problema real por primera vez — un problema para el que nadie le dio la respuesta exacta — la recompensa dopaminérgica es cualitativamente diferente. El cerebro registra un logro genuino, no un logro señalado por el sistema.</p>

<p>Esta distinción importa porque los logros genuinos construyen algo que los artificiales no pueden: la creencia de que podés resolver problemas desconocidos. Esa creencia — la autoeficacia cognitiva — es exactamente lo que necesitás para funcionar en un trabajo real, donde los problemas no vienen con instrucciones adjuntas.</p>

<h2>El antídoto práctico</h2>

<p>La solución no es evitar todo material estructurado. Es cambiar la métrica de éxito: de "¿cuántos videos completé?" a "¿qué puedo construir ahora que no podía construir antes?"</p>

<p>Por cada concepto que aprendés en un video, existe el momento de aplicación genuina: construir algo que uses ese concepto en un contexto que el tutorial no diseñó. Sin las instrucciones exactas. Sin la garantía de que funciona. Con la posibilidad real del error.</p>

<p>Ese momento — cuando el código que escribiste vos, sin guía, hace algo real — es la dopamina que se convierte en habilidad.</p>
`,
}

const POST_COMBATE_REAL: Post = {
  slug:          'combate-real-teoria-vs-produccion',
  title:         'El Combate Real: La Distancia Abismal Entre el Tutorial y la Producción',
  description:   'La diferencia entre la teoría en un entorno controlado y el impacto de desplegar código real. Por qué el verdadero aprendizaje empieza cuando tu código choca con las imprevisibilidades del mundo real.',
  publishedAt:   '2026-03-04',
  readTime:      '8 min',
  category:      'python',
  categoryLabel: 'Python',
  content: `
<p>En las artes marciales existe una separación fundamental entre el <em>kata</em> — las formas practicadas en el dojo con movimientos predecibles — y el combate real. Los karatekas pueden ejecutar el kata con perfección técnica absoluta durante años y aun así perder su primer enfrentamiento real porque el adversario no coopera con las secuencias ensayadas.</p>

<p>El código en producción es el adversario que no coopera.</p>

<h2>El entorno controlado del tutorial</h2>

<p>Los tutoriales, los cursos y los ejercicios de práctica tienen una característica en común que rara vez se explicita: están diseñados para funcionar. El autor preparó los datos de entrada, validó los casos borde, aseguró que el entorno es el correcto. El código del tutorial funciona porque el autor se aseguró de que funcione.</p>

<p>Esto es valioso para aprender conceptos. Es completamente diferente de lo que pasa en producción.</p>

<pre><code># El tutorial:
usuarios = ["Ana", "Luis", "Pedro"]
for usuario in usuarios:
    print(f"Bienvenido, {usuario}")
# Funciona. Siempre. Los datos son perfectos.

# La realidad:
usuarios = obtener_usuarios_de_base_de_datos()
# ¿Qué hay en esa lista?
# None si la query falló
# [] si no hay usuarios
# ["Ana", None, "Pedro"] si hay nulls
# ["Ana", 42, "Pedro"] si el tipo es incorrecto
# Una lista con 40,000 elementos si no hay paginación
# Una excepción si la base de datos no responde</code></pre>

<p>La diferencia no es una curiosidad técnica. Es la diferencia entre código que funciona en el tutorial y código que funciona en producción.</p>

<h2>Las imprevisibilidades del mundo real</h2>

<p>El mundo real inyecta variables que ningún tutorial considera porque hacerlo lo complicaría innecesariamente para el propósito de enseñar el concepto.</p>

<ul>
<li><strong>Concurrencia:</strong> En producción, tu código corre simultáneamente con otras instancias. La variable que leíste puede haber sido modificada por otro proceso en el nanosegundo entre que la leíste y la usaste.</li>
<li><strong>Estado de la red:</strong> Las APIs externas fallan. Tienen timeouts. Devuelven respuestas malformadas. El tutorial asume que el servidor siempre responde correctamente.</li>
<li><strong>Datos del mundo real:</strong> Los usuarios ingresan datos que no esperabas. Strings vacíos, caracteres especiales, valores negativos donde debería haber positivos, emails con formatos válidos pero inusuales.</li>
<li><strong>Escala:</strong> El algoritmo que procesa 100 registros en 0.1 segundos procesa 100,000 registros en 45 minutos. La escala cambia todo.</li>
</ul>

<h2>El primer deploy: el momento de la verdad</h2>

<p>Hay un momento específico en la vida de todo programador que lo transforma: el primer deploy real. Código tuyo, corriendo en un servidor, sirviendo requests de usuarios que no son vos.</p>

<p>Lo que ocurre en ese momento enseña más que meses de tutoriales porque el feedback es real, inmediato e inevitable. Si hay un bug, aparece. Si hay un problema de performance, aparece. Si hay un caso borde no manejado, aparece.</p>

<pre><code># El código que escribiste:
@app.post("/usuario")
def crear_usuario(email: str, nombre: str):
    usuario = Usuario(email=email, nombre=nombre)
    db.session.add(usuario)
    db.session.commit()
    return {"id": usuario.id}

# Lo que ocurre en producción la primera semana:
# - Dos requests simultáneas con el mismo email → IntegrityError
# - Email con 500 caracteres → columna VARCHAR(255) overflow
# - Request con nombre = None → NullConstraintError
# - Timeout de base de datos en horario pico → 500 sin mensaje útil
# - Bot haciendo 10,000 requests/segundo → tu servidor cae</code></pre>

<p>Ninguno de estos problemas aparece en el tutorial. Todos aparecen en producción.</p>

<h2>Por qué la producción enseña lo que el tutorial no puede</h2>

<p>La razón no es que el tutorial sea malo. Es que el tutorial, por definición, no puede replicar la complejidad emergente de un sistema real con usuarios reales.</p>

<p>La complejidad emergente no es la suma de los componentes — es lo que aparece en la interacción entre ellos. Tu código, el código de la librería que usás, el sistema operativo, la red, la base de datos, el comportamiento del usuario: todos interactúan de formas que ningún tutorial puede anticipar porque son infinitas.</p>

<p>El aprendizaje que ocurre cuando tu código choca contra esa complejidad es cualitativamente diferente al que ocurre en el tutorial. No porque el problema sea más difícil — sino porque es real.</p>

<h2>Cómo acelerar la exposición al combate real</h2>

<p>No hay que esperar al primer trabajo para tener exposición a producción. Hay formas de replicar la exposición antes:</p>

<ul>
<li><strong>Proyectos personales desplegados:</strong> Un bot de Telegram, una API que usás vos mismo, un script que procesa datos reales. El deploy en Render o Railway es gratuito y fuerza la exposición a errores de producción.</li>
<li><strong>Datos reales desde el día 1:</strong> En lugar de datos de prueba perfectos, usar datasets públicos reales — llenos de valores nulos, inconsistencias y tipos incorrectos.</li>
<li><strong>Simular adversarios:</strong> Intentar romper tu propio código. Pasar valores negativos, strings vacíos, nulls, emails malformados, listas de un millón de elementos. Si podés romperlo vos, alguien más lo va a romper en producción.</li>
</ul>

<h2>El programador que sobrevive en producción</h2>

<p>El programador que funciona bien en producción no es el que nunca cometió errores. Es el que aprendió a anticipar los modos de falla, a escribir código defensivo sin volverlo ilegible, y a recuperarse rápido cuando algo falla inevitablemente.</p>

<p>Esas habilidades no se aprenden en el tutorial. Se aprenden en el combate real. Cuanto antes empieces a exponerte a él, más rápido las desarrollás.</p>
`,
}

const POST_REPOSO_OPERADOR: Post = {
  slug:          'reposo-del-operador-asimilacion-inconsciente',
  title:         'El Reposo del Operador: Por Qué La Solución Aparece en la Ducha',
  description:   'La ciencia del descanso en el aprendizaje. Por qué la solución a un algoritmo imposible aparece mientras te duchás o dormís. Cómo el cerebro compila y optimiza en la fase de recuperación.',
  publishedAt:   '2026-02-25',
  readTime:      '7 min',
  category:      'metodologia',
  categoryLabel: 'Metodología',
  content: `
<p>Arquímedes en la bañera. Newton bajo el manzano. Kekulé soñando con una serpiente mordiéndose la cola y entendiendo la estructura del benceno. La historia de la ciencia está llena de insights que llegaron durante el descanso, no durante el trabajo concentrado.</p>

<p>No es coincidencia. Es neurobiología.</p>

<h2>El modo default del cerebro</h2>

<p>Durante décadas, los neurocientíficos ignoraron la actividad cerebral en estado de reposo, asumiendo que el cerebro simplemente "estaba en pausa" cuando no procesaba información activamente. Hasta que los escáneres de resonancia magnética funcional revelaron algo inesperado: cuando el cerebro no está concentrado en una tarea externa, activa una red de regiones diferente pero igualmente activa.</p>

<p>Esta red — la <em>Default Mode Network</em> (DMN) — se activa durante la ensoñación, el descanso, las duchas, las caminatas. Y lejos de ser pasiva, está realizando un trabajo cognitivo complejo: consolidar memorias, encontrar conexiones entre ideas aparentemente no relacionadas, procesar problemas sin la guía del pensamiento consciente.</p>

<blockquote>
<p>El cerebro no para de trabajar cuando dejás de estudiar. Cambia de modo. El modo de descanso realiza funciones cognitivas que el modo de concentración activa no puede hacer simultáneamente.</p>
</blockquote>

<h2>Por qué la ducha funciona</h2>

<p>La ducha tiene varias características que facilitan la activación de la DMN:</p>

<ul>
<li>Ausencia de pantallas y notificaciones (el mayor inhibidor de la DMN)</li>
<li>Actividad motora repetitiva y automática (libera la atención del control consciente)</li>
<li>Ambiente sensorial predecible y confortable (reduce la carga de procesamiento externo)</li>
<li>Transición clara del trabajo activo (señal al cerebro de que puede cambiar de modo)</li>
</ul>

<p>En ese estado, el cerebro puede procesar el problema en el que estuviste trabajando sin la rigidez del pensamiento dirigido. La DMN explora conexiones que la atención focalizada descarta como irrelevantes.</p>

<h2>La consolidación durante el sueño</h2>

<p>El sueño es el período de mayor actividad de consolidación de la memoria. Durante las fases de sueño NREM profundo, el hipocampo "reproduce" las experiencias del día y las transfiere a la memoria a largo plazo en la neocorteza. Durante el sueño REM, el cerebro integra nueva información con conocimiento existente y genera conexiones novedosas.</p>

<p>Los estudios de aprendizaje de programación muestran un patrón consistente: los sujetos que aprenden un concepto nuevo y duermen antes de ser evaluados obtienen resultados significativamente mejores que los que aprenden y son evaluados inmediatamente, incluso cuando el tiempo de estudio es el mismo.</p>

<p>El sueño no es tiempo perdido de estudio. Es parte del proceso de aprendizaje.</p>

<h2>El problema del estudio sin descanso</h2>

<p>Hay una tendencia entre quienes aprenden a programar de culpabilizarse por el descanso. "Podría estar estudiando en lugar de descansar." "Veo la solución mañana después de estudiar 2 horas más."</p>

<p>El problema es que el cerebro sobrecargado no consolida eficientemente. Después de 5-6 horas de estudio cognitivo intenso, la capacidad de formación de nuevas memorias cae de forma medible. Seguir estudiando en ese estado tiene rendimientos decrecientes cercanos a cero.</p>

<pre><code># El modelo erróneo del aprendizaje:
horas_de_estudio = 10  # Más horas = más aprendizaje
# Resultado: fatiga, frustración, baja retención

# El modelo correcto:
sesion_intensiva = 90   # minutos de estudio concentrado
descanso = 20           # minutos sin pantallas
sleep = 8               # horas de sueño
# Resultado: consolidación real, más retención, menos tiempo total</code></pre>

<h2>Cómo aprovechar el modo de descanso deliberadamente</h2>

<p>La DMN puede activarse de forma deliberada mediante prácticas específicas:</p>

<ul>
<li><strong>Caminatas sin teléfono.</strong> 20-30 minutos de caminata sin input externo activa la DMN y permite que el cerebro procese el problema en background.</li>
<li><strong>Técnica del "problema flotante".</strong> Antes de dormir, repasar mentalmente el problema en el que estuviste trabajando sin intentar resolverlo. El cerebro lo procesa durante el sueño.</li>
<li><strong>Pomodoro con descansos reales.</strong> Los 5 minutos de descanso del Pomodoro deben ser descanso verdadero — sin teléfono, sin pantalla. La corteza visual activa en el descanso inhibe la DMN.</li>
</ul>

<h2>Cuándo la solución llega sola</h2>

<p>La experiencia que describen los programadores senior de forma casi universal: el problema que parecía irresoluble al final del día aparece resuelto en la mente a la mañana siguiente, antes de abrir el IDE.</p>

<p>Esto no es magia ni genialidad. Es el cerebro haciendo su trabajo de noche, procesando el problema con recursos que el pensamiento concentrado no puede usar. El Operador que entiende este proceso no lucha contra él — lo aprovecha.</p>

<p>La disciplina del descanso no es menor que la disciplina del estudio. Es parte de ella.</p>
`,
}

const POST_MITO_CINTURON: Post = {
  slug:          'mito-cinturon-negro-python',
  title:         'El Mito del Cinturón Negro en Python: Los Expertos No Hacen Magia',
  description:   'Los Senior Devs y Arquitectos no hacen magia. El dominio avanzado no es conocer funciones secretas — es la ejecución impecable, automática y despiadada de los fundamentos bajo presión extrema.',
  publishedAt:   '2026-02-18',
  readTime:      '8 min',
  category:      'python',
  categoryLabel: 'Python',
  content: `
<p>Hay una fantasía común entre quienes aprenden a programar sobre cómo es la vida de un developer senior. Abre el IDE, escribe código críptico y sofisticado que ningún mortal puede leer, pulsa enter, y el sistema complejo que acaba de construir funciona a la primera.</p>

<p>Esta fantasía tiene el mismo fundamento de realidad que la del maestro de karate que noquea a diez personas de un solo golpe.</p>

<h2>Lo que el senior realmente hace</h2>

<p>Un developer senior experimentado, en un día normal de trabajo, pasa la mayoría del tiempo haciendo exactamente lo mismo que haría un developer junior: leer código, escribir funciones, manejar errores, debuggear problemas. La diferencia no está en las actividades — está en la velocidad, la precisión y la capacidad de hacerlo bajo presión.</p>

<p>El senior no conoce funciones secretas de Python que el junior no conoce. Conoce las mismas funciones que están en la documentación pública. Lo que hace diferente al senior es que las ejecuta sin pensar en ellas.</p>

<pre><code># Junior escribiendo esto:
# "¿Cómo era la sintaxis del defaultdict?
#  Déjame buscar... ah sí, from collections import defaultdict..."
from collections import defaultdict
frecuencias = defaultdict(int)
for palabra in texto.split():
    frecuencias[palabra] += 1

# Senior escribiendo esto:
# (los dedos ya escribieron esto 500 veces — sin pensarlo)
from collections import defaultdict
frecuencias = defaultdict(int)
for palabra in texto.split():
    frecuencias[palabra] += 1</code></pre>

<p>El código es idéntico. El proceso cognitivo es completamente diferente. El senior está pensando en el problema — el procesamiento de texto, la distribución de frecuencias, los casos borde. El junior está pensando en la sintaxis.</p>

<blockquote>
<p>El dominio avanzado en programación no es acceso a conocimiento secreto. Es la automatización de los fundamentos al punto donde requieren cero atención consciente, liberando toda la capacidad cognitiva para el problema real.</p>
</blockquote>

<h2>Los fundamentos que el cinturón negro ejecuta automáticamente</h2>

<p>Hay un conjunto de patrones en Python que un developer con 5+ años de experiencia ejecuta sin pensar. No porque sean complicados — son exactamente los mismos que el developer aprendió en sus primeros meses. La diferencia es la cantidad de veces que los ejecutó.</p>

<pre><code># 1. Manejo de contexto con recursos
with open(archivo, 'r', encoding='utf-8') as f:
    datos = json.load(f)

# 2. Comprensiones anidadas con condición
resultado = [
    procesar(item)
    for item in coleccion
    if es_valido(item)
]

# 3. Desempaquetado y asignación múltiple
primer, *resto = lista
clave, valor = tupla
x, y, z = coordenadas

# 4. Manejo de errores específico con contexto
try:
    conexion = crear_conexion(config)
except ConnectionRefusedError:
    logger.warning("Servidor no disponible, intentando backup")
    conexion = crear_conexion(config_backup)
except TimeoutError as e:
    raise ServiceUnavailableError(f"Timeout: {e}") from e

# 5. Generadores para datos grandes
def leer_csv_por_chunks(archivo, chunk_size=1000):
    with open(archivo) as f:
        chunk = []
        for linea in f:
            chunk.append(linea.strip().split(','))
            if len(chunk) == chunk_size:
                yield chunk
                chunk = []
        if chunk:
            yield chunk</code></pre>

<p>Ninguno de estos patrones es sofisticado. Todos están en la documentación de Python. La diferencia es que el senior los ejecuta en 30 segundos sin pensar, y el junior tarda 5 minutos y busca ejemplos.</p>

<h2>El cinturón negro bajo presión</h2>

<p>La prueba real del dominio no es el rendimiento en condiciones normales — es el rendimiento bajo presión extrema. En las artes marciales, el cinturón negro es el practicante que puede ejecutar técnicas precisas cuando está agotado, golpeado y estresado.</p>

<p>En programación, la presión equivalente es el incident a las 2 AM, el bug en producción con usuarios activos, el deadline que no se mueve, el código de otro que nadie entiende y que hay que modificar hoy.</p>

<p>Bajo esa presión, los conocimientos que no están automatizados desaparecen. La memoria de trabajo está ocupada procesando el estrés. Solo queda lo que está grabado en la memoria procedimental — los patrones que el cuerpo ejecuta sin que el cerebro tenga que pedírselo.</p>

<h2>El camino al cinturón negro en Python no tiene atajos</h2>

<p>La fantasía del atajo — el tutorial mágico, el libro secreto, el framework que lo hace todo fácil — existe porque la realidad es incómoda: la automatización de los fundamentos requiere tiempo y repetición. No hay reemplazo.</p>

<p>Los estudios sobre adquisición de habilidades expertas (Ericsson, Gladwell, Duckworth) coinciden en un punto: el nivel de maestría está correlacionado con la cantidad de práctica deliberada acumulada, no con el talento innato ni con el acceso a información específica.</p>

<p>Un developer con 10,000 horas de escritura de código real tiene patrones automatizados que no tienen precio. No porque tenga acceso a conocimiento secreto — porque ejecutó los fundamentos suficientes veces como para que dejen de requerir atención consciente.</p>

<h2>Lo que debería cambiar en tu perspectiva</h2>

<p>Cuando un developer senior resuelve un problema rápidamente, la tendencia es atribuirlo al genio o a la experiencia misteriosa. La realidad es más banal y más útil: ejecutó un patrón que ya automatizó. Probablemente el mismo patrón que vos también conocés, pero que todavía tenés que pensar para ejecutar.</p>

<p>La brecha entre vos y el senior no es de inteligencia ni de conocimiento. Es de repetición. Eso significa que es una brecha que podés cerrar. Requiere tiempo, práctica deliberada y la voluntad de ejecutar los fundamentos una y otra vez hasta que dejen de requerir atención.</p>

<p>Así es como se construye el cinturón negro en Python. Un patrón a la vez, automatizado hasta que sea reflejo.</p>
`,
}

// ─── Registro y helpers ───────────────────────────────────────────────────────

export const posts: Post[] = [
  POST_APRENDER_PYTHON,
  POST_PYTHON_TRABAJO,
  POST_CODE_REVIEW,
  POST_SOBRECARGA_PROGRESIVA,
  POST_MEMORIA_MUSCULAR,
  POST_ACONDICIONAMIENTO_PESADO,
  POST_TENSION_ISOMETRICA,
  POST_CONTROL_PANICO,
  POST_NEUROPLASTICIDAD,
  POST_TRAMPA_DOPAMINA,
  POST_COMBATE_REAL,
  POST_REPOSO_OPERADOR,
  POST_MITO_CINTURON,
]

/** Lista ordenada por fecha desc (sin campo content para las listas) */
export function getAllPosts(): Omit<Post, 'content'>[] {
  return posts
    .map(({ content: _, ...meta }) => meta)
    .sort((a, b) => b.publishedAt.localeCompare(a.publishedAt))
}

export function getPostBySlug(slug: string): Post | undefined {
  return posts.find(p => p.slug === slug)
}

export function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString('es-AR', {
    year: 'numeric', month: 'long', day: 'numeric',
  })
}
