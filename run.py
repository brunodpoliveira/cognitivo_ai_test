import logging
from os import environ
from app import app

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting API...")
    SERVER_HOST = environ.get('SERVER_HOST', 'localhost')
    app.run(host=SERVER_HOST, port=5500, debug=(not environ.get('ENV') == 'PRODUCTION'), threaded=True)
