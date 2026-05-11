from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    supabase_url: str = Field(..., alias="SUPABASE_URL")
    supabase_service_role_key: str = Field(..., alias="SUPABASE_SERVICE_ROLE_KEY")
    supabase_anon_key: str = Field(..., alias="SUPABASE_ANON_KEY")
    cors_origins_raw: str = Field("http://localhost:5173", alias="CORS_ORIGINS")

    @property
    def cors_origins(self):
        return [o.strip() for o in self.cors_origins_raw.split(",") if o.strip()]

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
