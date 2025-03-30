import importlib.util
from pathlib import Path

from fastapi import APIRouter

router = APIRouter(prefix="")


def load_module_from_file(file_path: Path):
    spec = importlib.util.spec_from_file_location(file_path.stem, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def include_routers(base_path: Path, tag: str = None):
    if not base_path.is_dir():
        return

    for item in base_path.iterdir():
        if item.is_dir():
            # Use the directory name as the tag
            folder_tag = item.name
            # Recursively include routers from subdirectories
            include_routers(item, folder_tag)

        elif item.suffix == ".py" and item.stem != "__init__":
            module = load_module_from_file(item)
            if hasattr(module, "router"):
                router.include_router(
                    module.router,
                    prefix=f"/{item.parent.name}/{item.stem}",
                    tags=[
                        f"command:{tag.upper()}"
                    ],  # Use the provided tag for the router
                )


# Start including routers with no initial tag
include_routers(Path(__file__).parent)
