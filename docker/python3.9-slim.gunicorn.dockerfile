FROM tiangolo/uvicorn-gunicorn:python3.9-slim

ARG REQUIREMENTS_FILE=${REQUIREMENTS_FILE:-"REQUIREMENTS_FILE NOT SET"}

# set work directory
WORKDIR /app

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements*.txt .
RUN pip install --no-cache-dir -r ${REQUIREMENTS_FILE}

COPY ./app /app

ENTRYPOINT [ "docker/entrypoints/entrypoint.sh" ]
