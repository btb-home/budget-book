import os
import rootdir
from pathlib import Path
from dotenv import load_dotenv

class Setting:
    __root__: str = rootdir.root_dir(__file__)
    APP_ROOT_DIR: Path = Path(__root__)
    ROOT_DIR: Path = APP_ROOT_DIR.parent
    CONF_DIR: Path = ROOT_DIR / "conf"
    print(CONF_DIR)

    @classmethod
    def load_env(cls):
        os.chdir(cls.APP_ROOT_DIR)

        app_env = os.getenv("APP_ENVIRONMENT", "local")
        assert app_env in ("local", "dev", "prod"), f"Invalid environment: {app_env}"

        dotenv_path = cls.CONF_DIR / app_env / f".env.{app_env}"
        load_dotenv(dotenv_path, verbose=True)
        print(dotenv_path)

        return cls()

setting = Setting.load_env()

class AppConfig:
    """config for the app

    """
    APP_NAME: str = os.environ["APP_NAME"]
    APP_VERSION: str = os.environ["APP_VERSION"]
    APP_ENVIRONMENT: str = os.environ["APP_ENVIRONMENT"]

    APP_LOG_LEVEL: str = os.environ["APP_LOG_LEVEL"]
    
    # Uvicorn Config
    UVICORN_LOG_LEVEL: str = os.environ["UVICORN_LOG_LEVEL"]
    
    # Redis Config
    REDIS_HOST: str = os.environ["REDIS_HOST"]
    REDIS_PORT: int = int(os.environ["REDIS_PORT"])
    REDIS_DB_SESSION: int = int(os.environ["REDIS_DB_SESSION"])
    REDIS_DB_HISTORY: int = int(os.environ["REDIS_DB_HISTORY"])
    REDIS_DB_APP: int = int(os.environ["REDIS_DB_APP"])
    REDIS_PASSWORD: str = os.environ["REDIS_PASSWORD"]

    # SQLAlchemy Database Config
    SQLALCHEMY_DATABASE_URL: str = os.environ["SQLALCHEMY_DATABASE_URL"]
    SQLALCHEMY_ASYNC_DATABASE_URL: str = os.environ["SQLALCHEMY_ASYNC_DATABASE_URL"]

    SQLALCHEMY_DATABASE_DRIVER: str = os.environ["SQLALCHEMY_DATABASE_DRIVER"]
    SQLALCHEMY_DATABASE_USERNAME: str = os.environ["SQLALCHEMY_DATABASE_USERNAME"]
    SQLALCHEMY_DATABASE_PASSWORD: str = os.environ["SQLALCHEMY_DATABASE_PASSWORD"]
    SQLALCHEMY_DATABASE_HOST: str = os.environ["SQLALCHEMY_DATABASE_HOST"]
    SQLALCHEMY_DATABASE_PORT: int = int(os.environ["SQLALCHEMY_DATABASE_PORT"])
    SQLALCHEMY_DATABASE_DBNAME: str = os.environ["SQLALCHEMY_DATABASE_DBNAME"]
    