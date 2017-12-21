FROM python:3.6

MAINTAINER Hubert Legęc <hubert.legec@gmail.com>

RUN apt-get update -y

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD ["ls -la"]

ENTRYPOINT ["python"]

EXPOSE 3000

CMD ["app.py"]