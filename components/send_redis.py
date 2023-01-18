import redis
from bottle import get, post, run, request
from redis.commands.json.path import Path
import json
import xmltodict
from xml.etree import ElementTree
from json2xml import json2xml
from json2xml.utils import readfromstring

r = redis.Redis(
host='127.0.0.1',
port=6379,
password='',
decode_responses=True)

# client = redis.Redis(host='127.0.0.1', port=6379, db=0)

# some_json = {
#      'one': "yes1",
#      'two': 2
#    }

# client.json().set('somejson:1', Path, some_json)

# try:
#     # decode_responses=True converts bytes to string
#     r = redis.Redis(
#         host='127.0.0.1',
#         port=6379,
#         password='',
#         decode_responses=True
#     )

#     r.set('foo', "1")
#     value = r.get('foo')
#     print(type(value))
# except Exception as ex:
#     print(ex)


# @post("/test/topic/<topic>")
# def _(topic):
#     try:
#         r.delete(topic)
#         return ("Deleted")
#     except Exception as ex:
#         print(ex)



@get("/delete-message/topic/<topic>")
def _(topic):
    try:
        r.delete(topic)
        return ("Deleted")
    except Exception as ex:
        print(ex)


@post("/create-message/topic/<topic>")
def _(topic):
    # decode_responses=True converts bytes to string
    if (request.headers.get('Content-Type') == "application/json"):
        data = json.load(request.body)
        # print(data)
        print(request.headers.get('Content-Type'))

        try:
            r.set(topic, json.dumps(data))
            r.expire(topic, 600)
            return ("OK JSON")

        except Exception as ex:
            print(ex)
    else:
        data = ElementTree.fromstring(request.body.read())
        print(request.headers.get('Content-Type'))

        try:
            r.set(topic, request.body.read())
            r.expire(topic, 600)
            return ("OK XML")

        except Exception as ex:
            print(ex)



@get("/get-message/topic/<topic>/format/<format1>")
def _(topic, format1):

    def isXml(value):
        try:
            ElementTree.fromstring(value)
        except ElementTree.ParseError:
            return False
        return True    

    if format1 == "xml":
        print("called xml get-message")
        try:
            # decode_responses=True converts bytes to string
            value = r.get(topic)
            # print(isXml(value))
            # print(value)
            if isXml(value):
                return value
            else:
                value2 = readfromstring(value)
                data = json2xml.Json2xml(value2).to_xml()
                return data

        except Exception as ex:
            print(ex)

    else:
        print("called json get-message")
        try:
            # decode_responses=True converts bytes to string
            value = r.get(topic)
            # print(value)
            if isXml(value):
                data = json.dumps(xmltodict.parse(value))
                return data
            else:
                return value
        
        except Exception as ex:
            print(ex)





run(host="127.0.0.1", port=3000, debug=True, reloader=True)
