from bottle import get, run, response
import json

users = {
    "12345": {"id": "1", "email": "@a", "token": "12345"},
    "67890": {"id": "2", "email": "@b", "token": "67890"}
}

messages = {
    "1": [
        {"id": "26b43fa3-e7e9-49c7-a273-e8f940b6c7d2",
            "message": "m1", "access": "*"},
        {"id": "34e8cd09-16fa-4bc9-9166-166e4edadb53",
            "message": "m2", "access": "*"},
        {"id": "0b01567b-3ba4-4974-9f2f-3d70ae7a34e6",
            "message": "m3", "access": "*"},
        {"id": "8617b576-a97b-4d4f-b661-b93b96075548",
            "message": "m4", "access": "*"}
    ]
}

########################################


@get("/provider/<id>/from/<last_message_id>/limit/<limit:int>/token/<token>")
def _(id, last_message_id, limit, token):
    try:
        # Validation
        if limit == 0:
            raise Exception("limit cannot be zero")
        # Validate that the token is registered in the system
        if token not in users:
            raise Exception("token is not valid")
        # print(json.dumps(messages[id][3]))
        for i in messages[id]:
            if last_message_id in messages[id][i]:
                print(json.dumps(messages[id][i]))
        response.content_type = "application/json"
        return json.dumps(messages[id][:limit])
    except Exception as ex:
        response.status = 400
        return str(ex) + "lol"


########################################
run(host="127.0.0.1", port=3000, debug=True, reloader=True)
