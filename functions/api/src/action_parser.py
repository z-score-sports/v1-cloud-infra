class ActionParser:
    def __init__(self, action_json) -> None:
        self.action = action_json

    def get_property(self, property):
        return self.action.get(property, None)

    def get_json_db_item(self, gameId):

        item = {
            "gameId": gameId,
            "snapshot": self.property("snapshot"),
            "type": self.get_property("type"),
            "subtype": self.get_property("subtype"),
            "detail": self.get_property("detail"),
            "home_lineup": self.get_property("home_lineup"),
            "away_lineup": self.get_property("away_lineup"),
            "gametime": self.get_property("gametime"),
        }

        ret_item = {k: v for k, v in item.items() if v is not None}

        return ret_item
