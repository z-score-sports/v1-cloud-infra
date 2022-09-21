from distutils.command.build import build
import os

import boto3
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.middleware_factory import lambda_handler_decorator
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.event_handler.exceptions import NotFoundError


from functions.api.src.response_utils import build_response

tracer = Tracer()
app = APIGatewayRestResolver()
logger = Logger(
    level=os.environ.get("LOG_LEVEL", "INFO"),
    service=os.environ.get("POWERTOOLS_SERVICE_NAME", "DBInterfaceApi"),
)


@lambda_handler_decorator
def middleware(handler, event, context: LambdaContext):

    ip_address = event.get("headers", {}).get("X-Forwarded-For", "UNK")
    logger.append_keys(ip_address=ip_address)

    handler_return = handler(event, context)

    return handler_return


@app.not_found
@tracer.capture_method
def not_found(ex: NotFoundError):
    method = app.current_event.http_method
    path = app.current_event.path
    return build_response(404, {"message": f"Route {method} {path} not found"})


@app.get("/health")
def health():
    return build_response(200, {"message": "Healthy"})


@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST)
@tracer.capture_lambda_handler
@middleware
def lambda_handler(event, context: LambdaContext):
    logger.info("App Called")

    return app.resolve(event, context)
