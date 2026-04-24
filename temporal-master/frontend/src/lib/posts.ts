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

// ─── Registro y helpers ───────────────────────────────────────────────────────

export const posts: Post[] = [
  POST_APRENDER_PYTHON,
  POST_PYTHON_TRABAJO,
  POST_CODE_REVIEW,
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
