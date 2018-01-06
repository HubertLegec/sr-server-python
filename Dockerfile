FROM python:3.6

MAINTAINER Hubert Legęc <hubert.legec@gmail.com>

RUN apt-get update -y

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 4200

ENTRYPOINT ["python", "run.py"]