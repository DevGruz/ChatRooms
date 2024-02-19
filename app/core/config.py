from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class PostgresSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="POSTGRES")

    host: str
    port: int
    user: str
    password: str
    name: str

    @property
    def url(self):
        # return f"postgresql+asyncpg://postgres:postgres@db:5432/chat_rooms"
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", env_nested_delimiter="__"
    )

    secret_key: str
    database: PostgresSettings = Field(alias="POSTGRES")


settings = Settings()
