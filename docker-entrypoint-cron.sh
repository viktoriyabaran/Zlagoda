#!/bin/sh
set -e

printenv \
  | grep -E '^(DATABASE_URL|POSTGRES_|SECRET_KEY|DEBUG|ALLOWED_HOSTS|CSRF_TRUSTED_ORIGINS|DJANGO_|TZ)[A-Z0-9_]*=' \
  > /app/.env || true

exec cron -f
