# syntax=docker/dockerfile:1
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

WORKDIR /app

# Install dependencies first so this layer stays cached across code-only changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application
COPY . .

# Run as a non-root user, with a dedicated writable directory for
# app_config.json, the saved knowledge graph, and pyvis's graph.html —
# all of which the app currently writes as plain relative paths.
RUN useradd --create-home --uid 1000 appuser \
    && mkdir -p /data \
    && chown -R appuser:appuser /app /data

USER appuser

# Making /data the working directory at container start means every
# relative file the app writes lands in the mounted volume instead of
# disappearing when the container is removed or rebuilt.
WORKDIR /data

EXPOSE 8501

# Uses Python's stdlib instead of curl/wget, so no extra packages are needed
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request as u; u.urlopen('http://localhost:8501/_stcore/health')" || exit 1

# main.py's subprocess wrapper exists to launch a local browser tab on your
# own machine — not useful inside a container, so Streamlit is invoked
# directly against the app entry point instead.
CMD ["streamlit", "run", "/app/app/app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true"]
