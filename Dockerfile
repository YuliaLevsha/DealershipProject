FROM python:3.11.1

WORKDIR /app

COPY Pipfile .
COPY Pipfile.lock .
COPY . /app/

RUN python -m pip install --upgrade pip && pip install pipenv
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --dev --system --deploy