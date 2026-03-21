from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    APP_NAME: str = "DAKI EdTech"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    SECRET_KEY: str = "change-me-in-production"

    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/pythonquest"

    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"

    ANTHROPIC_API_KEY: str = ""

    # Activar SSL para conexión a BD (requerido en Supabase / producción)
    DB_SSL: bool = False

    # Webhook secret compartido con la pasarela de pagos.
    # Generar con: python -c "import secrets; print(secrets.token_hex(32))"
    # En Stripe: copiar desde Dashboard → Webhooks → Signing secret
    PAYMENT_WEBHOOK_SECRET: str = "change-me-in-production"

    # Precio de la Licencia de Operador en USD (para proyección de ingresos)
    LICENSE_PRICE_USD: float = 49.0

    # TTL del JWT de admin en minutos (8 horas por defecto)
    ADMIN_TOKEN_EXPIRE_MINUTES: int = 480

    # ── Alertas CEO (Prompt 48) ───────────────────────────────────────────────
    # Discord: crea un webhook en tu servidor → Ajustes del canal → Integraciones
    ALERT_DISCORD_WEBHOOK: str = ""
    # Telegram: crea un bot con @BotFather, obtén el chat_id con @userinfobot
    ALERT_TELEGRAM_BOT_TOKEN: str = ""
    ALERT_TELEGRAM_CHAT_ID: str = ""


settings = Settings()
