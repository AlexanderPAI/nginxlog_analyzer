from pathlib import Path
from typing import Any, Dict, Optional


def create_temp_file(
    temp_config_path: str, config: Optional[Dict[Any, Any]] = None
) -> None:
    """Create temp config file"""
    temp_config = Path(temp_config_path)
    with open(temp_config, "w", encoding="utf-8") as file:
        if config is not None:
            for key, value in config.items():
                file.write(f"{key}={value}\n")


def delete_temp_file(temp_config_path: str) -> None:
    """Delete temp config file"""
    temp_config = Path(temp_config_path)
    temp_config.unlink()
