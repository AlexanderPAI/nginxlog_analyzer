import gzip
import os
import re
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Generator, List, Optional

import structlog

from src.config import Settings

logger = structlog.getLogger(__name__)


@dataclass
class NginxLogFile:
    path: str
    date: date
    extension: Optional[str] = None


class NginxLogAnalyzer:
    """
    Analyzer for nginx logs.
    It searches last_nginx_file and prepares logs generator from last_nginx_file.
    """

    def __init__(self, settings: Settings):
        self._log_dir = os.path.abspath(settings.config["LOG_DIR"])

    def find_last_nginx_log_file(self) -> Optional[NginxLogFile]:

        nginx_log_title_regex = (
            r"^nginx-access-ui\.log-(?P<date>\d{8})(?P<extension>(\.gz)?)$"
        )

        last_date: Optional[date] = None
        last_log = None

        for file in Path(self._log_dir).iterdir():
            name = re.match(nginx_log_title_regex, file.name)
            if name:
                file_date = name.group("date")
                extension = name.group("extension")
                if file_date:
                    file_date = datetime.strptime(file_date, "%Y%m%d").date()
                    if not isinstance(file_date, date):
                        raise TypeError(f"Date in log_filename is not {date}")
                    if last_date is None or file_date > last_date:
                        last_date = file_date
                        last_log = NginxLogFile(
                            path=str(file), date=file_date, extension=extension
                        )

        if last_log:
            return last_log
        return None

    @staticmethod
    def get_nginx_logs(
        nginx_log_file: NginxLogFile,
    ) -> Generator[List[str], None, None]:
        """Generator for parsing nginx log line by line"""
        if not nginx_log_file:
            raise ValueError("LastLogFile wasn't passed to get_nginx_logs_generator")
        open_func = gzip.open if nginx_log_file.extension == ".gz" else open
        try:
            with open_func(nginx_log_file.path, "rt", encoding="utf-8") as file:
                for line in file:
                    yield line.strip().split(" ")
        except PermissionError as e:
            logger(f"There is no access to the file: {e}")
        except IOError as e:
            logger.error(f"The file cannot be read: {e}")
        except UnicodeDecodeError as e:
            logger.error(f"Encoding error: {e}")
