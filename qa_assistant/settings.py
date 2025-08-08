from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    masters_urls: list[str] = [
        "https://abit.itmo.ru/program/master/ai",
        "https://abit.itmo.ru/program/master/ai_product",
    ]
    bot_token: str = ""
    postgres_dsn: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"


settings = Settings()
