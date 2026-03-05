# =========================
# Base image
# =========================
FROM python:3.10-slim

# =========================
# Environment settings
# =========================
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# =========================
# System dependencies
# =========================
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libgl1 \
    libglib2.0-0 \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH="/root/.cargo/bin:/root/.local/bin:${PATH}"

# =========================
# Working directory
# =========================
WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev

# =========================
# Copy source code
# =========================
COPY . .

# =========================
# Expose API port
# =========================
EXPOSE 8000

# =========================
# Run FastAPI app
# =========================
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]