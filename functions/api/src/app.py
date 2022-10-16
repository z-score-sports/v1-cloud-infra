import os
from datetime import datetime
from uuid import uuid4

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.middleware_factory import lambda_handler_decorator
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.event_handler.exceptions import NotFoundError

from functions.api.src.dynamo import DynamoTable
from functions.api.src.response_utils import build_response

tracer = Tracer()
app = APIGatewayRestResolver()
logger = Logger(
    level=os.environ.get("LOG_LEVEL", "INFO"),
    service=os.environ.get("POWERTOOLS_SERVICE_NAME", "DBInterfaceApi"),
)

TABLE = DynamoTable("http://host.docker.internal:8000", "DevTable")

@app.not_found
@tracer.capture_method
def not_found(ex: NotFoundError):
    method = app.current_event.http_method
    path = app.current_event.path
    return build_response(404, {"message": f"Route {method} {path} not found"})


@app.get("/health")
def health():
    return build_response(200, {"message": "OK"})


@app.post("/game")
@tracer.capture_method
def create_game():
    logger.info("Request POST/game")

    game_id = uuid4()
    test_item = {
            "gameId": str(game_id),
            "snapshot": "INFO",
            "createTime": str(datetime.now()),
            "deleted": False
        }

    put_item_response = TABLE.put_item(test_item)

    return build_response(200, {"message": "Attempted to create game", "data": put_item_response})


@app.get("/game/all")
@tracer.capture_method
def get_all():
    logger.info("Request GET/game/all")

    table_items = TABLE.get_all_items()

    return build_response(200, {"message": "Attempted get all items", "data": table_items})
    
@app.get("/game/<gameId>")
@tracer.capture_method
def get_game(gameId):
    logger.info(f"Request GET/game/{gameId}")

    return build_response(200, {"message": f"Attempted to get game {gameId}"})

@app.post("/game/<gameId>")
@tracer.capture_method
def post_game(gameId):
    logger.info(f"Request POST/game/{gameId}")
    # TODO: Creates a random gameId, processes data, then writes to dynamo

    return build_response(
        200, {"message": f"Game {gameId} data registered successfully"}
    )


@lambda_handler_decorator
def middleware(handler, event, context: LambdaContext):


    ip_address = event.get("headers", {}).get("X-Forwarded-For", "UNK")
    logger.append_keys(ip_address=ip_address)

    handler_return = handler(event, context)

    return handler_return


@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST)
@tracer.capture_lambda_handler
@middleware
def lambda_handler(event, context: LambdaContext):

    return app.resolve(event, context)
