FROM python:3.11-slim-buster as bot_base
COPY bot_app/requirements.txt /app/bot_app/requirements.txt
COPY shared/requirements.txt /app/shared/requirements.txt

RUN apt update && apt install -y git
RUN pip install -r /app/bot_app/requirements.txt
RUN apt remove -y git && apt autoremove -y

FROM bot_base

COPY ../bot_app /app/bot_app
COPY ../shared /app/shared

WORKDIR /app/bot_app
ENV PYTHONPATH "${PYTHONPATH}:/app"