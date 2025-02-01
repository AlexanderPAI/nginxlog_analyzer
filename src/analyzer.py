import gzip
import os
import re
from datetime import date, datetime
from pathlib import Path
from typing import Generator, List, Optional

import structlog

from src.config import Settings

logger = structlog.getLogger(__name__)


class NginxLogAnalyzer:
    """Analyzer for nginx logs"""

    def __init__(self, settings: Settings):
        self._log_dir = os.path.abspath(settings.config["LOG_DIR"])

    def find_last_nginx_log_file(self, log_dir: Path) -> Optional[Path]:
        nginx_log_title_regex = r"^nginx-access-ui\.log-(\d{8})(\.gz)?$"
        date_regex = r"(?P<date>\d{8})"

        log_dir = Path(log_dir)
        last_date: Optional[date] = None
        last_log: Optional[Path] = None
        print(last_date)

        for file in log_dir.iterdir():
            if re.match(nginx_log_title_regex, file.name):
                date_str = re.search(date_regex, file.name)
                if date_str:
                    date_from_name = datetime.strptime(
                        date_str["date"], "%Y%m%d"
                    ).date()
                    if last_date is None or date_from_name > last_date:
                        last_date = date_from_name
                        print(last_date)
                        last_log = file

        if last_log:
            return last_log
        logger.error(f"The logs were not found at {self._log_dir}")
        return None

    @staticmethod
    def get_nginx_logs(nginx_log_file: Path) -> Generator[List[str], None, None]:
        """Generator for parsing nginx log line by line"""
        if nginx_log_file:
            open_func = gzip.open if nginx_log_file.suffix == ".gz" else open
            with open_func(nginx_log_file, "rt", encoding="utf-8") as file:
                for line in file:
                    yield line.strip().split(" ")
