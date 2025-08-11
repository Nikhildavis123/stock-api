import logging
import os
from datetime import datetime


log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

today = datetime.now().strftime("%Y-%m-%d")
log_filename = os.path.join(log_dir, f"log_{today}.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_filename, mode='a'),
        logging.StreamHandler()  # also print to console
    ]
)

logger = logging.getLogger("stock-api")
