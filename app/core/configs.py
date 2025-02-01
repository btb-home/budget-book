from pathlib import Path
from pydantic import AliasGenerator

from app.utils.configs.configs import Setting

MODULE_PATH = Path(__file__).parent.parent.parent

MODULE_ENV = str(MODULE_PATH.joinpath(".env"))
MODULE_PREFIX = "BTB_BGB_"

class ModuleConfig(Setting):
    class Config:
        # extra = "allow"
        env_file = MODULE_ENV
        env_file_encoding = "utf-8"
        alias_generator = AliasGenerator(
            alias=lambda field_name: MODULE_PREFIX + field_name.upper()
        )


configs = ModuleConfig()