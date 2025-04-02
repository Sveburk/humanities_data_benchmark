import os
import time
import logging

# Ensure the logs directory exists
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s:%(name)s:%(message)s",
    handlers=[
        logging.FileHandler(f"{log_dir}/{time.strftime('%Y%m%d-%H%M%S')}.log"),
        logging.StreamHandler(),
    ]
)

logger = logging.getLogger(__name__)