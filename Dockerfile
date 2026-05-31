FROM python:3.12-alpine

WORKDIR /app

# System deps:
# - tzdata / ca-certificates: correct time + TLS for Telegram MTProto
# - su-exec: drop privileges from root to appuser in the entrypoint
RUN apk add --no-cache tzdata ca-certificates su-exec

# Install Python dependencies first for better layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Application code
COPY Code/ ./Code/
COPY entrypoint.sh /entrypoint.sh

# Make entrypoint executable and create the non-root user
RUN chmod +x /entrypoint.sh && \
    addgroup -g 1000 appuser && \
    adduser -D -u 1000 -G appuser appuser && \
    chown -R appuser:appuser /app

# Don't set USER here: the entrypoint starts as root to fix volume
# permissions, then drops to appuser via su-exec.

# Reserved for a future health/web endpoint (see Traefik labels in compose)
EXPOSE 8080

ENTRYPOINT ["/entrypoint.sh"]
CMD ["python", "-u", "Code/index.py"]
