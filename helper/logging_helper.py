import logging
import os
from datetime import datetime

log_filename = datetime.now().strftime("app_%Y-%m-%d_%H-%M-%S.log")
log_path = os.path.join("logs", log_filename)

logging.basicConfig(
    level=logging.INFO,  # set minimum log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(funcName)s:%(lineno)d - %(message)s',
    handlers=[
        logging.StreamHandler(),  # log to console
        logging.FileHandler(log_path, mode='a'),
    ]
)

logger = logging.getLogger(__name__)
