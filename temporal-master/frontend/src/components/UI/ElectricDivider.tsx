/**
 * ElectricDivider.tsx — Divisor eléctrico entre secciones · DAKI EdTech
 * ────────────────────────────────────────────────────────────────────────
 * Línea horizontal con chispa animada que cruza de izquierda a derecha.
 * CSS de animación (.elec-spark) vive en globals.css.
 * Server Component: sin hooks.
 */

export default function ElectricDivider() {
  return (
    <div aria-hidden="true" className="relative w-full h-8 overflow-hidden">
      {/* Línea base con gradiente */}
      <div className="absolute top-1/2 left-0 right-0 h-px -translate-y-1/2 bg-gradient-to-r from-transparent via-[#00FF41]/12 to-transparent" />
      {/* Chispa eléctrica */}
      <div className="elec-spark" />
      {/* Conector central — rombo */}
      <div
        className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-1.5 h-1.5 border border-[#00FF41]/25 rotate-45"
      />
    </div>
  )
}
