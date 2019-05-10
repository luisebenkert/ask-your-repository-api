""" Entry point for our application """
import logging
from application.custom_loggers import setup_file_logger
from application import create_app
from application.extensions import socketio

# Call the Application Factory function to construct a Flask application instance
# using the standard configuration defined in /instance/flask.cfg
app = create_app("development_config.cfg")  # pylint: disable=invalid-name

setup_file_logger(
    name="query_logger",
    filename=app.config["QUERY_LOG_FILE_PATH"],
    format="%(asctime)s user: %(user)s, query: %(message)s",
)

if __name__ != "__main__":
    gunicorn_logger = logging.getLogger("gunicorn.error")  # pylint: disable=invalid-name
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)  # pylint: disable=no-member

if __name__ == "__main__":
    socketio.run(host="0.0.0.0")  # pylint: disable=no-value-for-parameter
