from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    APP_NAME: str = "DAKI EdTech"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    SECRET_KEY: str = "change-me-in-production"

    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/pythonquest"

    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",       # dev — Next.js
        "https://dakiedtech.com",      # prod dominio propio
        "https://www.dakiedtech.com",  # prod con www
    ]

    # URL dinámica del frontend en Vercel (p. ej. https://daki-edtech.vercel.app).
    # Se inyecta en CORS_origins en tiempo de ejecución.
    # Cargar en Render: FRONTEND_URL=https://<tu-proyecto>.vercel.app
    FRONTEND_URL: str = ""

    @property
    def cors_origins(self) -> List[str]:
        """ALLOWED_ORIGINS + FRONTEND_URL si está definido."""
        origins = list(self.ALLOWED_ORIGINS)
        if self.FRONTEND_URL and self.FRONTEND_URL not in origins:
            origins.append(self.FRONTEND_URL)
        return origins

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 días — alineado con cookie
    ALGORITHM: str = "HS256"

    ANTHROPIC_API_KEY: str = ""

    # Activar SSL para conexión a BD (requerido en Supabase / producción)
    DB_SSL: bool = False

    # Clave de administrador para activación manual de licencias (/payments/verify).
    # DEBE ser diferente a SECRET_KEY.
    # Generar con: python -c "import secrets; print(secrets.token_hex(32))"
    ADMIN_API_KEY: str = "change-me-in-production"

    # Webhook secret compartido con la pasarela de pagos.
    # Generar con: python -c "import secrets; print(secrets.token_hex(32))"
    # En Stripe: copiar desde Dashboard → Webhooks → Signing secret
    PAYMENT_WEBHOOK_SECRET: str = "change-me-in-production"

    # ── Stripe — Pasarela Global (Directiva 011) ──────────────────────────────
    # sk_test_... (dev) o sk_live_... (producción)
    STRIPE_SECRET_KEY: str = ""
    # whsec_... — desde Stripe Dashboard → Developers → Webhooks → Signing secret
    STRIPE_WEBHOOK_SECRET: str = ""
    # price_... — ID del precio mensual $25 USD desde Stripe Dashboard → Products
    STRIPE_PRICE_ID: str = ""

    # Precio de la Licencia de Operador en USD (para proyección de ingresos)
    LICENSE_PRICE_USD: float = 49.0

    # ── Hotmart — Pasarela de Pagos ──────────────────────────────────────────
    # Hottok: Dashboard → Webhooks → configurar → campo "Hottok" (secreto de verificación)
    # El mismo hottok aplica a AMBOS productos (configurar en cada webhook)
    HOTMART_HOTTOK: str = ""

    # ── Producto 1: Licencia Vitalicia ($97 pago único) ───────────────────────
    # Product Key: Dashboard → Productos → tu producto → ícono de compartir → clave tipo "A12345678B"
    HOTMART_PRODUCT_KEY: str = ""
    # Offer code de la Licencia Vitalicia — Productos → Ofertas → copiar código
    # Dejar vacío si el producto tiene una sola oferta (Hotmart usará la default)
    HOTMART_LIFETIME_OFFER: str = ""

    # ── Producto 2: Suscripción Mensual ($29/mes recurrente) ──────────────────
    # Product Key del segundo producto (Suscripción)
    HOTMART_SUBSCRIPTION_KEY: str = ""
    # Offer code del plan mensual — Productos → Ofertas → copiar código
    HOTMART_MONTHLY_OFFER: str = ""

    # URL de redirección post-compra (configurar en Hotmart → Página de Agradecimiento)
    # Configurar en AMBOS productos. Hotmart redirige aquí después del pago exitoso.
    HOTMART_REDIRECT_URL: str = ""

    # ── Google OAuth ──────────────────────────────────────────────────────────
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/api/v1/auth/google/callback"

    # ── Email Transaccional (Resend) ──────────────────────────────────────────
    # Obtener en: resend.com → API Keys
    RESEND_API_KEY: str = ""
    EMAIL_FROM: str = "DAKI Nexo <noreply@dakiedtech.com>"

    # ── Whitelist Alpha (Directiva 041) ──────────────────────────────────────
    # Lista de emails autorizados, separados por coma.
    # Vacío = whitelist desactivada (registro abierto).
    # Activar en Render: ALPHA_WHITELIST=email1@gmail.com,email2@gmail.com,...
    # El rol FOUNDER siempre bypassa esta validación.
    ALPHA_WHITELIST: str = ""

    @property
    def alpha_allowed_emails(self) -> set[str]:
        """Set de emails en minúsculas. Vacío = sin restricción."""
        if not self.ALPHA_WHITELIST.strip():
            return set()
        return {e.strip().lower() for e in self.ALPHA_WHITELIST.split(",") if e.strip()}

    # TTL del JWT de admin en minutos (8 horas por defecto)
    ADMIN_TOKEN_EXPIRE_MINUTES: int = 480

    # ── Alertas CEO (Prompt 48) ───────────────────────────────────────────────
    # Discord: crea un webhook en tu servidor → Ajustes del canal → Integraciones
    ALERT_DISCORD_WEBHOOK: str = ""
    # Telegram: crea un bot con @BotFather, obtén el chat_id con @userinfobot
    ALERT_TELEGRAM_BOT_TOKEN: str = ""
    ALERT_TELEGRAM_CHAT_ID: str = ""


settings = Settings()
