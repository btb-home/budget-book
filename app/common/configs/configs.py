import os
import rootdir
from dotenv import load_dotenv
from pathlib import Path


class Setting:
    __root__: str = rootdir.root_dir(__file__)
    APP_ROOT_DIR: Path = Path(__root__)
    ROOT_DIR: Path = APP_ROOT_DIR.parent
    CONF_DIR: Path = ROOT_DIR / "conf"

    @classmethod
    def load_env(cls):
        os.chdir(cls.APP_ROOT_DIR)

        app_env = os.getenv("ENVIRONMENT", "local")
        assert app_env in ("local", "dev", "prod"), f"Invalid environment: {app_env}"

        dotenv_path = cls.CONF_DIR / app_env / f".env.{app_env}"
        load_dotenv(dotenv_path, verbose=True)

        return cls()

setting = Setting.load_env()
