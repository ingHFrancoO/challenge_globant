from pydantic_settings import BaseSettings
from urllib.parse import quote_plus

class Settings(BaseSettings):
    PROJECT_NAME: str = "GLobant Challenge"
    PG_USER: str
    PG_PASSWORD: str
    PG_HOST: str
    PG_PORT: str
    PG_DB: str

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        password = quote_plus(self.PG_PASSWORD)  # escapa caracteres especiales
        return f"postgresql://{self.PG_USER}:{password}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DB}"

    class Config:
        env_file = ".env"
        extra = "ignore"   # evita errores si hay claves adicionales

settings = Settings()
