import logging
import sys
from typing import Dict, List

from src.config import Settings

logger = logging.getLogger(__name__)


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
    valid_args = parse_args(args)
    settings = Settings(config_file_path=valid_args.get("--config", None))
    logger.info(settings.config_file_path)
    logger.info(settings.config)


if __name__ == "__main__":
    main(sys.argv)
