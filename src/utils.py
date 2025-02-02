from typing import Dict, List

import structlog

logger = structlog.getLogger("app")


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
