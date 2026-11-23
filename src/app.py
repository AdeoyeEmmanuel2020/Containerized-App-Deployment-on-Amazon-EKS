"""Minimal stateless service used to exercise Kubernetes workload controls."""

from datetime import datetime, timezone
import os
import socket

from flask import Flask, jsonify


def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/")
    def index():
        return jsonify(
            application="eks-reference-service",
            version=os.getenv("APP_VERSION", "development"),
            environment=os.getenv("ENVIRONMENT", "development"),
            hostname=socket.gethostname(),
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

    @app.get("/health/live")
    def live():
        return jsonify(status="alive"), 200

    @app.get("/health/ready")
    def ready():
        if os.path.exists("/tmp/not-ready"):
            return jsonify(status="not-ready"), 503
        return jsonify(status="ready"), 200

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")), debug=False)
