import os
from pathlib import Path
from typing import Dict

import pytest
import structlog

from src.config import Settings

logger = structlog.getLogger("test")


def create_temp_config_file(temp_config_path: str, config: Dict) -> None:
    """Create temp config file"""
    temp_config = Path(temp_config_path)
    with open(temp_config, "w", encoding="utf-8") as file:
        for key, value in config.items():
            file.write(f"{key}={value}\n")


def delete_temp_config_file(temp_config_path: str) -> None:
    """Delete temp config file"""
    temp_config = Path(temp_config_path)
    temp_config.unlink()


class TestSettings:
    """Check settings"""

    DEFAULT_CONFIG_FILE_PATH: str = "./config/analyzer.cfg"
    NOT_DEFAULT_CONFIG_FILE_PATH: str = "./config/temp_config.cfg"
    DEFAULT_CONFIG: Dict = {
        "REPORT_SIZE": "1000",
        "REPORT_DIR": "./reports",
        "LOG_DIR": "./log",
        "ANALYZER_LOG_FILE_PATH": "",
    }
    NOT_DEFAULT_CONFIG: Dict = {
        "REPORT_SIZE": "100",
        "REPORT_DIR": "./report_dir",
        "LOG_DIR": "./nginx_log",
        "ANALYZER_LOG_FILE_PATH": "",
    }

    def test_init_settings_without_config_file(self):
        """Check init Settings without config file"""
        config_args = {"--config": "nowhere"}
        with pytest.raises(FileNotFoundError):
            Settings(config_args["--config"])

    def test_init_settings_without_config_arg(self):
        """Check init Settings without arg --config"""
        settings = Settings()
        assert settings.config_file_path == os.path.abspath(
            self.DEFAULT_CONFIG_FILE_PATH
        ), "Default config path does not match expected path"
        assert (
            settings.config == self.DEFAULT_CONFIG
        ), "Default config does not match expected config"

    def test_init_settings_with_config_arg(self):
        """Check init Settings with arg --config"""
        config_args = {"--config": self.NOT_DEFAULT_CONFIG_FILE_PATH}
        create_temp_config_file(config_args["--config"], self.NOT_DEFAULT_CONFIG)
        settings = Settings(config_args["--config"])
        delete_temp_config_file(config_args["--config"])
        assert settings.config_file_path == os.path.abspath(
            self.NOT_DEFAULT_CONFIG_FILE_PATH
        ), "Config path does not match expected path"
        assert (
            settings.config == self.NOT_DEFAULT_CONFIG
        ), "Config does not match expected config"
