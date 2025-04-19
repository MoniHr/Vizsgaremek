FROM python:3.10

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements/local.txt

CMD ["celery", "-A", "config", "worker", "--loglevel=info"]
