FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY main.py .
EXPOSE 8701

ENV OTEL_EXPORTER_OTLP_TRACES_PROTOCOL=http/protobuf

ENTRYPOINT gunicorn main:app -b=0.0.0.0:8701 -k uvicorn.workers.UvicornWorker -w 5 --max-requests 512000 --reload
