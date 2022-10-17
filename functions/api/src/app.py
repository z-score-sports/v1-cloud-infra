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


@app.post("/game/new")
@tracer.capture_method
def create_game():
    """
    Description : this method creates a new game entry to update

    """
    logger.info("Request POST/game")

    game_id = uuid4()
    create_time = str(datetime.now())
    snapshot = "INFO"
    item = {
        "gameId": str(game_id),
        "snapshot": snapshot,
        "createTime": create_time,
        "lastUpdateTime": create_time,
        "deleted": False,
        "complete": False,
    }

    put_item_response = TABLE.put_item(item)

    return build_response(
        200,
        {
            "message": "Attempted to create game",
            "data": {
                "gameId": str(game_id),
                "snapshot": snapshot,
                "createTime": create_time,
            },
            "info": put_item_response,
        },
    )


@app.get("/game/all")
@tracer.capture_method
def get_all():
    logger.info("Request GET/game/all")

    table_items = TABLE.get_all_items()

    return build_response(
        200, {"message": "Attempted get all items", "data": table_items}
    )


@app.get("/game/<gameId>")
@tracer.capture_method
def get_game(gameId):
    logger.info(f"Request GET/game/{gameId}")

    item = TABLE.get_item(gameId)

    return build_response(
        200, {"message": f"Attempted to get game {gameId}", "data": item}
    )


@app.post("/game/<gameId>")
@tracer.capture_method
def post_game(gameId):
    logger.info(f"Request POST/game/{gameId}")
    # TODO: Creates a random gameId, processes data, then writes to dynamo

    body: dict = app.current_event.json_body

    actions = body.get("actions", [])

    TABLE.upload_game(gameId=gameId, actions=actions)

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
