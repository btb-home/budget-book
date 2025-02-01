from pydantic import Field
from pydantic_settings import BaseSettings


class Setting(BaseSettings):
    # Project info
    DB_DRIVER: str = Field(default="jdbc protocol")
    DB_DATABASE: str = Field(default="database")
    DB_USERNAME: str = Field(default="username")
    DB_PASSWORD: str = Field(default="password")
    DB_HOST: str = Field(default="127.0.0.1")
    DB_PORT: int = Field(default=5433)
    
    @property
    def DATABASE_URL(self):
        return f"{self.DB_DRIVER}://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_DATABASE}"

    def __getattr__(self, name):
        return getattr(self, name.lower())