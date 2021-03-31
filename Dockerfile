FROM python:3.6.8-alpine

LABEL Image for running the flask application

# Change this to the correct directory on the local machine
WORKDIR ~/Desktop/Projects/rotation_bot

COPY . .

RUN ["pip3", "install", "pipenv"]

RUN ["pipenv", "install"]

CMD pipenv run flask run
