# gunicorn with OTel

> This is not an official Dynatrace sample,
it was created to demonstrate the usage of
OpenTelemetry Python auto-instrumentation.  
> Use it at your own risk.
---

This sample was created in order to demonstrate how
[OpenTelemetry Python auto-instrumentation](https://opentelemetry.io/docs/instrumentation/python/automatic/)
works with [Uvicorn](https://www.uvicorn.org/).

In order to send Traces to Dynatrace, you can configure the environment variables
as explained below in the `Run the container` section.

To further instructions, please check out the
[official Dynatrace documentation](https://www.dynatrace.com/support/help/extend-dynatrace/opentelemetry/walkthroughs/python).

## Build the image

```shell
docker build -t uvicorn . 
```

## Run the container

Replace `<TENANT_URL>` and `<TOKEN>` below with your tenant data
and run the command:

```shell
docker run --rm -d -p 8701:8701 --name uvicorn \
  -e OTEL_SERVICE_NAME=uvicorn-sample \
  -e OTEL_METRICS_EXPORTER=none \
  -e OTEL_EXPORTER_OTLP_TRACES_ENDPOINT=https://<TENANT_URL>/api/v2/otlp/v1/traces \
  -e OTEL_EXPORTER_OTLP_TRACES_HEADERS=Authorization=Api-Token%20<TOKEN> \
  uvicorn
```

## Access the app

The Hello World app is accessible at: <localhost:8701>.

## Access the traces

For each time you open the app, you should get a trace similar to this one:

![image](https://github.com/julianocosta89/gunicorn-with-OTel/assets/15364991/c080f50d-ae2a-482a-941f-dc2469fc6315)
