FROM python:3.10

ENV POETRY_VERSION=1.1.13
WORKDIR /app

COPY requirements.txt .
RUN python3 -m pip install --no-cache -r requirements.txt

COPY . .

ENTRYPOINT ["sh", "entrypoint.sh"]