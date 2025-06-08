"""
Metrics Exporter

Exposes redis performance data for prometheus to scrape
"""

from prometheus_client import Gauge, generate_latest, CollectorRegistry
import redis
import os
from flask import Flask, Response

REDIS_HOST = os.getenv("REDIS_HOST", "custom-redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

my_redis = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

registry = CollectorRegistry()


# Define the Data Objects to collect

app = Flask(__name__)

telem_1 = Gauge(
    "attempted_generations", "Attempted Generations of STL files", registry=registry
)
telem_2 = Gauge(
    "successful_generations", "Successful Generations of STL files", registry=registry
)
telem_3 = Gauge(
    "failed_generations", "Failed Generations of STL files", registry=registry
)
telem_4 = Gauge("signups", "Number of signups", registry=registry)
telem_5 = Gauge("logins", "Number of Logins", registry=registry)
telem_6 = Gauge("logouts", "Number of Logouts", registry=registry)


def collect_metrics():
    """
    Refresh the metrics
    """
    keys = [
        "telem:1",
        "telem:2",
        "telem:3",
        "telem:4",
        "telem:5",
        "telem:6",
    ]
    vars = [
        telem_1,
        telem_2,
        telem_3,
        telem_4,
        telem_5,
        telem_6,
    ]

    for key, var in zip(keys, vars):
        t = my_redis.get(key)
        if t is not None:
            var.set(t)
        else:
            var.set(0)


@app.route("/metrics")
def metrics():
    collect_metrics()
    return Response(generate_latest(registry), mimetype="text/plain")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
