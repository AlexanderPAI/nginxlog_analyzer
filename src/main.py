import json
import sys
import time
from typing import Dict, List

import structlog

from src.analyzer import NginxLogAnalyzer
from src.config import Settings
from src.reporter import Reporter

logger = structlog.getLogger(__name__)


def parse_args(args: List) -> Dict:
    """Parse valid args from console"""
    valid_args_list = [
        "--config",
    ]
    valid_args_received = {}

    for arg in args[1:]:
        if arg.count("=") != 1:
            logger.error(
                f"Argument {arg} - an invalid console argument or syntax error"
            )
        key, value = arg.split("=", 1)
        if key in valid_args_list:
            valid_args_received[key] = value
    return valid_args_received


def main(args):
    start_time = time.time()

    valid_args = parse_args(args)
    settings = Settings(config_file_path=valid_args.get("--config", None))
    nginx_analyzer = NginxLogAnalyzer(settings)
    reporter = Reporter()

    last_log = nginx_analyzer.find_last_nginx_log_file(settings.config["LOG_DIR"])
    logs = nginx_analyzer.get_nginx_logs(last_log)
    report = reporter.make_report_data(logs)

    end_time = time.time()

    print(f"Time: {end_time - start_time}")

    with open("test_report.json", "w", encoding="utf-8") as file:
        json.dump(report, file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main(sys.argv)
