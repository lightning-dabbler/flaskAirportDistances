FROM python:3.7

EXPOSE 2004

WORKDIR /build

COPY Pipfile Pipfile.* /build/

RUN pip install --upgrade pip \
    && pip install pipenv \
    && pipenv lock --clear

RUN pipenv install --system --deploy --ignore-pipfile --skip-lock --verbose

WORKDIR /us-airport-distance-calc