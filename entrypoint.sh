#!/bin/sh
set -e

# Auto-fix permissions for the data directory when started as root, then
# drop privileges to the non-root appuser. This lets a root-owned Docker
# volume be made writable by appuser on first start.
if [ "$(id -u)" = "0" ]; then
    echo "Running as root, fixing /app/data permissions..."
    mkdir -p /app/data
    chown -R appuser:appuser /app/data
    echo "Switching to appuser..."
    exec su-exec appuser "$@"
fi

# Already running as appuser
exec "$@"
