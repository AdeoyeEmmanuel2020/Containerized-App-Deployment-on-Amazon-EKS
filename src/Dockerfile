FROM python:3.12.12-slim

LABEL org.opencontainers.image.title="EKS reference service" \
      org.opencontainers.image.description="Hardened stateless workload for Kubernetes assurance experiments" \
      org.opencontainers.image.source="https://github.com/AdeoyeEmmanuel2020/Containerized-App-Deployment-on-Amazon-EKS"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8080

WORKDIR /app
RUN groupadd --gid 10001 app && useradd --uid 10001 --gid app --no-create-home app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir --requirement requirements.txt
COPY --chown=10001:10001 app.py ./

USER 10001:10001
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/health/live', timeout=2)"]

ENTRYPOINT ["gunicorn"]
CMD ["--bind=0.0.0.0:8080", "--workers=2", "--threads=2", "--timeout=30", "--access-logfile=-", "--error-logfile=-", "app:app"]
