from bottle import default_app, get, view, run, static_file, post, request, redirect, template
import json
import jwt
import random
import string
import send_sms
import send_email
import uuid

import redis
from xml.etree import ElementTree
from json2xml import json2xml
from json2xml.utils import readfromstring
import xmltodict


#################################
n = 0
tok = ""


r = redis.Redis(
    host='127.0.0.1',
    port=6379,
    password='',
    decode_responses=True)

################################################################


@get("/")
@view("index")
def _():
    return
################################################################


################################################################
@get("/delete-from/topic/<topic>/from/<from1>/limit/<limit>/token/<token>")
def _(topic, from1, limit, token):
    try:
        global tok
        tok = r.get("token")
    except Exception as ex:
        print(ex)

    if (token == tok):

        mydict = []

        for k in r.scan_iter(topic + ":*"):
            mydict.append(k.split(":", 1)[1])

        mydict.sort()
        le = int(limit) + int(from1)

        if (len(mydict) >= int(from1) and len(mydict) >= le):
            small_dict = mydict[int(from1): le]

            for i in range(0, len(small_dict)):
                r.delete(topic + ":" + small_dict[i])
            return ("Deleted")

        elif (len(mydict) <= int(from1) or len(mydict) <= le):
            return ("From or limit exceed topics limit")
    else:
        return ("Invalid token or token expired")
################################################################


################################################################
@post("/create-message/topic/<topic>/token/<token>")
def _(topic, token):
    u = uuid.uuid1()

    try:
        global tok
        tok = r.get("token")
    except Exception as ex:
        print(ex)

    if (token == tok):
        if (request.headers.get('Content-Type') == "application/json"):
            data = json.load(request.body)

            try:
                r.set(topic + ":" + str(u), json.dumps(data))
                r.expire(topic + ":" + str(u), 5000)
                return ("OK JSON")

            except Exception as ex:
                print(ex)
        else:
            data = ElementTree.fromstring(request.body.read())
            print(request.headers.get('Content-Type'))

            try:
                r.set(topic + ":" + str(u), request.body.read())
                r.expire(topic + ":" + str(u), 5000)
                return ("OK XML")

            except Exception as ex:
                print(ex)
    else:
        return ("Invalid token or token expired")

    return ("Invalid data")
################################################################


################################################################
@get("/get-message/topic/<topic>/from/<from1>/limit/<limit>/format/<format1>/token/<token>")
def _(topic, format1, token, from1, limit):
    try:
        global tok
        tok = r.get("token")
    except Exception as ex:
        print(ex)

    if (token == tok):
        mydict = []

        for k in r.scan_iter(topic + ":*"):
            mydict.append(k.split(":", 1)[1])

        mydict.sort()
        le = int(limit) + int(from1)

        if (len(mydict) >= int(from1) and len(mydict) >= le):

            def isXml(value):
                try:
                    ElementTree.fromstring(value)
                except ElementTree.ParseError:
                    return False
                return True

            if format1 == "xml":
                try:
                    res = []

                    small_dict = mydict[int(from1): le]

                    for i in range(0, len(small_dict)):
                        value = r.get(topic + ":" + small_dict[i])
                        if isXml(value):
                            res.append(value)
                        else:
                            value2 = readfromstring(value)
                            data = json2xml.Json2xml(value2).to_xml()
                            res.append(data)

                    return res

                except Exception as ex:
                    print(ex)

            else:
                try:
                    res = []
                    small_dict = mydict[int(from1): le]
                    for i in range(0, len(small_dict)):
                        value = r.get(topic + ":" + small_dict[i])
                        if isXml(value):
                            data = json.dumps(xmltodict.parse(value))
                            res.append(data)
                        else:
                            res.append(value)
                    return res

                except Exception as ex:
                    print(ex)

        elif (len(mydict) <= int(from1) or len(mydict) <= le):
            return ("From or limit exceed topics limit")

    if (token != tok):
        return ("Invalid token or token expired")
    return ("No such topic")

################################################################


################################################################
@post("/upload")
@view("form")
def _():
    global n
    try:
        jwt.decode(request.json, key='secret', algorithms=['HS256', ])
        n = random.randint(1000, 9999)
        print(n)
        # send_sms.send_sms(n)
        send_email.send_email(n)
    except:
        print("failed")
    return
################################################################


################################################################
@post("/check")
def _():
    global tok

    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(10))

    try:
        r.set("token", result_str)
        # half hour
        r.expire("token", 4000)
    except Exception as ex:
        print(ex)

    print('token: ' + result_str)
    if int(request.forms.get('code')) != n:
        redirect('/')
    return template("welcome.html", encoded_jwt=result_str)
################################################################


################################################################
run(host="127.0.0.1", port=3333, debug=True, reloader=True)
################################################################
