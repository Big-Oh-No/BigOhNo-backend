from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    postgres_password: str
    database_name: str
    postgres_user: str

    class ConfigDict:
        env_file = ".env"


settings = Settings()