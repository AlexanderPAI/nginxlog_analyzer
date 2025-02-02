import os.path
import sys
from typing import List

import structlog

from src.analyzer import NginxLogAnalyzer
from src.config import Settings
from src.reporter import Reporter
from src.utils import parse_args

logger = structlog.getLogger(__name__)


def check_success(file: str) -> None:
    """Check creating report file"""
    if os.path.isfile(file):
        logger.info("Report File is done.")
    else:
        logger.info(f"Something went wrong. Failed to create {file}")


def main(args: List):
    """Main app func"""
    # Load args and init settings
    valid_args = parse_args(args)
    settings = Settings(config_file_path=valid_args.get("--config", None))

    # Init nginx_analyzer
    nginx_analyzer = NginxLogAnalyzer(settings)

    # Get and check last log file
    last_log_file = nginx_analyzer.find_last_nginx_log_file()
    if not last_log_file:
        logger.error(f"The logs were not found at {last_log_file}")
        sys.exit()
    logger.info(f"Last Nginx Log File: {last_log_file}")

    # Prepare logs generator
    nginx_logs = nginx_analyzer.get_nginx_logs(last_log_file)

    # Init reporter
    reporter = Reporter(settings, last_log_file=last_log_file)

    # Check if this work has already been done
    if reporter.check_report_exist():
        logger.info(f"Report for {last_log_file} is exist already")
        sys.exit()
    logger.info(f"Report File: {reporter.report_file}")

    # Prepare report data and render report
    report_data = reporter.make_report_data(nginx_logs)
    reporter.render_report(report_data=report_data)

    # Check if report file has been done
    check_success(reporter.report_file)


if __name__ == "__main__":
    main(sys.argv)
