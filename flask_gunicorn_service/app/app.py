from flask import Flask
import random
import time

from app.metrics.flask_prometheus_metrics import FlaskPrometheusMetrics


app = Flask(__name__)

@app.get("/fetch")
def fetch():
    time.sleep(random.randint(1, 4))
    return "200"

@app.get("/select/<item_no>")
def select_item(item_no):
    time.sleep(random.randint(1, 4))
    return "200"

@app.post("/update_item/<int:item_no>/type_no/<int:type_no>")
def update_item(item_no, type_no):
    time.sleep(random.randint(1, 4))
    return "200"

@app.put("/update_item/<int:item_no>/type_no/<int:type_no>")
def insert_item(item_no, type_no):
    time.sleep(random.randint(1, 4))
    return "200"

@app.delete("/update_item/<int:item_no>/type_no/<int:type_no>")
def delete_item(item_no, type_no):
    time.sleep(random.randint(1, 4))
    return "200"

# NOTE: This should be initialized at the end of all endpoints definition
FlaskPrometheusMetrics.initialize(app=app)
