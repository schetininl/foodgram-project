FROM python:3.8.2

WORKDIR /usr/src/foodgram_project

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

RUN mkdir -p /home/app

ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static
RUN mkdir $APP_HOME/media
WORKDIR $APP_HOME

COPY entrypoint.sh $APP_HOME

COPY . $APP_HOME

