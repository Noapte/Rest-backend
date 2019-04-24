FROM python:3.6-alpine

RUN mkdir /app
WORKDIR /app
RUN pip install pip==18.1 pipenv==2018.10.13

COPY Pipfile Pipfile.lock ./

RUN apk add --no-cache postgresql-libs
RUN apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev openssl-dev libffi-dev
RUN pipenv install --system --deploy
RUN apk --purge del .build-deps

ENV DOXAPI_SETTINGS=Production

COPY . ./
EXPOSE 5000

CMD uwsgi --ini uwsgi-prod.ini