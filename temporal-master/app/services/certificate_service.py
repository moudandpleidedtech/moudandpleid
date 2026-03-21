"""
certificate_service.py — Forja de PDFs del Nexo

Genera el certificado oficial DAKI EdTech en memoria (io.BytesIO).
Formato: A4 apaisado (landscape).  Sin tocar el disco del servidor.

Paleta:
    Fondo          #0D0D0D  — negro profundo
    Acento dorado  #FFD700
    Acento púrpura #8A2BE2
    Verde neón     #00FF41  (metadatos / hash)
    Texto claro    #E0E0E0
"""

import io
import random
import string
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas

# ── Paleta ────────────────────────────────────────────────────────────────────

BG          = colors.HexColor("#0D0D0D")
GOLD        = colors.HexColor("#FFD700")
PURPLE      = colors.HexColor("#8A2BE2")
NEON        = colors.HexColor("#00FF41")
WHITE       = colors.HexColor("#E0E0E0")
DIM         = colors.HexColor("#555555")
PURPLE_DARK = colors.HexColor("#2D0066")

# ── Helpers ───────────────────────────────────────────────────────────────────

def _cert_id() -> str:
    pool = string.ascii_uppercase + string.digits
    return "GG-CERT-" + "".join(random.choices(pool, k=6))


def _today() -> str:
    d = datetime.utcnow()
    months = ["ENE","FEB","MAR","ABR","MAY","JUN",
               "JUL","AGO","SEP","OCT","NOV","DIC"]
    return f"{d.day:02d} {months[d.month - 1]} {d.year}"


# ── Core draw functions ────────────────────────────────────────────────────────

def _draw_background(c: Canvas, w: float, h: float) -> None:
    c.setFillColor(BG)
    c.rect(0, 0, w, h, fill=1, stroke=0)


def _draw_outer_border(c: Canvas, w: float, h: float) -> None:
    """Marco dorado exterior con sombra púrpura."""
    pad = 8 * mm
    # Sombra / glow púrpura (desplazado 1.5mm)
    c.setStrokeColor(PURPLE)
    c.setLineWidth(1.2)
    c.rect(pad + 1.5 * mm, pad - 1.5 * mm,
           w - 2 * pad - 1.5 * mm, h - 2 * pad + 1.5 * mm,
           fill=0, stroke=1)
    # Marco dorado
    c.setStrokeColor(GOLD)
    c.setLineWidth(2.2)
    c.rect(pad, pad, w - 2 * pad, h - 2 * pad, fill=0, stroke=1)


def _draw_inner_border(c: Canvas, w: float, h: float) -> None:
    """Línea interior delgada."""
    pad = 12 * mm
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.5)
    c.setDash([2, 3])
    c.rect(pad, pad, w - 2 * pad, h - 2 * pad, fill=0, stroke=1)
    c.setDash()  # reset dash


def _draw_corner_accents(c: Canvas, w: float, h: float) -> None:
    """Esquinas tipo HUD."""
    arm = 14 * mm
    pad = 8 * mm
    c.setStrokeColor(GOLD)
    c.setLineWidth(2.5)
    corners = [
        (pad, pad),          # bottom-left
        (pad, h - pad),      # top-left
        (w - pad, h - pad),  # top-right
        (w - pad, pad),      # bottom-right
    ]
    dirs = [
        (+1, +1), (+1, -1), (-1, -1), (-1, +1)
    ]
    for (cx, cy), (dx, dy) in zip(corners, dirs):
        c.line(cx, cy, cx + dx * arm, cy)
        c.line(cx, cy, cx, cy + dy * arm)


def _draw_scanlines(c: Canvas, w: float, h: float) -> None:
    """Líneas de escaneo sutiles (CRT effect)."""
    c.setStrokeColor(colors.HexColor("#111111"))
    c.setLineWidth(0.3)
    step = 2.4
    y = 0.0
    while y < h:
        c.line(0, y, w, y)
        y += step


def _draw_header_band(c: Canvas, w: float, h: float) -> None:
    """Banda de título en la parte superior."""
    band_h = 14 * mm
    top    = h - 22 * mm
    # Fondo banda
    c.setFillColor(PURPLE_DARK)
    c.rect(20 * mm, top, w - 40 * mm, band_h, fill=1, stroke=0)
    # Líneas top/bottom de la banda en dorado
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.8)
    c.line(20 * mm, top,             w - 20 * mm, top)
    c.line(20 * mm, top + band_h,    w - 20 * mm, top + band_h)
    # Texto de la banda
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(w / 2, top + 4.5 * mm, "GLITCH & GOLD NETWORK  ◈  AUTORIDAD CENTRAL DEL NEXO")


def _draw_title(c: Canvas, w: float, h: float) -> None:
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 38)
    c.drawCentredString(w / 2, h - 54 * mm, "CERTIFICADO DE OPERADOR")


def _draw_username(c: Canvas, w: float, h: float, username: str) -> None:
    # Separador
    sep_y = h - 64 * mm
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.7)
    c.line(30 * mm, sep_y, w - 30 * mm, sep_y)

    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 30)
    c.drawCentredString(w / 2, h - 80 * mm, username.upper())


def _draw_subtitle(c: Canvas, w: float, h: float) -> None:
    mid_y = h / 2

    # "Validación DAKI" en púrpura
    c.setFillColor(PURPLE)
    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(w / 2, mid_y + 6 * mm, "Validación DAKI")

    # Línea decorativa
    c.setStrokeColor(PURPLE)
    c.setLineWidth(0.6)
    c.line(w / 2 - 45 * mm, mid_y + 3 * mm, w / 2 + 45 * mm, mid_y + 3 * mm)

    # Nivel 100
    c.setFillColor(WHITE)
    c.setFont("Helvetica", 12)
    c.drawCentredString(w / 2, mid_y - 4 * mm, "Nivel 100 Completado  ·  Nexo Vencido")


def _draw_daki_badge(c: Canvas, w: float, h: float) -> None:
    """Rombo decorativo central."""
    cx = w / 2
    cy = h / 2 - 20 * mm
    size = 6 * mm
    c.setStrokeColor(PURPLE)
    c.setLineWidth(1.0)
    c.setFillColor(PURPLE_DARK)
    path = c.beginPath()
    path.moveTo(cx,        cy + size)
    path.lineTo(cx + size, cy)
    path.lineTo(cx,        cy - size)
    path.lineTo(cx - size, cy)
    path.close()
    c.drawPath(path, fill=1, stroke=1)
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 7)
    c.drawCentredString(cx, cy - 2, "DAKI")


def _draw_metadata_row(
    c: Canvas, w: float, h: float, cert_id: str, date_str: str
) -> None:
    """Fila inferior: hash (izquierda), fecha (derecha), selector central."""
    base_y = 18 * mm

    # Hash ID
    c.setFillColor(NEON)
    c.setFont("Courier-Bold", 9)
    c.drawString(20 * mm, base_y, cert_id)

    # Separador central
    c.setFillColor(DIM)
    c.setFont("Helvetica", 8)
    c.drawCentredString(w / 2, base_y, "NEXO CENTRAL  ◈  CERTIFICACIÓN PERMANENTE")

    # Fecha
    c.setFillColor(NEON)
    c.setFont("Courier-Bold", 9)
    c.drawRightString(w - 20 * mm, base_y, date_str)

    # Línea separadora de la fila de metadatos
    c.setStrokeColor(DIM)
    c.setLineWidth(0.4)
    c.line(20 * mm, base_y + 5 * mm, w - 20 * mm, base_y + 5 * mm)


def _draw_pixel_grid(c: Canvas, x: float, y: float, cols: int = 6, rows: int = 4) -> None:
    """Mini cuadrícula de píxeles decorativa."""
    size = 2.8 * mm
    gap  = 1.2 * mm
    for row in range(rows):
        for col in range(cols):
            px = x + col * (size + gap)
            py = y + row * (size + gap)
            shade = GOLD if (row + col) % 3 == 0 else PURPLE
            c.setFillColor(shade)
            c.setStrokeColor(shade)
            c.setLineWidth(0.2)
            c.rect(px, py, size, size, fill=1, stroke=0)


# ── Public API ────────────────────────────────────────────────────────────────

def build_certificate_pdf(username: str) -> tuple[bytes, str]:
    """
    Genera el PDF del certificado en memoria.

    Returns:
        (pdf_bytes, cert_id)  — los bytes del PDF y el ID único emitido.
    """
    buf = io.BytesIO()
    page_size = landscape(A4)
    w, h = page_size

    c = Canvas(buf, pagesize=page_size)
    c.setTitle(f"DAKI EdTech — Certificado de Completado: {username}")
    c.setAuthor("DAKI EdTech")
    c.setSubject("Certificado oficial de completado del programa de Python — DAKI EdTech")
    c.setCreator("DAKI EdTech Platform")

    cert_id  = _cert_id()
    date_str = _today()

    _draw_background(c, w, h)
    _draw_scanlines(c, w, h)
    _draw_outer_border(c, w, h)
    _draw_inner_border(c, w, h)
    _draw_corner_accents(c, w, h)
    _draw_header_band(c, w, h)
    _draw_title(c, w, h)
    _draw_username(c, w, h, username)
    _draw_subtitle(c, w, h)
    _draw_daki_badge(c, w, h)
    _draw_metadata_row(c, w, h, cert_id, date_str)

    # Cuadrículas decorativas esquinas
    _draw_pixel_grid(c, 20 * mm, h - 48 * mm)
    _draw_pixel_grid(c, w - 20 * mm - 6 * (2.8 + 1.2) * mm, h - 48 * mm)

    c.save()
    return buf.getvalue(), cert_id
