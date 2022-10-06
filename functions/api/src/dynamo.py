class DB:

    def __init__(self, resource, table_name):

        self.table = resource.Table(table_name)
        

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
        

