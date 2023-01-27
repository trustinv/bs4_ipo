FROM python:3.10

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV TZ=Asia/Seoul
ENV PYTHONPATH="$PYTHONPATH:/ipo_crawler"

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  # && apt-get install -y libpq-dev \
  # mariadb dependencies
  && apt-get install -y gcc libmariadb-dev \
  # Translations dependencies
  && apt-get install -y gettext \
  # Additional dependencies
  && apt-get install -y procps telnet git vim libsndfile1\
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /ipo_crawler
COPY . .

RUN pip install -r /ipo_crawler/config/requirements/dev_requirements.txt
