from pathlib import Path
from typing import Any, Dict, Optional


def create_temp_file(
    temp_config_path: str, content: Optional[Dict[Any, Any] | str] = None
) -> None:
    """Create temp config file"""
    temp_config = Path(temp_config_path)
    if isinstance(content, Dict):
        with open(temp_config, "w", encoding="utf-8") as file:
            for key, value in content.items():
                file.write(f"{key}={value}\n")
    if isinstance(content, str):
        lines = content.split("\n")
        with open(temp_config, "w", encoding="utf-8") as file:
            for line in lines:
                file.write(f"{line}\n")
    if not content:
        with open(temp_config, "w", encoding="utf-8") as file:
            file.write("")


def delete_temp_file(temp_config_path: str) -> None:
    """Delete temp config file"""
    temp_config = Path(temp_config_path)
    temp_config.unlink()
