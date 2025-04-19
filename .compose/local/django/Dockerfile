# Definiáljuk a Python verziót és architektúrát
ARG PYTHON_VERSION=3.10-slim-bookworm

ARG PLATFORM=linux/amd64
FROM --platform=${PLATFORM} python:3.10-slim-bookworm as python


# Python base image alias (ARM64 és AMD64 támogatás)
# FROM --platform=linux/arm64 python:${PYTHON_VERSION} as python

# Python build stage
FROM python as python-build-stage

ARG BUILD_ENVIRONMENT=local

# Frissítjük az apt-get és telepítjük az alapcsomagokat
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        build-essential \
        libpq-dev \
        libldap2-dev \
        libsasl2-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Requirements fájlok másolása
COPY ./requirements .

# Python dependency wheel-ek létrehozása
RUN pip wheel --wheel-dir /usr/src/app/wheels -r local.txt

# Python run stage
FROM python as python-run-stage

ARG BUILD_ENVIRONMENT=local
ARG APP_HOME=/app

# Környezeti változók beállítása
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV BUILD_ENV ${BUILD_ENVIRONMENT}

WORKDIR ${APP_HOME}

# Frissítjük az apt-get és telepítjük a szükséges rendszerfüggőségeket
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev \
    gettext \
    wget \
    gnupg2 \
    libsasl2-dev \
    python3-dev \
    libssl-dev \
    libldap2-dev \
    libmagic1 \
    wkhtmltopdf \
    curl \
    netcat-openbsd \
    iputils-ping \
    net-tools \
    vim-tiny \
    procps \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


# Másoljuk a Python dependency wheel-eket a build stagről
COPY --from=python-build-stage /usr/src/app/wheels /wheels/

# Telepítjük a Python csomagokat a wheel-ekből
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
    && rm -rf /wheels/

COPY ./.compose/local/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

# Másoljuk az alkalmazás kódját a WORKDIR-be
COPY . ${APP_HOME}

# Tesztelési és debugging parancsok
RUN echo "✅ Curl telepítve: $(curl --version | head -n 1)" \
    && echo "✅ Netcat telepítve: $(nc -h 2>&1 | head -n 1)" \
    && echo "✅ Ping telepítve: $(ping -V 2>&1 | head -n 1)" \
    && echo "✅ Netstat telepítve: $(netstat -V 2>&1 | head -n 1)"

# Indítási beállítás
ENTRYPOINT ["/start"]
