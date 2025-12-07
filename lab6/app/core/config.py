from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_driver: str = "postgresql"
    db_user: str = "postgres"
    db_password: str = "postgres"
    db_host: str = "db"
    db_port: int = 5432
    db_name: str = "library"

    app_env: str = "development"

    @property
    def database_url(self) -> str:
        return f"{self.db_driver}+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
