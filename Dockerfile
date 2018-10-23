FROM python
WORKDIR /ml
ADD . /ml
RUN pip install -r ml-data-pipeline/requirements.txt
EXPOSE 5000
CMD [ "python", "./pull_data.py" ]
