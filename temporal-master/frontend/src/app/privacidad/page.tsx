import Link from 'next/link'

export const metadata = {
  title: 'Política de Privacidad — DAKI EdTech',
  description: 'Política de Privacidad y tratamiento de datos de la plataforma DAKI EdTech.',
}

export default function PrivacidadPage() {
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
          <span>SECTOR LEGAL // POLÍTICA DE PRIVACIDAD</span>
        </div>

        {/* Header */}
        <div className="border-b border-[#00FF41]/15 pb-8 mb-10">
          <div className="text-xs text-[#00FF41]/30 tracking-[0.4em] uppercase mb-3">
            Documento Legal // Protocolo v1.0
          </div>
          <h1 className="text-2xl text-[#00FF41] tracking-wide mb-4">
            Política de Privacidad
          </h1>
          <p className="text-sm text-[#00FF41]/50 leading-6">
            Plataforma DAKI EdTech — Propiedad de{' '}
            <span className="text-[#00FF41]/70">Adrian Eduardo Ardiles Peralta</span>
            <br />
            Última actualización: 20 de marzo de 2026
          </p>
        </div>

        <PrivacyDoc />

        {/* Footer */}
        <div className="mt-16 pt-8 border-t border-[#00FF41]/10 text-xs text-[#00FF41]/25 leading-6">
          <p>DAKI EdTech © 2026 · Todos los derechos reservados.</p>
          <p className="mt-1">
            <Link href="/terminos" className="hover:text-[#00FF41]/50 underline transition-colors">
              Términos y Condiciones
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

function PrivacyDoc() {
  return (
    <div className="space-y-10 text-sm leading-7">

      <Section title="1. Responsable del Tratamiento">
        <Table rows={[
          ['Responsable', 'Adrian Eduardo Ardiles Peralta'],
          ['Marca comercial', 'DAKI EdTech'],
          ['Soporte técnico', 'systemsupport@dakiedtech.com'],
          ['Legal / privacidad', 'legal@dakiedtech.com'],
          ['País', 'Argentina'],
        ]} />
      </Section>

      <Section title="2. Datos que Recopilamos">
        <p>Recopilamos únicamente los datos estrictamente necesarios para prestar el servicio:</p>
        <div className="mt-4 space-y-4">
          <DataCategory
            label="Datos de registro"
            items={[
              'Nombre de usuario (alias, no nombre real).',
              'Dirección de correo electrónico.',
              'Contraseña en formato hash (nunca en texto plano).',
            ]}
          />
          <DataCategory
            label="Datos de pago"
            items={[
              'ID de transacción de la pasarela de pago (ej. Stripe charge_id).',
              'Estado de pago (pagado / no pagado).',
              'DAKI EdTech NO almacena datos de tarjeta bancaria. El procesamiento de pago ocurre íntegramente en la pasarela de terceros.',
            ]}
          />
          <DataCategory
            label="Datos de uso y progresión"
            items={[
              'Niveles completados, XP acumulado, intentos de código enviados.',
              'Marcas de tiempo de actividad (fechas de acceso, racha de días).',
              'Fragmentos de código enviados al evaluador, almacenados de forma anonimizada para telemetría y mejora del sistema.',
              'Marcadores de lectura y pistas utilizadas.',
            ]}
          />
          <DataCategory
            label="Datos técnicos"
            items={[
              'Dirección IP (registrada en logs del servidor durante 30 días máximo).',
              'User-Agent del navegador.',
              'NO usamos cookies de rastreo ni publicidad de terceros.',
            ]}
          />
        </div>
      </Section>

      <Section title="3. Finalidad del Tratamiento">
        <ul className="space-y-2 text-[#00FF41]/60">
          <Li>Prestación del servicio educativo y gestión de tu cuenta.</Li>
          <Li>Procesamiento y verificación del pago de la Licencia de Operador.</Li>
          <Li>Seguimiento de tu progresión y personalización de la experiencia de aprendizaje.</Li>
          <Li>Detección de errores técnicos y mejora del sistema de evaluación de código.</Li>
          <Li>Cumplimiento de obligaciones legales (facturación, resolución de disputas).</Li>
          <Li>Comunicaciones transaccionales (confirmación de pago, notificaciones del servicio). Sin newsletters ni marketing sin consentimiento explícito.</Li>
        </ul>
      </Section>

      <Section title="4. Base Legal del Tratamiento">
        <ul className="space-y-2 text-[#00FF41]/60">
          <Li><strong className="text-[#00FF41]/80">Ejecución del contrato:</strong> tratamiento de datos necesario para prestarte el servicio contratado.</Li>
          <Li><strong className="text-[#00FF41]/80">Interés legítimo:</strong> telemetría técnica y seguridad del sistema.</Li>
          <Li><strong className="text-[#00FF41]/80">Consentimiento:</strong> para cualquier comunicación de marketing (si se implementa en el futuro).</Li>
          <Li><strong className="text-[#00FF41]/80">Obligación legal:</strong> conservación de datos de facturación según la normativa fiscal aplicable.</Li>
        </ul>
      </Section>

      <Section title="5. Inteligencia Artificial — DAKI">
        <Callout type="info">
          DAKI es un sistema de IA generativa integrado en DAKI EdTech. Las interacciones
          con DAKI (mensajes de retroalimentación, voz sintética) se generan en tiempo real.
          La síntesis de voz utiliza la Web Speech API del navegador, procesándose localmente
          en tu dispositivo sin enviar audio a servidores externos.
        </Callout>
        <p className="mt-4 text-[#00FF41]/50">
          Los intentos de código que envías para evaluación son procesados en el servidor
          de DAKI EdTech y pueden almacenarse de forma anonimizada para mejorar el motor
          de evaluación. No se asocian a tu identidad personal en los registros de telemetría.
        </p>
      </Section>

      <Section title="6. Conservación de Datos">
        <Table rows={[
          ['Datos de cuenta', 'Mientras la cuenta esté activa + 2 años tras baja.'],
          ['Datos de pago (ID transacción)', 'Hasta 7 años (obligación fiscal).'],
          ['Logs de servidor (IP)', '30 días.'],
          ['Telemetría de código (anonimizada)', 'Indefinido (datos desvinculados de identidad).'],
          ['Datos de progresión', 'Mientras la cuenta esté activa.'],
        ]} />
      </Section>

      <Section title="7. Cesión de Datos a Terceros">
        <p>
          DAKI EdTech no vende ni cede tus datos personales a terceros con fines
          comerciales. Compartimos datos únicamente con los siguientes proveedores de
          servicios, bajo acuerdo de confidencialidad:
        </p>
        <Table rows={[
          ['Pasarela de pago (Stripe/PayPal)', 'Procesamiento de la transacción'],
          ['Proveedor de hosting (Render/Railway)', 'Alojamiento de la API y la base de datos'],
          ['Proveedor de BD (Supabase)', 'Almacenamiento de datos de usuario y progresión'],
          ['Anthropic (opcional)', 'API de IA si se activa generación avanzada de DAKI'],
        ]} />
        <p className="mt-4 text-[#00FF41]/50">
          Todos los proveedores están sujetos a sus propias políticas de privacidad.
          DAKI EdTech puede estar legalmente obligado a facilitar datos a autoridades
          competentes si así lo requiere la ley aplicable.
        </p>
      </Section>

      <Section title="8. Tus Derechos">
        <p>
          De acuerdo con la normativa de protección de datos aplicable, tienes derecho a:
        </p>
        <ul className="mt-3 space-y-2 text-[#00FF41]/60">
          <Li><strong className="text-[#00FF41]/80">Acceso:</strong> solicitar qué datos tuyos almacenamos.</Li>
          <Li><strong className="text-[#00FF41]/80">Rectificación:</strong> corregir datos inexactos.</Li>
          <Li><strong className="text-[#00FF41]/80">Supresión («derecho al olvido»):</strong> solicitar la eliminación de tu cuenta y datos asociados.</Li>
          <Li><strong className="text-[#00FF41]/80">Portabilidad:</strong> recibir tus datos en formato legible por máquina.</Li>
          <Li><strong className="text-[#00FF41]/80">Oposición y limitación:</strong> oponerte al tratamiento en los casos previstos por la ley.</Li>
        </ul>
        <p className="mt-4 text-[#00FF41]/50">
          Para ejercer cualquiera de estos derechos, escríbenos a{' '}
          <a href="mailto:legal@dakiedtech.com" className="text-[#00FF41]/70 hover:text-[#00FF41] underline transition-colors">
            legal@dakiedtech.com
          </a>{' '}con el asunto «DERECHOS ARCO» e indicando tu email de cuenta.
          Para consultas técnicas de cuenta, escríbenos a{' '}
          <a href="mailto:systemsupport@dakiedtech.com" className="text-[#00FF41]/80 hover:text-[#00FF41] underline transition-colors">
            systemsupport@dakiedtech.com
          </a>. Atendemos en un plazo máximo de 30 días.
        </p>
      </Section>

      <Section title="9. Seguridad">
        <p className="text-[#00FF41]/60">
          Aplicamos medidas técnicas y organizativas para proteger tus datos: conexiones
          cifradas (HTTPS/TLS), contraseñas en hash (bcrypt), acceso restringido a la base
          de datos, y sandbox de ejecución de código aislado del sistema principal.
          No obstante, ningún sistema es 100% infalible; en caso de brecha de seguridad,
          notificaremos a los usuarios afectados en los plazos legalmente establecidos.
        </p>
      </Section>

      <Section title="10. Cookies">
        <p className="text-[#00FF41]/60">
          DAKI EdTech utiliza exclusivamente cookies de sesión técnicas necesarias para
          el funcionamiento del servicio (autenticación). No utilizamos cookies de
          analítica de terceros (Google Analytics) ni cookies publicitarias.
          Puedes configurar tu navegador para bloquear o eliminar cookies, aunque esto
          puede impedir el correcto funcionamiento del login.
        </p>
      </Section>

      <Section title="11. Modificaciones">
        <p className="text-[#00FF41]/60">
          Esta Política puede actualizarse. Los cambios se publicarán en esta misma página
          con la fecha de revisión actualizada. Si los cambios son sustanciales, lo
          notificaremos por email a los usuarios registrados.
        </p>
      </Section>

      <Section title="12. Contacto y Reclamaciones">
        <ul className="space-y-2 text-[#00FF41]/60">
          <Li>
            <span className="text-[#00FF41]/80">Soporte técnico y consultas generales:</span>{' '}
            <a href="mailto:systemsupport@dakiedtech.com" className="text-[#00FF41]/80 hover:text-[#00FF41] underline transition-colors">
              systemsupport@dakiedtech.com
            </a>
          </Li>
          <Li>
            <span className="text-[#00FF41]/80">Consultas sobre privacidad y ejercicio de derechos ARCO:</span>{' '}
            <a href="mailto:legal@dakiedtech.com" className="text-[#00FF41]/70 hover:text-[#00FF41] underline transition-colors">
              legal@dakiedtech.com
            </a>
          </Li>
        </ul>
        <p className="mt-4 text-[#00FF41]/40">
          Si consideras que el tratamiento de tus datos no se ajusta a la normativa,
          tienes derecho a presentar una reclamación ante la autoridad de control de
          protección de datos de tu país.
        </p>
      </Section>

    </div>
  )
}

// ── Componentes auxiliares ────────────────────────────────────────────────────

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

function Li({ children }: { children: React.ReactNode }) {
  return (
    <li className="flex gap-2">
      <span className="text-[#00FF41]/30 select-none flex-shrink-0 mt-0.5">▸</span>
      <span>{children}</span>
    </li>
  )
}

function Callout({ type, children }: { type: 'info' | 'warn'; children: React.ReactNode }) {
  const colors = type === 'warn'
    ? 'border-amber-500/40 bg-amber-500/5 text-amber-400/70'
    : 'border-[#00FF41]/20 bg-[#00FF41]/5 text-[#00FF41]/60'
  return (
    <div className={`border-l-2 pl-4 py-3 pr-4 text-sm leading-7 ${colors}`}>
      {children}
    </div>
  )
}

function DataCategory({ label, items }: { label: string; items: string[] }) {
  return (
    <div>
      <div className="text-[#00FF41]/80 text-xs tracking-[0.2em] uppercase mb-2">{label}</div>
      <ul className="space-y-1 text-[#00FF41]/55">
        {items.map((item, i) => <Li key={i}>{item}</Li>)}
      </ul>
    </div>
  )
}

function Table({ rows }: { rows: [string, string][] }) {
  return (
    <div className="mt-3 border border-[#00FF41]/10 overflow-hidden">
      {rows.map(([key, val], i) => (
        <div key={i} className={`flex text-xs ${i % 2 === 0 ? 'bg-[#00FF41]/3' : ''}`}>
          <div className="w-2/5 px-4 py-2.5 text-[#00FF41]/70 border-r border-[#00FF41]/8 flex-shrink-0">
            {key}
          </div>
          <div className="px-4 py-2.5 text-[#00FF41]/50 flex-1">
            {val}
          </div>
        </div>
      ))}
    </div>
  )
}
