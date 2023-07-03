import logging

import uvicorn

from src.core.logger import LOGGING
from src.main import create_app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_config=LOGGING, log_level=logging.DEBUG)
