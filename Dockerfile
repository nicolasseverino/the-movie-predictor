FROM python:3.7-alpine

RUN pip install argparse mysql-connector-python beautifulsoup4 requests

COPY . /usr/src/themoviepredictor

CMD python /usr/src/themoviepredictor/app.py movies import --api themoviedb --imdb_id tt3896198