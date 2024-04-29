import colorlog
import logging

from src.conf.config import config

logger = logging.getLogger(f"{config.APP_NAME}")
logger.setLevel(logging.INFO)
handler = colorlog.StreamHandler()
handler.setLevel(logging.INFO)
handler.setFormatter(
    colorlog.ColoredFormatter(
        "%(yellow)s%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
)
