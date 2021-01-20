FROM python:3.9-slim-buster
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
COPY . ./app
RUN apt update &&\
    apt install -y libc-dev gcc bash zip htop &&\
    pip3 install -r ./app/requirements.txt
