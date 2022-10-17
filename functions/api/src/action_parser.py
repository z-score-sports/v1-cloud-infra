class ActionParser:
    def __init__(self, action_json) -> None:
        self.action = action_json

    def get_snapshot_key(self):
        return self.action.get("playIndex", None)

    def get_action_type(self):
        return self.action.get("type", None)

    def get_action_subtype(self):
        return self.action.get("subtype", None)

    def get_action_detail(self):
        return self.action.get("detail", None)

    def get_home_lineup(self):
        return self.action.get("home_lineup", [])

    def get_away_lineup(self):
        return self.action.get("away_lineup", [])

    def get_gametime(self):
        return self.action.get("gametime", None)

    def get_json_db_item(self, game_id):

        item = {
            "gameId": game_id,
            "snapshot": self.get_snapshot_key(),
            "type": self.get_action_type(),
            "subtype": self.get_action_subtype(),
            "detail": self.get_action_detail(),
            "home_lineup": self.get_home_lineup(),
            "away_lineup": self.get_away_lineup(),
            "gametime": self.get_gametime(),
        }

        ret_item = {k: v for k, v in item.items() if v is not None}

        return ret_item
