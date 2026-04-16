import Link from 'next/link'

export const metadata = {
  title: 'Términos y Condiciones — DAKI EdTech',
  description: 'Términos y Condiciones del Sistema de Entrenamiento Táctico DAKI EdTech — Naturaleza del servicio, política de reembolso condicionada y propiedad intelectual.',
}

export default function TerminosPage() {
  return (
    <div className="min-h-screen bg-[#0A0A0A] text-[#00FF41]/80 font-mono px-6 md:px-16 lg:px-32 py-16 relative overflow-hidden">

      {/* CRT scanlines */}
      <div className="fixed inset-0 pointer-events-none z-0"
        style={{ backgroundImage: 'repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,0,0,0.06) 2px,rgba(0,0,0,0.06) 4px)' }} />

      <div className="relative z-10 max-w-3xl mx-auto">

        {/* Nav */}
        <div className="flex items-center gap-4 mb-12 text-xs text-[#00FF41]/30 tracking-[0.3em]">
          <Link href="/" className="hover:text-[#00FF41]/70 transition-colors">← VOLVER AL NEXO</Link>
          <span>/</span>
          <span>SECTOR LEGAL // TÉRMINOS Y CONDICIONES</span>
        </div>

        {/* Header */}
        <div className="border-b border-[#00FF41]/15 pb-8 mb-10">
          <div className="text-xs text-[#00FF41]/30 tracking-[0.4em] uppercase mb-3">
            Documento Legal // Protocolo v2.0
          </div>
          <h1 className="text-2xl text-[#00FF41] tracking-wide mb-4">
            Términos y Condiciones de Uso
          </h1>
          <p className="text-sm text-[#00FF41]/50 leading-6">
            Sistema de Entrenamiento Táctico DAKI EdTech — Propiedad de{' '}
            <span className="text-[#00FF41]/70">Adrian Eduardo Ardiles Peralta</span>
            <br />
            Última actualización: 22 de marzo de 2026
          </p>
        </div>

        <LegalDoc />

        {/* Footer */}
        <div className="mt-16 pt-8 border-t border-[#00FF41]/10 text-xs text-[#00FF41]/25 leading-6">
          <p>DAKI EdTech © 2026 · Todos los derechos reservados.</p>
          <p className="mt-1">
            <Link href="/privacidad" className="hover:text-[#00FF41]/50 underline transition-colors">
              Política de Privacidad
            </Link>
            {' · '}
            <Link href="/" className="hover:text-[#00FF41]/50 transition-colors">
              Volver al inicio
            </Link>
          </p>
        </div>

      </div>
    </div>
  )
}

// ── Contenido del documento ───────────────────────────────────────────────────

function LegalDoc() {
  return (
    <div className="space-y-10 text-sm leading-7">

      <Section title="0. Aviso Importante — Leer antes de continuar">
        <p>
          Al registrarte en DAKI EdTech, completar el proceso de pago o pulsar el botón{' '}
          <strong className="text-[#00FF41]/90">[ INGRESAR AL NEXO ]</strong>, manifiestas
          que has leído, comprendido y aceptado en su totalidad los presentes Términos y
          Condiciones, así como nuestra{' '}
          <Link href="/privacidad" className="text-[#00FF41]/80 underline hover:text-[#00FF41]">
            Política de Privacidad
          </Link>.
        </p>
        <p className="text-[#00FF41]/50 mt-2">
          Si no aceptas alguna de estas condiciones, no utilices la plataforma.
        </p>
      </Section>

      <Section title="1. Identificación del Titular">
        <ul className="space-y-1 text-[#00FF41]/60">
          <li><span className="text-[#00FF41]/80">Nombre:</span> Adrian Eduardo Ardiles Peralta</li>
          <li><span className="text-[#00FF41]/80">Marca comercial:</span> DAKI EdTech</li>
          <li><span className="text-[#00FF41]/80">Soporte técnico:</span> systemsupport@dakiedtech.com</li>
          <li><span className="text-[#00FF41]/80">Legal / reembolsos:</span> legal@dakiedtech.com</li>
          <li><span className="text-[#00FF41]/80">País de constitución:</span> Argentina</li>
        </ul>
      </Section>

      <Section title="2. Naturaleza del Servicio y El Ecosistema DAKI">
        <p>
          DAKI EdTech no es un servicio de clases de programación tradicional. Operamos
          como un{' '}
          <strong className="text-[#00FF41]/90">
            Sistema de Entrenamiento Táctico Asistido por Inteligencia Artificial
          </strong>
          . Al adquirir nuestros servicios, el usuario (en adelante,{' '}
          <em className="text-[#00FF41]/80">&quot;El Operador&quot;</em>) obtiene acceso a{' '}
          <strong className="text-[#00FF41]/90">DAKI</strong>, nuestra Entidad Neuronal de
          acompañamiento, y a los entornos de simulación interactiva.
        </p>
        <p className="mt-3">
          El valor del servicio radica en la orquestación del aprendizaje, el andamiaje
          táctico y la retroalimentación en tiempo real proporcionada por el{' '}
          <strong className="text-[#00FF41]/80">Motor Cognitivo DAKI</strong>,
          independientemente del lenguaje de programación subyacente.
        </p>
        <ul className="mt-4 space-y-1.5 text-[#00FF41]/60 list-none">
          <Li>195 incursiones estructuradas en 22 sectores temáticos de dificultad progresiva.</Li>
          <Li>DAKI — Instructora Neuronal Táctica con sistema de escalación cognitiva de 3 niveles.</Li>
          <Li>Sistema de rangos operacionales, XP, certificado de élite y tabla de clasificación.</Li>
          <Li>Acceso vía navegador web, sin instalación de software adicional.</Li>
        </ul>
      </Section>

      <Section title="2b. Certificación y Alcance Académico">
        <p>
          DAKI EdTech es una plataforma tecnológica orientada al{' '}
          <strong className="text-[#00FF41]/80">entrenamiento de alto rendimiento</strong> y
          el aprendizaje autodidacta a través de la gamificación. No constituimos un centro
          de formación académica reglada.
        </p>
        <Callout type="info">
          Los <strong>&quot;Rangos de Operador&quot;</strong> y certificados expedidos son
          reconocimientos internos de destreza lógica dentro de nuestro ecosistema y{' '}
          <strong>no poseen validez oficial</strong> respaldada por ministerios de educación
          o entidades gubernamentales.
        </Callout>
      </Section>

      <Section title="3. Propiedad Intelectual">
        <p>
          Todos los contenidos de DAKI EdTech son propiedad exclusiva del Titular o de
          sus licenciantes, y están protegidos por la legislación de propiedad intelectual
          aplicable. Esto incluye, de forma enunciativa y no limitativa:
        </p>
        <ul className="mt-3 space-y-1.5 text-[#00FF41]/60">
          <Li>El código fuente, la arquitectura y el diseño de la plataforma.</Li>
          <Li>El universo narrativo, los personajes, el lore y el nombre «DAKI EdTech».</Li>
          <Li>El motor de voz, la personalidad y el nombre «DAKI» (instructora de IA).</Li>
          <Li>Los desafíos de código, sus enunciados, soluciones y textos de teoría.</Li>
          <Li>Los assets gráficos, sonoros y tipográficos.</Li>
        </ul>
        <Callout type="warn">
          Todo el contenido narrativo, el lore, el diseño de las misiones y la{' '}
          <strong>&quot;Personalidad y Lógica de Respuesta de DAKI&quot;</strong> son propiedad
          intelectual exclusiva de DAKI EdTech. Queda{' '}
          <strong>estrictamente prohibida</strong> la extracción automatizada (scraping),
          copia, o reproducción del contenido de las simulaciones para su uso en plataformas
          externas. Asimismo quedan prohibidos: la redistribución o reventa del material, la
          ingeniería inversa del sistema de evaluación y la reproducción total o parcial sin
          autorización escrita del Titular. El incumplimiento podrá dar lugar a acciones legales.
        </Callout>
      </Section>

      <Section title="4. Licencia de Uso">
        <p>
          Al adquirir una Licencia de Operador, el Titular te concede una licencia{' '}
          <strong className="text-[#00FF41]/80">personal, intransferible, no exclusiva y revocable</strong>{' '}
          para acceder a la plataforma y consumir sus contenidos únicamente para tu uso
          personal y formativo.
        </p>
        <p className="mt-3 text-[#00FF41]/50">
          La licencia no autoriza: el acceso compartido de cuentas, la cesión de credenciales
          a terceros, ni el uso comercial del material.
        </p>
      </Section>

      <Section title="5. Política de Pagos y Reembolsos">
        <SubSection title="5.1 Precio y Acceso Freemium">
          <p>
            El acceso completo a DAKI EdTech requiere la adquisición única de una{' '}
            <strong className="text-[#00FF41]/80">Licencia de Fundador</strong> (pago
            único, sin suscripción recurrente). El precio vigente se muestra en la página
            de compra en el momento de la transacción.
          </p>
          <p className="mt-2 text-[#00FF41]/50">
            El{' '}
            <strong className="text-[#00FF41]/70">Sector de Evaluación (Niveles 00 al 10)</strong>{' '}
            es de acceso gratuito e irrestricto, sin necesidad de pago, para que el
            Operador valide la compatibilidad del Sistema DAKI antes de comprometerse.
          </p>
        </SubSection>

        <SubSection title='5.2 Garantía de Sincronización ("Política de Reembolso Condicionada")'>
          <p>
            Para las compras de la Licencia de Fundador, ofrecemos una garantía de
            devolución de{' '}
            <strong className="text-[#00FF41]/90">7 días corridos</strong> desde la
            fecha de compra, <strong>estrictamente condicionada</strong> al consumo de
            los recursos de la IA.
          </p>
          <Callout type="warn">
            <strong>Condición de Anulación del Reembolso:</strong> El reembolso solo
            será procesado si se solicita dentro de los primeros 7 días corridos
            posteriores a la compra,{' '}
            <strong>Y</strong> si los registros del sistema indican que el Operador{' '}
            <strong>NO ha superado el Nivel 20</strong> de la incursión.
            <br /><br />
            Si el Operador completa el Nivel 21 o superior, se considerará que el
            servicio y la capacidad de procesamiento de DAKI han sido{' '}
            <strong>consumidos de manera efectiva</strong>, inhabilitando cualquier
            reclamo de reembolso.
          </Callout>
          <p className="mt-3 text-[#00FF41]/50">
            Para solicitar el reembolso dentro de las condiciones establecidas, escribe a{' '}
            <span className="text-[#00FF41]/80">legal@dakiedtech.com</span> con el
            asunto «GARANTÍA DE SINCRONIZACIÓN» e indicando el email de tu cuenta.
          </p>
        </SubSection>

        <SubSection title="5.3 Procesamiento del Pago">
          <p className="text-[#00FF41]/50">
            Los pagos se gestionan a través de pasarelas de pago de terceros (Stripe, PayPal
            u otras). DAKI EdTech no almacena datos de tarjeta bancaria. Consulta los
            términos de la pasarela utilizada para información sobre seguridad del pago.
          </p>
        </SubSection>
      </Section>

      <Section title="6. Uso de Inteligencia Artificial — DAKI">
        <p>
          DAKI EdTech integra un sistema de IA generativa denominado{' '}
          <strong className="text-[#00FF41]/90">DAKI</strong> que actúa como instructora
          táctica de aprendizaje. Al usar la plataforma, aceptas las siguientes condiciones
          sobre el uso de IA:
        </p>
        <ul className="mt-3 space-y-1.5 text-[#00FF41]/60">
          <Li>DAKI es un sistema de IA, no una persona humana. Sus respuestas son generadas algorítmicamente.</Li>
          <Li>
            Los fragmentos de código que envíes para evaluación son procesados por el
            motor de ejecución de la plataforma y pueden almacenarse de forma anonimizada
            con fines de telemetría, detección de errores y mejora del sistema educativo.
          </Li>
          <Li>No se almacena ni comparte código con identificación personal sin tu consentimiento explícito.</Li>
          <Li>
            La síntesis de voz de DAKI utiliza la Web Speech API del navegador;
            el procesamiento ocurre localmente en tu dispositivo.
          </Li>
        </ul>
      </Section>

      <Section title="7. Naturaleza del Servicio — Descargo de Responsabilidad Educativa">
        <Callout type="info">
          DAKI EdTech es una herramienta de aprendizaje. No garantizamos, ni expresa ni
          implícitamente, ningún resultado específico derivado del uso de la plataforma,
          incluyendo (pero no limitándose a) la obtención de empleo, la aprobación de
          certificaciones oficiales de terceros o el desarrollo de habilidades a un nivel
          determinado. Los resultados dependen del esfuerzo, la dedicación y las
          circunstancias individuales de cada usuario.
        </Callout>
        <p className="mt-4 text-[#00FF41]/50">
          El Titular no asume responsabilidad por el uso que el usuario haga de los
          conocimientos de Python adquiridos a través de la plataforma, incluyendo su
          aplicación en entornos profesionales, proyectos propios o de terceros.
        </p>
      </Section>

      <Section title="8. Limitación de Responsabilidad">
        <p>
          En la máxima medida permitida por la legislación aplicable, DAKI EdTech y su
          Titular no serán responsables de:
        </p>
        <ul className="mt-3 space-y-1.5 text-[#00FF41]/60">
          <Li>Daños indirectos, incidentales o consecuentes derivados del uso o la imposibilidad de uso del servicio.</Li>
          <Li>Interrupciones del servicio por mantenimiento, fallos técnicos o causas de fuerza mayor.</Li>
          <Li>Pérdida de datos de progreso causada por fallos técnicos no imputables al Titular.</Li>
          <Li>
            El uso de los conocimientos técnicos adquiridos para actividades ilegales,
            no autorizadas o perjudiciales para terceros. El usuario asume plena
            responsabilidad de sus actos.
          </Li>
        </ul>
        <p className="mt-4 text-[#00FF41]/50">
          La responsabilidad máxima del Titular, en cualquier circunstancia, estará
          limitada al importe abonado por el usuario en la compra de su licencia.
        </p>
      </Section>

      <Section title="9. Disponibilidad del Servicio (Uptime)">
        <p>
          DAKI EdTech realiza esfuerzos razonables para mantener la disponibilidad continua
          del servicio. Sin embargo, dado que el Motor Cognitivo DAKI depende de
          infraestructuras de IA de terceros, pueden producirse interrupciones o latencias
          fuera del control directo del Titular.
        </p>
        <Callout type="info">
          En caso de latencias o caídas de los servidores centrales de IA, el sistema
          entrará en{' '}
          <strong>modo de contingencia (&quot;Respuestas Offline&quot;)</strong> para preservar
          la inmersión del Operador hasta que se restablezca la conexión total. Las
          interrupciones planificadas se anunciarán con antelación cuando sea posible.
        </Callout>
        <p className="mt-3 text-[#00FF41]/50">
          El Titular no asume responsabilidad por interrupciones causadas por fallos
          en servicios de terceros (proveedores cloud, API de IA, pasarelas de pago),
          cortes de energía, eventos de fuerza mayor o ataques externos.
        </p>
      </Section>

      <Section title="10. Conducta del Operador">
        <p>
          El usuario se compromete a no utilizar la plataforma para:
        </p>
        <ul className="mt-3 space-y-1.5 text-[#00FF41]/60">
          <Li>Intentar comprometer la seguridad del sistema de evaluación o del sandbox de código.</Li>
          <Li>Ejecutar código malicioso, scripts de denegación de servicio o ataques de cualquier tipo.</Li>
          <Li>Automatizar el avance de niveles mediante bots o scripts externos.</Li>
          <Li>Publicar o compartir las soluciones de los desafíos en foros, repositorios públicos u otras plataformas.</Li>
        </ul>
        <p className="mt-4 text-[#00FF41]/50">
          El incumplimiento de estas normas podrá resultar en la suspensión inmediata y
          definitiva de la cuenta, sin derecho a reembolso.
        </p>
      </Section>

      <Section title="11. Modificación de los Términos">
        <p>
          El Titular se reserva el derecho a modificar estos Términos en cualquier momento.
          Los cambios entrarán en vigor con su publicación en esta página con la nueva fecha
          de actualización. El uso continuado de la plataforma tras la publicación de cambios
          implica la aceptación de los nuevos Términos.
        </p>
      </Section>

      <Section title="12. Ley Aplicable y Jurisdicción">
        <p className="text-[#00FF41]/50">
          Estos Términos se rigen por la legislación de{' '}
          <span className="text-[#00FF41]/70">Argentina</span>. Para cualquier
          controversia derivada del presente contrato, las partes se someten a los
          juzgados y tribunales de{' '}
          <span className="text-[#00FF41]/70">Córdoba</span>, con renuncia expresa a
          cualquier otro fuero que pudiera corresponderles.
        </p>
      </Section>

      <Section title="13. Contacto">
        <ul className="space-y-2 text-[#00FF41]/50">
          <Li>
            <span className="text-[#00FF41]/80">Soporte técnico y consultas generales:</span>{' '}
            <a href="mailto:systemsupport@dakiedtech.com" className="text-[#00FF41]/80 hover:text-[#00FF41] underline transition-colors">
              systemsupport@dakiedtech.com
            </a>
          </Li>
          <Li>
            <span className="text-[#00FF41]/80">Consultas legales, reembolsos y propiedad intelectual:</span>{' '}
            <a href="mailto:legal@dakiedtech.com" className="text-[#00FF41]/70 hover:text-[#00FF41] underline transition-colors">
              legal@dakiedtech.com
            </a>
          </Li>
        </ul>
      </Section>

    </div>
  )
}

// ── Componentes auxiliares de layout ─────────────────────────────────────────

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section>
      <h2 className="text-[#00FF41] text-base tracking-wide mb-4 pb-2 border-b border-[#00FF41]/10">
        {title}
      </h2>
      <div className="space-y-3 text-[#00FF41]/65 leading-7">
        {children}
      </div>
    </section>
  )
}

function SubSection({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="mt-4">
      <h3 className="text-[#00FF41]/80 text-sm mb-2">{title}</h3>
      {children}
    </div>
  )
}

function Li({ children }: { children: React.ReactNode }) {
  return (
    <li className="flex gap-2">
      <span className="text-[#00FF41]/30 select-none flex-shrink-0 mt-0.5">▸</span>
      <span>{children}</span>
    </li>
  )
}

function Callout({ type, children }: { type: 'warn' | 'info'; children: React.ReactNode }) {
  const colors = type === 'warn'
    ? 'border-amber-500/40 bg-amber-500/5 text-amber-400/70'
    : 'border-[#00FF41]/20 bg-[#00FF41]/5 text-[#00FF41]/60'
  return (
    <div className={`mt-4 border-l-2 pl-4 py-3 pr-4 text-sm leading-7 ${colors}`}>
      {children}
    </div>
  )
}
