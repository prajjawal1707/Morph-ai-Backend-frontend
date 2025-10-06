import logging

logging.basicConfig(level=logging.INFO)

def log_upload(filename: str):
    logging.info(f"File uploaded: {filename}")
