FROM ubuntu:latest
MAINTAINER Ohannes (Hovig) Ohannessian

#install dependencies for python
RUN apt-get -yqq update
RUN apt-get -yqq install python-pip python-dev curl gnupg

#add app to folder, fetch dependencies
WORKDIR /opt/ml-data-pipeline
ADD ml-data-pipeline /opt/ml-data-pipeline
RUN pip install -r requirements.txt

#expose port, start app
EXPOSE 5000
CMD [ "python", "./pull_data.py" ]
