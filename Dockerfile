FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

COPY main.py .

RUN pip install opentelemetry-distro
RUN pip install opentelemetry-exporter-otlp
RUN opentelemetry-bootstrap -a install

EXPOSE 8701

ENV OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE=delta
ENV OTEL_EXPORTER_OTLP_TRACES_PROTOCOL=http/protobuf
ENV OTEL_EXPORTER_OTLP_METRICS_PROTOCOL=http/protobuf

ENTRYPOINT opentelemetry-instrument gunicorn main:app -b=0.0.0.0:8701 -k uvicorn.workers.UvicornWorker -w 5
