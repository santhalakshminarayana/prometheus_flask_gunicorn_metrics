from flask import Flask
import logging

from prometheus_flask_exporter.multiprocess import GunicornPrometheusMetrics


class FlaskPrometheusMetrics:
    @classmethod
    def initialize(cls, app: Flask):
        try:
            logging.debug(f"initiating prometheus metrics")
            p = cls(app)
            p.initialize_custom_metrics()
        except Exception as e:
            logging.error(f"error initiating prometheus metrics: {e}")

    def __init__(self, app: Flask): 
        self.metrics = GunicornPrometheusMetrics(app)
        self.metrics.info('flask_prometheus_metrics', 'Metrics')

    def initialize_custom_metrics(self):
        pass
