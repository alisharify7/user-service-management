#!/bin/bash

set -e

if [ "${APP}" == "celery" ]; then
    echo "🚀 Starting Celery instance..."

    LOGLEVEL="${LOGLEVEL:-DEBUG}"
    if [  "${CELERY_ROLE:-worker}" == "both"  ]; then
      celery -A <app> beat --loglevel="${LOGLEVEL}" &
    fi
    celery -A <app> worker --loglevel="${LOGLEVEL}"
else
    if [ "$DEBUG" == "1" ]; then
        # Development mode: run Django's built-in development server
        echo "🐞 Development mode detected — starting uvicorn fastapi local server"
        python app.py
    else
        # Use WORKERS from env or fallback to number of processors (or 1 if nproc fails)
        WORKERS=$( [ -n "$WORKERS" ] && echo "$WORKERS" || nproc 2>/dev/null || echo 1 )

        # Production mode: use Gunicorn as the WSGI server
        echo "🚀 Production mode — starting Gunicorn server with ${PROCESS} cpu"
        # Use exec to replace shell process with Gunicorn (avoids extra shell layer)
        exec gunicorn app:app \
            --bind 0.0.0.0:${APP_PORT:-8000} \
            --workers "${WORKERS}"
    fi
fi
