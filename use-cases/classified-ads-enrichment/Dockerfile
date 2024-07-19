FROM python:3.12-slim

ADD requirements.txt /python/src/
WORKDIR /python/src/
RUN pip3 install -r requirements.txt

ADD consumer.py /python/src/

CMD [ "python", "/python/src/consumer.py" ]