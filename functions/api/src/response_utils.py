import json

from aws_lambda_powertools.event_handler.api_gateway import Response
from aws_lambda_powertools.event_handler import content_types


def build_response(status_code: int, body: dict):

    return Response(
        status_code=status_code, content_type=content_types.APPLICATION_JSON, body=body
    )
