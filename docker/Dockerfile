FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 0

# Python
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install --no-install-recommends -y \
    build-essential \
    python3-dev \
    python3-pip \
    python3-setuptools \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# PostgreSQL
RUN apt-get update \
    && apt-get -y install libpq-dev gcc cmake libssl-dev \
    && pip install psycopg2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /src

ADD requirements.txt /src

RUN pip install --upgrade pip
RUN pip install -r requirements.txt