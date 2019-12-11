FROM python:3.7.5-slim-buster

WORKDIR /usr/src/thethe/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/thethe/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY server /usr/src/thethe/server
COPY tasks /usr/src/thethe/tasks

CMD ["gunicorn", "-b 0.0.0.0:8000", "server.main:app"]
