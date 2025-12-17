import os
import time
import logging
import psutil
from flask import Flask, jsonify

# -----------------------------
# App Configuration
# -----------------------------

APP_NAME = os.getenv("APP_NAME", "python-devops-metrics")
APP_PORT = int(os.getenv("APP_PORT", "5001"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

START_TIME = time.time()

# -----------------------------
# Logging Setup
# -----------------------------

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(APP_NAME)

# -----------------------------
# Flask App
# -----------------------------

app = Flask(__name__)

# -----------------------------
# Health Endpoint
# Used by:
# - Load balancers
# - Kubernetes
# - Monitoring tools
# -----------------------------

@app.route("/health", methods=["GET"])
def health():
    return jsonify(
        status="ok",
        service=APP_NAME
    ), 200

# -----------------------------
# Metrics Endpoint
# Used by:
# - Monitoring systems
# - Debugging
# -----------------------------

@app.route("/metrics", methods=["GET"])
def metrics():
    uptime_seconds = int(time.time() - START_TIME)

    metrics_data = {
        "cpu_percent": psutil.cpu_percent(interval=0.1),
        "memory_percent": psutil.virtual_memory().percent,
        "uptime_seconds": uptime_seconds
    }

    logger.info("Metrics requested")

    return jsonify(metrics_data), 200

# -----------------------------
# App Entry Point
# -----------------------------

if __name__ == "__main__":
    logger.info(f"Starting {APP_NAME} on port {APP_PORT}")
    app.run(host="0.0.0.0", port=APP_PORT)
