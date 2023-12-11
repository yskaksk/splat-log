FROM python:3.11-slim

WORKDIR /app

EXPOSE 7860

COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt --cache-dir /pip-cache && \
    rm -rf /pip-cache

ENV GRADIO_ANALYTICS_ENABLED=false

COPY . .

CMD uvicorn --host 0.0.0.0 --port 8000 main:app
