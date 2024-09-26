from pathlib import Path

import logging
import os

from dotenv import load_dotenv

load_dotenv()

# IMPORTANT: This should be imported after all the environemntal variables
from prometheus_flask_exporter.multiprocess import GunicornPrometheusMetrics


bind = "0.0.0.0:4001"
workers = 4
worker_class = "gevent"
reload = True
reload_engine = "poll"
loglevel = "DEBUG"
accesslog = "-"
errorlog = "-"
# Set the keep-alive timeout in seconds
keepalive = 5

logconfig_dict = {
    "formatters": {
        "default": {
            "format": "%(asctime)s [%(levelname)s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": loglevel,
        },
        "null": {"class": "logging.NullHandler"},
    },
    "loggers": {
        "gunicorn.error": {
            "level": loglevel,
            "propagate": False,
            "handlers": ["console"],
        },
    },
}

def clean_old_prometheus_logs(path):
    for filename in os.listdir(path):
        if filename.endswith("db"):
            try:
                os.remove(os.path.join(path, filename))
            except Exception as e:
                logging.error(
                    f"error deleting file {os.path.join(path, filename)}: {e}"
                )

def on_starting(server):
    try:
        if os.getenv("PROMETHEUS_MULTIPROC_DIR") is None:
            raise ValueError(
                "PROMETHEUS_MULTIPROC_DIR environment variable not found"
            )
        prometheus_dir = os.getenv("PROMETHEUS_MULTIPROC_DIR")
        dct = Path(prometheus_dir)
        if not dct.exists():
            dct.mkdir(parents=True, exist_ok=True)
        clean_old_prometheus_logs(prometheus_dir)
    except Exception as e:
        logging.error(f"error setting up prometheus logs directory on start: {e}")

def when_ready(server):
    try:
        if os.getenv("PROMETHEUS_METRICS_PORT") is None:
            raise ValueError(
                "PROMETHEUS_METRICS_PORT environment variable not found"
            )
        GunicornPrometheusMetrics.start_http_server_when_ready(
            int(os.getenv("PROMETHEUS_METRICS_PORT"))
        )
    except Exception as e:
        logging.error(f"error initializing the prometheus metrics: {e}")


def child_exit(server, worker):
        try:
            GunicornPrometheusMetrics.mark_process_dead_on_child_exit(worker.pid)
        except Exception as e:
            logging.error(f"error exiting the child for prometheus: {e}")
