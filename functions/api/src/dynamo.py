import json
from datetime import datetime
from boto3 import resource

from functions.api.src.action_parser import ActionParser


class DynamoTable:
    def __init__(self, endpoint_url, table_name):
        self.table = resource("dynamodb", endpoint_url=endpoint_url).Table(table_name)

    def get_item(self, gameId, snapshot="INFO"):
        item = self.table.get_item(Key={"gameId": gameId, "snapshot": snapshot})

        return item

    def get_all_items(self, limit=5):

        response = self.table.scan(Limit=limit)

        return response

    def put_item(self, item_definition, return_value="ALL_OLD", batch=None):

        key_schema = self.table.key_schema

        for attr in key_schema:
            name = attr.get("AttributeName")
            if not name in item_definition:
                raise RuntimeError("Not all keys in the key schema exist")

        if not batch:
            response = self.table.put_item(
                Item=item_definition, ReturnValues=return_value
            )
        else:
            response = batch.put_item(Item=item_definition)

        return response

    def upload_game(self, gameId, actions: list):

        with self.table.batch_writer() as batch:
            for action in actions:
                parser = ActionParser(action)
                item = parser.get_json_db_item(gameId)
                self.put_item(item, return_value="NONE", batch=batch)
        now = str(datetime.now())
        self.table.update_item(
            Key={"gameId": gameId, "snapshot": "INFO"},
            AttributeUpdates={
                "lastUpdateTime": {"Value": now, "Action": "PUT"},
                "complete": {"Value": True, "Action": "PUT"},
            },
        )
        return
