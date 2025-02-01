import logging

from config import Settings

logger = logging.getLogger(__name__)


def main():
    settings = Settings()
    logger.info(settings.config)


if __name__ == "__main__":
    main()
