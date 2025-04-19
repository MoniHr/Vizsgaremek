FROM python:3.11-slim-bookworm

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

# Install required system dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
  # psycopg2 dependencies
  libpq-dev \
  wget \
  # Translations dependencies
  gettext gnupg2 \
   # LDAP dependencies
  libsasl2-dev \
  python3-dev \
  libssl-dev \
  libldap2-dev \
  ldap-utils \
  libmagic1 \
  curl \
  wkhtmltopdf \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

COPY ./libs/wkhtmltopdf /usr/local/bin/wkhtmltopdf
RUN ln -sf '/usr/local/bin/wkhtmltopdf' '/usr/bin/wkhtmltopdf'

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r /requirements/production.txt \
    && rm -rf /requirements


COPY ./.compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint


COPY ./.compose/production/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start


COPY  . /app

RUN mkdir /app/staticfiles
RUN mkdir /var/log/inter_hm


ENTRYPOINT ["/entrypoint"]

