FROM python:3.8.2

WORKDIR /usr/src/foodgram_project

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY entrypoint.sh .

COPY . .

ENTRYPOINT ["/usr/src/foodgram_project/entrypoint.sh"]