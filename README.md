# API Documentation

## Get the health of the API

### Request
`GET /health`

### Response
```
{
    "message": "OK"
}
```

## Create a new game

### Request

`POST /game/new`

### Response
Example:
```
{
    "message": "Attempted to create game",
    "data": {
        "gameId": "ad0e757e-fe8e-455e-8952-6c804a01cf6c",
        "snapshot": "INFO",
        "createTime": "2022-10-22 19:00:25.485054"
    }
    ...
}
```

## Get information on a single game

### Request

`GET /game/<gameId>`

### Response
Example with gameId ad0e757e-fe8e-455e-8952-6c804a01cf6c:
```
{
    "message": "Attempted to get game ad0e757e-fe8e-455e-8952-6c804a01cf6c",
    "data": {
        "Item": {
            "deleted": false,
            "complete": false,
            "lastUpdateTime": "2022-10-22 19:00:25.485054",
            "snapshot": "INFO",
            "createTime": "2022-10-22 19:00:25.485054",
            "gameId": "ad0e757e-fe8e-455e-8952-6c804a01cf6c"
        },
        ...
    }
}
```

## Upload actions to a game

### Request

`POST /game/<gameId>`

### Response
```
{
    "message": "Game ad0e757e-fe8e-455e-8952-6c804a01cf6c data registered successfully"
}
```

## Get 5 items in the table

### Request

`GET /game/all`

### Response

```
{
    "message": "Attempted get all items",
    "data": {
        "Items": [
            **Random 5 items**
        ],
        "Count": 5,
        "ScannedCount": 5,
        ...
    }
}
```