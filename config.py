from pydantic import BaseSettings


class Settings(BaseSettings):
    sender: str
    password: str
    
    class Config:
        env_file = ".env"


setting = Settings()