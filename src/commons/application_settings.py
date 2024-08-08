from pydantic_settings import BaseSettings


class ApplicationSettings(BaseSettings):

    openai_api_key : str

    class Config:
        env_file = ".env"

