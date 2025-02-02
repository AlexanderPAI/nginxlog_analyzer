import json
import os.path
from string import Template
from typing import Any, Dict, Generator, List

import structlog

from src.analyzer import NginxLogFile
from src.config import Settings

logger = structlog.getLogger(__name__)


class Reporter:
    """Service for making report_data"""

    _REPORT_TEMPLATE_PATH = "./report_template/report.html"

    def __init__(self, settings: Settings, last_log_file: NginxLogFile) -> None:
        self._report_dir = settings.config["REPORT_DIR"]
        self._report_size = settings.config["REPORT_SIZE"]
        self.last_log_file = last_log_file
        self.report_file = (
            f"{self._report_dir}/report-{last_log_file.date.strftime("%Y.%m.%d")}.html"
        )

    @staticmethod
    def _get_median(number_list) -> float:
        """Func for getting median from list of numbers"""
        number_list.sort()
        n = len(number_list)
        mid = n // 2
        if n % 2 == 0:
            return (number_list[mid - 1] + number_list[mid]) / 2
        else:
            return number_list[mid]

    @staticmethod
    def _create_report_record(report, log, total_count, total_time):
        """Create url-record in report"""
        url = log[7]
        time = float(log[-1])

        report[url] = {
            "count": 1,
            "time_sum": time,
            "time_max": time,
            "time_list": [time],
            "time_med": time,
            "time_avg": time,
            "count_perc": (1 / total_count) * 100,
            "time_perc": (time / total_time) * 100,
        }

    def _refresh_report_record(self, report, log, total_count, total_time):
        """Refresh url-record in report"""
        url = log[7]
        time = float(log[-1])

        report[url]["count"] += 1
        report[url]["time_sum"] += time
        report[url]["time_max"] = max(report[url]["time_max"], time)
        report[url]["time_list"].append(time)
        report[url]["time_med"] = self._get_median(report[url]["time_list"])
        report[url]["time_avg"] = report[url]["time_sum"] / report[url]["count"]
        report[url]["count_perc"] = (report[url]["count"] / total_count) * 100
        report[url]["time_perc"] = (report[url]["time_sum"] / total_time) * 100

    def check_report_exist(self):
        """Check report for log"""
        return os.path.isfile(self.report_file)

    def make_report_data(
        self, nginx_logs: Generator[List[str], None, None]
    ) -> List[Dict[str, str]]:
        """Make report data"""
        report: Dict[str, Any] = {}

        total_count: int = 0
        total_time: float = 0.0

        for log in nginx_logs:
            url = log[7]
            time = float(log[-1])

            total_count += 1
            total_time += time

            if report.get(url):
                self._refresh_report_record(report, log, total_count, total_time)
            else:
                self._create_report_record(report, log, total_count, total_time)
        sorted_report = dict(
            sorted(report.items(), key=lambda item: item[1]["time_sum"], reverse=True)
        )
        result = []
        # O(n log n + n * m)
        for url, data in sorted_report.items():
            element = {"url": url, **data}
            element.pop("time_list")
            result.append(element)
        return result

    def render_report(self, report_data: List[Dict[str, Any]]) -> None:
        """Render report_data to html-file"""
        with open(self._REPORT_TEMPLATE_PATH, "r") as file:
            template_data = file.read()
        template = Template(template_data)
        table_json = json.dumps(report_data[: int(self._report_size)])
        html_report = template.safe_substitute(table_json=table_json)
        with open(self.report_file, "w") as file:
            file.write(html_report)
