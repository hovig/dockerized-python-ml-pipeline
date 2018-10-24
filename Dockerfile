FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
RUN pip install Flask 
RUN pip install pathlib
WORKDIR /ml
ADD . /ml
RUN pip install -r requirements.txt
