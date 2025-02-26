import json
from pathlib import Path
from app.utils.common.files import read_file
from app.core.logger import LOGGER
from app.core.configs import AppConfig

async def load_init_data(data_schema: str, name: str):
    root_path = Path(AppConfig.ROOT_DIR)
    resources_path = root_path / "data" / "resources" / "init-data" / data_schema / f"{name}.json"

    try:
        read_data = read_file(resources_path)

        return json.loads(read_data)
    except Exception as e:
        LOGGER.error(f"Failed to load init data: {e} from ({resources_path})")

        return []
    