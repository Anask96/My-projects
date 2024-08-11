import threading
import logging
from Storage import Storage

stop_event = threading.Event()
pause_event = threading.Event() 

DataStorage = Storage()

logging.basicConfig(
    filename='application.log',  # Log file name
    level=logging.INFO,           # Log level (e.g., INFO, DEBUG, WARNING)
    format='%(asctime)s - %(message)s',  # Format: timestamp followed by the original message
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)

def log_message(message):
    logging.info(message)