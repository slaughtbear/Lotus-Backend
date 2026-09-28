from functools import lru_cache # Least Recently Used Cache

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class Settings(BaseSettings):
    db_user: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str

    @computed_field
    @property
    def db_url(self) -> str:
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
        ).render_as_string(hide_password=False)

    model_config = SettingsConfigDict(
        env_file=".env", # define desde qué .env obtiene las variables de entorno
        extra="ignore", # ignora variables de entorno no definidas en la clase
    )


@lru_cache
def get_settings() -> Settings:
    """Devuelve la instancia de configuración de la aplicación.

    Gracias a `lru_cache`, `Settings()` se instancia una sola vez
    (leyendo el `.env` en ese momento) y las llamadas posteriores
    reutilizan la misma instancia cacheada, sin releer el `.env`
    ni recrear el objeto, hasta que el proceso se reinicie.
    """
    return Settings()
