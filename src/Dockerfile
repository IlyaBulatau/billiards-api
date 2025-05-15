FROM python:3.12.9-slim-bullseye as builder

ENV \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PATH="/root/.local/bin/:$PATH"

RUN apt-get update && apt-get install --no-install-recommends --no-install-suggests -y \
    gcc \
    python3-dev \
    curl \
    libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ADD https://astral.sh/uv/install.sh /uv-installer.sh

RUN sh /uv-installer.sh && rm /uv-installer.sh

COPY --from=ghcr.io/astral-sh/uv:0.7.3 /uv /uvx /bin/

WORKDIR /opt/app

COPY ./pyproject.toml ./uv.lock  ./

COPY ./src .

RUN bash -c "uv pip install --system -r <(uv pip compile pyproject.toml)"

# ---------- development -------------
FROM builder as development

WORKDIR /opt/app

RUN uv sync --group dev

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
