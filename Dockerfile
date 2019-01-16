FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /apacheparser
WORKDIR /apacheparser
COPY requirements.txt /apacheparser/
RUN pip install -r requirements.txt
COPY . /apacheparser/
