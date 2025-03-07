import importlib
import pathlib
from sys import stderr
from logging import getLogger


def load_routes(app, base_path: str, url_prefix: str = ""):
    logger = getLogger(__name__)
    logger.setLevel("INFO")

    path = pathlib.Path(base_path)
    # Recursively find all .py files
    for route_file in path.rglob("*.py"):
        if route_file.stem != "__init__":
            # Convert path to module notation and add 'src.' prefix
            relative_path = route_file.relative_to(path.parent)
            module_path = "src." + str(relative_path).replace("/", ".").replace("\\", ".")[:-3]  # remove .py

            try:
                logger.info(f"Loading {module_path}")
                module = importlib.import_module(module_path)
                if hasattr(module, "router"):
                    app.include_router(module.router, prefix=url_prefix)
            except Exception as e:
                print(f"Failed to load {module_path}: {e}", file=stderr)
                raise e
