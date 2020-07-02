FROM python:3.8.2-buster

WORKDIR /app
COPY . .
RUN apt-get update && \
	apt-get install -y build-essential
RUN pip3 install poetry
RUN poetry install
