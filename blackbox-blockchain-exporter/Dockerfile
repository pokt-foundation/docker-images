FROM --platform=linux/amd64 python:3.10

RUN apt update && \
    apt -y dist-upgrade && \
    apt install -y --no-install-recommends \
        tzdata \
        ca-certificates && \
    rm -rf /var/cache/apt/*

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt \
    && useradd --create-home appuser

COPY ./app /app
WORKDIR /app

USER appuser
CMD ["gunicorn", "--conf", "/app/gunicorn_conf.py", "bb_exporter:app"]