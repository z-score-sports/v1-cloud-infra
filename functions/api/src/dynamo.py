import json
from datetime import datetime
from boto3 import resource


class DynamoTable:
    def __init__(self, endpoint_url, table_name):
        self.table = resource("dynamodb", endpoint_url=endpoint_url).Table(table_name)

    def get_item(self, gameId, snapshot="INFO"):
        item = self.table.get_item(Key={"gameId": gameId, "snapshot": snapshot})

        return item

    def get_all_items(self, limit=5):

        response = self.table.scan(Limit=limit)

        return response

    def put_item(self, item_definition):

        key_schema = self.table.key_schema

        for attr in key_schema:
            name = attr.get("AttributeName")
            if not name in item_definition:
                raise Exception("Not all keys in the key schema exist")

        response = self.table.put_item(Item=item_definition, ReturnValues="ALL_OLD")

        return response

    def upload_game(self, req_body):
        # TODO:

        # This is a batch writer for dynamodb
        # with self.table.batch_writer() as batch:
        #     for _ in range(1000000):
        #         batch.put_item(Item={'HashKey': '...',
        #                             'Otherstuff': '...'})
        #     # You can also delete_items in a batch.
        #     batch.delete_item(Key={'HashKey': 'SomeHashKey'})

        return
