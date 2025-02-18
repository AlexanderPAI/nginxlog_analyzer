import os.path
import sys
import traceback
from pathlib import Path
from types import TracebackType
from typing import Dict, Optional, Type

import structlog

logger = structlog.getLogger(__name__)


class LoggerConfig:
    """Config for Logger"""

    def __init__(self) -> None:
        structlog.configure(
            processors=[
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.add_log_level,
                structlog.processors.JSONRenderer(ensure_ascii=False),
            ]
        )
        sys.excepthook = self._exception_logging

    @staticmethod
    def write_logs_to_file(file_path):
        structlog.configure(
            logger_factory=structlog.WriteLoggerFactory(
                file=Path(file_path).open("a", encoding="utf-8"),
            ),
        )

    def _exception_logging(
        self,
        exc_type: Type[BaseException],
        exc_info: BaseException,
        exc_tb: Optional[TracebackType],
    ) -> None:
        """
        Handler for catching all exception to structlog.
        For sys.excepthook.
        """
        logger.error(
            exception_class=str(exc_type),
            event=exc_info,
            traceback=traceback.extract_tb(exc_tb),
        )


class Settings:
    """Config for Analyzer"""

    _DEFAULT_CONFIG_FILE_PATH: str = "./config/analyzer.cfg"
    _DEFAULT_CONFIG: Dict = {
        "REPORT_SIZE": 1000,
        "REPORT_DIR": "./reports",
        "LOG_DIR": "./log",
        "ANALYZER_LOG_FILE_PATH": None,
    }

    def __init__(self, config_file_path: Optional[str] = None) -> None:
        self.config_file_path: str = os.path.abspath(self._DEFAULT_CONFIG_FILE_PATH)
        self.config: Dict = self._DEFAULT_CONFIG
        self._logger_config: LoggerConfig = LoggerConfig()

        if config_file_path:
            self.config_file_path = os.path.abspath(config_file_path)

        self._check_settings_from_config_file()

    def _check_settings_from_config_file(self) -> None:
        """Check and set settings from config_file"""
        if self._config_file_exists():
            self._parse_config_file()
        else:
            raise FileNotFoundError(
                f"Config file was not found at {self.config_file_path}."
            )

        if self.config.get("ANALYZER_LOG_FILE_PATH"):
            self._logger_config.write_logs_to_file(
                self.config.get("ANALYZER_LOG_FILE_PATH")
            )

        logger.info(f"Settings: {self.config}")

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
