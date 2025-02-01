FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential tree curl git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /src

COPY ./src .

RUN pip install poetry==2.0.1 && curl -s https://pyenv.run | bash

CMD ["python3", "main.py"]
