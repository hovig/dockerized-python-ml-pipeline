FROM python:2-alpine
WORKDIR /ml
#RUN apt-get update -y
#RUN apt-get install -y python-pip python-dev build-essential
COPY requirements.txt /tmp/requirements.txt
RUN apk --update add python py-pip openssl ca-certificates py-openssl wget bash linux-headers
RUN apk --update add --virtual build-dependencies libffi-dev openssl-dev python-dev py-pip build-base \
  && pip install --upgrade pip \
  && pip install --upgrade pipenv\
  && pip install --upgrade -r /tmp/requirements.txt\
  && pip install Flask\
  && pip install pathlib\
  && apk del build-dependencies
ADD . /ml
#RUN pip install -r requirements.txt
CMD ["python", "pull_data.py", "start", "0.0.0.0:5000"]
