from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """
    All Settings are here
    > dotenv ファイルを使用する場合でも、pydantic はdotenv ファイルだけでなく環境変数も読み取ります。
    環境変数は常に dotenv ファイルからロードされた値よりも優先されます。
    ref: https://docs.pydantic.dev/latest/usage/settings/
    """

    # app
    APP_NAME: str = "python_template"
    PORT: int = Field(env="PORT", default=3000)
    DEBUG: bool = Field(env="DEBUG", default=True)
    LOG_LEVEL: str = Field(env="LOG_LEVEL", default="info")
    # DB
    POSTGRES_CONNECTION_STRING: str = Field(env="POSTGRES_CONNECTION_STRING", default="")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        frozen = True
