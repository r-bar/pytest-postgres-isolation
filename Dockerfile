FROM python:3.11

RUN pip install poetry

WORKDIR /dbtest

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root

COPY dbtest tests ./
RUN poetry install

ENTRYPOINT ["poetry", "run", "-q", "--"]
