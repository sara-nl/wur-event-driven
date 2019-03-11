FROM python:3.7.2-alpine3.9

WORKDIR /usr/src/app

COPY requirements.txt .
# We need to add some dependencies to the base image for the requirements.
# See https://stackoverflow.com/questions/45028650/docker-image-with-python-alpine-failure-due-missing-compiler-error
RUN apk add --no-cache --virtual .py_deps build-base python3-dev libffi-dev libressl-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    # remove the dependancies again
    apk del .py_deps 

COPY . .

CMD [ "python", "./app.py" ]
