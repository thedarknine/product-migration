FROM python:3.13-slim

ARG DEBIAN_FRONTEND=noninteractive
ARG USER=pyuser

RUN apt-get update \
    && apt-get install --no-install-recommends -y make \
        wget curl \
        ca-certificates \
        git \
        libssl-dev \
        zlib1g-dev \
        libbz2-dev \
        libreadline-dev \
        libsqlite3-dev \
        libpq-dev gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home $USER
USER $USER
ARG HOME="/home/$USER"

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/app/.tmp/poetry_cache

RUN rm -rf $POETRY_CACHE_DIR
RUN echo "alias ll='ls -lah'" >> ~/.bashrc

WORKDIR /app

COPY . .

RUN pip install poetry && echo "Poetry installed"
ENV PATH="/home/pyuser/.local/bin:$PATH"

CMD ["bash"]