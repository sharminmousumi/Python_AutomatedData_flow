import logging
import os

def setup_logger():
    # Create logs folder if it doesn't exist
    if not os.path.exists("logs"):
        os.makedirs("logs")

    logging.basicConfig(
        filename='logs/app.log',
        level=logging.INFO,
        format='%(asctime)s %(levelname)s:%(message)s' 
    )

    #Returns a logger object
    return logging.getLogger()
