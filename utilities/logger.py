import logging
import os

os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("Automation")
logger.setLevel(logging.INFO)

if not logger.handlers:

    file_handler = logging.FileHandler("logs/automation.log", mode="w")
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)