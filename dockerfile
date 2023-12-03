###########
# BUILDER #
###########

FROM python:3.11.6-alpine3.18 as builder

# set work directory
WORKDIR /usr/src/asvetabot

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add gcc python3-dev musl-dev linux-headers

# lint
RUN pip install --upgrade pip
COPY . .

# install dependencies
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/asvetabot/wheels -r requirements.txt

#########
# FINAL #
#########

# pull official base image
FROM python:3.11.6-alpine3.18

# create directory for the app
RUN mkdir -p /home

# create the appropriate directories
ENV HOME=/home
ENV APP_HOME=/home/asvetabot
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# install dependencies
RUN apk update && apk add libpq
COPY --from=builder /usr/src/asvetabot/wheels /wheels
COPY --from=builder /usr/src/asvetabot/requirements.txt .
RUN pip install --no-cache /wheels/*

# copy project
COPY . $APP_HOME