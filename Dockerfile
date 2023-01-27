FROM python:3.10

ENV PYTHONUNBUFFERED 1

WORKDIR /ipo_crawler

ENV PYTHONPATH="$PYTHONPATH:/ipo_crawler"

COPY . .
RUN pip install -r /ipo_crawler/config/requirements/dev_requirements.txt
COPY start.sh /start.sh
