FROM python:3.8-alpine
RUN apk add git gcc musl-dev openssl-dev make  libffi-dev g++

WORKDIR /authority

COPY /v2/bot.py /authority
COPY /v2/cogs /authority/cogs
COPY /v2/requirements.txt /authority
COPY /v2/.env /authority

EXPOSE 1755

RUN pip install -r requirements.txt
CMD python3 bot.py
