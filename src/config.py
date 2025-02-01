import logging
import os.path
from typing import Dict, Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


logger = logging.getLogger(__name__)


class Settings:
    """Config for Analyzer"""

    _DEFAULT_CONFIG_FILE_PATH: str = "./settings.cfg"
    _DEFAULT_CONFIG: Dict = {
        "REPORT_SIZE": 1000,
        "REPORT_DIR": "./reports",
        "LOG_DIR": "./log",
    }

    def __init__(self, config_file_path: Optional[str] = None) -> None:
        self.config_file_path = os.path.abspath(self._DEFAULT_CONFIG_FILE_PATH)
        self.config = self._DEFAULT_CONFIG

        if config_file_path:
            self.config_file_path = os.path.abspath(config_file_path)

        if self._config_file_exists():
            self._parse_config_file()
        else:
            logger.error(f"Config file was not found at {self.config_file_path}.")

    def _config_file_exists(self) -> bool:
        """Check the existence of the file at self.config_file_path"""
        return os.path.isfile(self.config_file_path)

    def _parse_config_file(self) -> None:
        """Parse config_file at self.config_file_path"""
        with open(self.config_file_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if "=" in line:
                    key, value = line.split("=", 1)
                    if key in self.config:
                        self.config[key] = value
