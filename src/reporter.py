from typing import Any, Dict, Generator, List

import structlog

logger = structlog.getLogger(__name__)


class Reporter:
    """Service for making report_data"""

    @staticmethod
    def get_median(number_list) -> float:
        """Func for getting median from list of numbers"""
        number_list.sort()
        n = len(number_list)
        mid = n // 2
        if n % 2 == 0:
            return (number_list[mid - 1] + number_list[mid]) / 2
        else:
            return number_list[mid]

    @staticmethod
    def create_report_record(report, log, total_count, total_time):
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

    def refresh_report_record(self, report, log, total_count, total_time):
        """Refresh url-record in report"""
        url = log[7]
        time = float(log[-1])

        report[url]["count"] += 1
        report[url]["time_sum"] += time
        report[url]["time_max"] = max(report[url]["time_max"], time)
        report[url]["time_list"].append(time)
        report[url]["time_med"] = self.get_median(report[url]["time_list"])
        report[url]["time_avg"] = report[url]["time_sum"] / report[url]["count"]
        report[url]["count_perc"] = (report[url]["count"] / total_count) * 100
        report[url]["time_perc"] = (report[url]["time_sum"] / total_time) * 100

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
                self.refresh_report_record(report, log, total_count, total_time)
            else:
                self.create_report_record(report, log, total_count, total_time)
        sorted_report = dict(
            sorted(report.items(), key=lambda item: item[1]["time_sum"], reverse=True)
        )
        result = [{"url": url, **data} for url, data in sorted_report.items()]
        return result
