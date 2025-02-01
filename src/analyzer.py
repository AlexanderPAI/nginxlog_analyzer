import os
import re
from datetime import date, datetime
from pathlib import Path
from typing import Optional

import structlog

from src.config import Settings

logger = structlog.getLogger(__name__)


class NginxLogAnalyzer:
    """Analyzer for nginx logs"""

    NGINX_LOG_TITLE_REGEX = r"^nginx-access-ui\.log-(\d{8})(\.gz)?$"
    DATE_REGEX = r"(?P<date>\d{8})"

    def __init__(self, settings: Settings):
        self._log_dir = os.path.abspath(settings.config["LOG_DIR"])

    def find_last_nginx_log(self) -> Optional[Path]:
        log_dir = Path(self._log_dir)

        last_date: Optional[date] = None
        last_log: Optional[Path] = None

        for file in log_dir.iterdir():
            if re.match(self.NGINX_LOG_TITLE_REGEX, file.name):
                date_str = re.search(self.DATE_REGEX, file.name)
                if date_str:
                    date_from_name = datetime.strptime(
                        date_str["date"], "%Y%m%d"
                    ).date()
                    if last_date is None or date_from_name > last_date:
                        last_date = date_from_name
                        last_log = file
            return last_log
        logger.error(f"The logs were not found at {self._log_dir}")
        return None
