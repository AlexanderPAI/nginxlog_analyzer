import os.path
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
    """Main app func"""
    valid_args = parse_args(args)
    settings = Settings(config_file_path=valid_args.get("--config", None))

    nginx_analyzer = NginxLogAnalyzer(settings)
    last_log_file = nginx_analyzer.find_last_nginx_log_file()
    if not last_log_file:
        sys.exit()
    logs = nginx_analyzer.get_nginx_logs(last_log_file)
    logger.info(f"Last Nginx Log File: {last_log_file}")

    reporter = Reporter(settings, last_log_file=last_log_file)
    logger.info(f"Report File: {reporter.report_file}")

    start_time = time.time()
    logger.info(f"Log Analyzer starts: {start_time}")

    report_data = reporter.make_report_data(logs)
    reporter.render_report(report_data=report_data)
    end_time = time.time()
    logger.info(f"Finished at: {end_time}")
    logger.info(f"The analyzer worked in {end_time - start_time}")

    if os.path.isfile(reporter.report_file):
        logger.info("Report File is done.")
    else:
        logger.info(f"Something went wrong. Failed to create {reporter.report_file}")


if __name__ == "__main__":
    main(sys.argv)
