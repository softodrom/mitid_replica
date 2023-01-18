# Bottle
# Route to validate the app
# from curses import resetty
from bottle import default_app, get, view, run, static_file, post, request, redirect, template
import json
import jwt
from xml.dom import minidom
import random
import time
import string
import send_sms
import send_email

import redis
from xml.etree import ElementTree
from json2xml import json2xml
from json2xml.utils import readfromstring
import xmltodict


#################################
n = 0
encoded_jwt = ""
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
@get("/delete-message/topic/<topic>/token/<token>")
def _(topic, token):
    try:
        global tok
        tok = r.get("token")
    except Exception as ex:
        print(ex)


    if (token == tok):
        try:
            r.delete(topic)
            return ("Deleted")
        except Exception as ex:
            print(ex)
    else:
        return ("Invalid token or token expired")
################################################################


################################################################
@post("/create-message/topic/<topic>/token/<token>")
def _(topic, token):
    # decode_responses=True converts bytes to string
    try:
        global tok
        tok = r.get("token")
    except Exception as ex:
        print(ex)


    if (token == tok):    
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
    else:
        return ("Invalid token or token expired")           

    return ("Invalid data")     
################################################################


################################################################
@get("/get-message/topic/<topic>/format/<format1>/token/<token>")
def _(topic, format1, token):
    try:
        global tok
        tok = r.get("token")
    except Exception as ex:
        print(ex)


    if (token == tok):
        def isXml(value):
            try:
                ElementTree.fromstring(value)
            except ElementTree.ParseError:
                return False
            return True

        if format1 == "xml":
            # print("called xml get-message")
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
            # print("called json get-message")
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
    else:
        return ("Invalid token or token expired")

    return ("No such topic")
################################################################


################################################################
@post("/upload")
@view("form")
def _():
    global n
    try:
        # print(jwt.decode(request.json, key='secret', algorithms=['HS256', ]))
        jwt.decode(request.json, key='secret', algorithms=['HS256', ])
        n = random.randint(1000, 9999)
        print(n)
        # send_sms.send_sms(n)
        send_email.send_email(n)
    except:
        print("failed")
    # send_email.send_email(n)
    return
################################################################


################################################################
@post("/check")
# @view("welcome")
def _():
    global encoded_jwt
    global tok
    # cpr = "12345"
    # iat = int(time.time())
    # exp = iat + 600
    # encoded_jwt = jwt.encode(
    #     {"cpr": cpr, "iat": iat, "exp": exp}, "secret", algorithm="HS256")
    
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range (10))

    try:
        r.set("token", result_str)
        r.expire("token", 100)
    except Exception as ex:
        print(ex)

    print('token: ' + result_str)
    if int(request.forms.get('code')) != n:
        redirect('/')
    return template("welcome.html", encoded_jwt=result_str)


run(host="127.0.0.1", port=3333, debug=True, reloader=True)
################################################################
# try:
#     # Server AWS (Production)
#     import production
#     application = default_app()
# except:
#     # Local machine
#     run(host="127.0.0.1", port=3333, debug=True, reloader=True, server="paste")
