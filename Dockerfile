FROM python:latest

WORKDIR /usr/app/src
COPY messenger.py ./
RUN python3 -m pip install paho-mqtt python-telegram-bot

CMD [ "python", "./messenger.py"]