# ---------------------------------------------------------------------------
# Stage 1 — dependency installer
# ---------------------------------------------------------------------------
FROM python:3.11-slim AS builder

WORKDIR /build

# System deps required by psycopg (libpq) and cryptography
RUN apt-get update && apt-get install -y --no-install-recommends \
        libpq-dev \
        gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --prefix=/install --no-cache-dir -r requirements.txt


# ---------------------------------------------------------------------------
# Stage 2 — runtime image
# ---------------------------------------------------------------------------
FROM python:3.11-slim AS runtime

LABEL org.opencontainers.image.title="Egide HRM API"
LABEL org.opencontainers.image.description="Human Risk Management platform — backend"
LABEL org.opencontainers.image.licenses="Proprietary"

# Runtime system deps (libpq only)
RUN apt-get update && apt-get install -y --no-install-recommends \
        libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Non-root user (security hardening)
RUN groupadd --gid 1001 egide \
    && useradd --uid 1001 --gid egide --no-create-home --shell /bin/false egide

WORKDIR /app
COPY --chown=egide:egide . .

USER egide

EXPOSE 8000

# Run Alembic migrations then start uvicorn
# Use sh -c so the shell expands environment variables correctly
CMD ["sh", "-c", \
     "alembic upgrade head && \
      uvicorn app.main:app \
        --host 0.0.0.0 \
        --port 8000 \
        --workers 2 \
        --log-level info"]
