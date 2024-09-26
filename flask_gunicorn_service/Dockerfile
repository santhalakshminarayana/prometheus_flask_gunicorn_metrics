FROM python:3.12-slim-bookworm AS base

RUN apt-get update && apt-get install -y --no-install-recommends gcc

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN chmod +x run_gunicorn.sh

RUN echo $(ls -la)

EXPOSE 9200
EXPOSE 4001

ENTRYPOINT ["sh", "run_gunicorn.sh"]
