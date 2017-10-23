FROM python:3.6.3
LABEL maintainer="Tim Langford <tim.langford@gmail.com>"

RUN apt-get update && apt-get install -qq -y \
  build-essential libpq-dev --no-install-recommends

ENV INSTALL_PATH /memoria
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD gunicorn -b 0.0.0.0:8888 --preload --log-level debug --access-logfile - "memoria.wsgi:app"