import json
import logging

from fastapi import FastAPI
from fastapi.logger import logger as fastapi_logger

from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.trace import set_tracer_provider
from opentelemetry.sdk.trace import TracerProvider, sampling
from opentelemetry.sdk.trace.export import BatchSpanProcessor

import opentelemetry.instrumentation.fastapi as otel_fastapi


gunicorn_error_logger = logging.getLogger("gunicorn.error")
gunicorn_logger = logging.getLogger("gunicorn")
uvicorn_access_logger = logging.getLogger("uvicorn.access")
uvicorn_access_logger.handlers = gunicorn_error_logger.handlers
fastapi_logger.handlers = gunicorn_error_logger.handlers


def initOTel():
    merged = dict()
    for name in ["dt_metadata_e617c525669e072eebe3d0f08212e8f2.json", "/var/lib/dynatrace/enrichment/dt_metadata.json"]:
        try:
            data = ''
            with open(name) as f:
                data = json.load(f if name.startswith("/var") else open(f.read()))
                merged.update(data)
        except:
            pass

    merged.update({
        "service.name": "gunicorn-sample",
        "service.version": "1.0.0",
    })
    resource = Resource.create(merged)

    tracer_provider = TracerProvider(sampler=sampling.ALWAYS_ON, resource=resource)
    processor = BatchSpanProcessor(OTLPSpanExporter())
    tracer_provider.add_span_processor(processor)
    set_tracer_provider(tracer_provider)


initOTel()
app = FastAPI()
otel_fastapi.FastAPIInstrumentor().instrument_app(app)


@app.get("/")
async def read_root():
    return {"message": "Hello World"}


if __name__ != "__main__":
    fastapi_logger.setLevel(gunicorn_logger.level)
else:
    fastapi_logger.setLevel(logging.DEBUG)
