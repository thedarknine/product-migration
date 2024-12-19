FROM debian:trixie-slim

ARG DEBIAN_FRONTEND=noninteractive
ARG USER=pyuser

RUN apt-get update \
    && apt-get install --no-install-recommends -y make \
        wget curl \
        python3.12 python-is-python3 \
        python3-poetry \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home $USER
USER $USER
ARG HOME="/home/$USER"
ARG PYTHON_VERSION=3.12

RUN echo "alias ll='ls -lah'" >> ~/.bashrc

WORKDIR /app

COPY . .

EXPOSE 5000

CMD ["bash"]