from typing import Any, Dict, Generator, List


class Reporter:

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

    def make_report_data(self, nginx_logs: Generator[List[str], None, None]):
        """Make report data"""
        report: Dict[str, Any] = {}

        total_request_count: int = 0
        total_request_time: float = 0.0

        for request in nginx_logs:
            request_url = request[7]
            request_time = float(request[-1])

            total_request_count += 1
            total_request_time += request_time

            if not report.get(request_url):
                count = 1
                count_perc = (count / total_request_count) * 100
                time_sum = time_max = time_avg = request_time
                time_list = [request_time]
                time_med = self.get_median(time_list)
                time_perc = (time_sum / total_request_time) * 100
                report[request_url] = {
                    "count": count,
                    "count_perc": count_perc,
                    "time_sum": time_sum,
                    "time_max": time_max,
                    "time_list": time_list,
                    "time_med": time_med,
                    "time_avg": time_avg,
                    "time_perc": time_perc,
                }
            else:
                report[request_url]["count"] += 1
                report[request_url]["count_perc"] = (
                    report[request_url]["count"] / total_request_count * 100
                )
                report[request_url]["time_sum"] += request_time
                if request_time > report[request_url]["time_max"]:
                    report[request_url]["time_max"] = request_time
                report[request_url]["time_list"].append(request_time)
                report[request_url]["time_med"] = self.get_median(
                    report[request_url]["time_list"]
                )
                report[request_url]["time_avg"] = (
                    report[request_url]["time_sum"] / report[request_url]["count"]
                )
                report[request_url]["time_perc"] = (
                    report[request_url]["time_sum"] / total_request_time * 100
                )
        return report
