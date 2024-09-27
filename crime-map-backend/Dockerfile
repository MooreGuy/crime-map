FROM python:3.8-buster

WORKDIR /usr/share/crime-map/

RUN apt-get update && apt-get install -y pipenv && apt-get clean

COPY ./Pipfile* /usr/share/crime-map/
RUN pipenv install

COPY ./ /usr/share/crime-map/

CMD pipenv run uwsgi --py-autoreload 1 --socket 0.0.0.0:5000 --protocol=http -w wsgi:app
