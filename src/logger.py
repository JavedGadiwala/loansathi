import logging
import sys
from pathlib import Path
from datetime import datetime

LOGS_DIR = Path(__file__).parent.parent / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOGS_DIR / f"loansathi_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if logger.handlers:
        return logger
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(name)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(name)s [%(filename)s:%(lineno)d]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    return logger

root_logger = setup_logger('loansathi')
