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
import uuid

import redis
from xml.etree import ElementTree
from json2xml import json2xml
from json2xml.utils import readfromstring
import xmltodict

import datetime
from collections import OrderedDict

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
    u = uuid.uuid1()
    # print("UUID: ")
    # print(u)
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
            # print(request.headers.get('Content-Type'))

            try:
                # print(topic + ":" + str(u))
                r.set(topic + ":" + str(u), json.dumps(data))
                r.expire(topic, 600)
                return ("OK JSON")

            except Exception as ex:
                print(ex)
        else:
            data = ElementTree.fromstring(request.body.read())
            print(request.headers.get('Content-Type'))

            try:
                r.set(topic + ":" + str(u), request.body.read())
                r.expire(topic, 600)
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
    # global mydict

    try:
        global tok
        tok = r.get("token")
    except Exception as ex:
        print(ex)

    # for k in r.scan_iter(topic + ":*"):
    #     mydict.append(k.split(":", 1)[1])
    # mydict.sort(key=lambda x:x['Timestamp'])
    # mydict.sort()
    # print(len(mydict))
    # print(mydict[0])
    # print(uuid.UUID(mydict[0]).time)
    # print(mydict[1])
    # print(mydict[2])
    # print(mydict[3])
    # print(uuid.UUID(mydict[1]).int)
    # print(uuid.UUID(mydict[2]).int)
    # print(uuid.UUID(mydict[3]).int)
    # dates = [datetime.datetime.strptime(ts, "%Y-%m-%d %H:%M:%S %Z") for ts in mydict]
    # dates = mydict.sort()-
    # print("dates")
    # print(dates)
    # ordered_data = OrderedDict(sorted(mydict.items(), key = lambda x:datetime.strptime(x[0], '%d-%m-%Y')) )
    # print(ordered_data)

    if (token == tok):
        mydict = []

        for k in r.scan_iter(topic + ":*"):
            mydict.append(k.split(":", 1)[1])        

        mydict.sort()
        le = int(limit) + int(from1)
        # print(from1)
        # print(le)
        # print(mydict)
        # print(mydict[int(from1): le])
        
        if (len(mydict) >= int(from1) and len(mydict) >= le):
        
            def isXml(value):
                try:
                    ElementTree.fromstring(value)
                except ElementTree.ParseError:
                    return False
                return True

            if format1 == "xml":
                # print("called xml get-message")
                try:
                    res = []
                    # decode_responses=True converts bytes to string
                    
                    small_dict = mydict[int(from1): le]
                    # print(small_dict)
                    # for x in small_dict:
                    #     print("1")
                    #     res.append(r.get(topic) + ":" + x)
                    for i in range(0 , len(small_dict)):
                        value = r.get(topic + ":" + small_dict[i])
                        if isXml(value):
                            res.append(value)
                        else:
                            value2 = readfromstring(value)
                            data = json2xml.Json2xml(value2).to_xml()
                            res.append(data)
                        # res.append(r.get(topic + ":" + small_dict[i]))
                        # value = r.get(topic)
                    # print(res)
                    return res
                    # value = r.get(topic)
                    # print(isXml(value))
                    # print(value)
                    # if isXml(value):
                    #     return value
                    # else:
                    #     value2 = readfromstring(value)
                    #     data = json2xml.Json2xml(value2).to_xml()
                    #     return data

                except Exception as ex:
                    print(ex)

            else:
                # print("called json get-message")
                try:
                    res = []
                    small_dict = mydict[int(from1): le]
                    for i in range(0 , len(small_dict)):
                        value = r.get(topic + ":" + small_dict[i])
                        if isXml(value):
                            data = json.dumps(xmltodict.parse(value))
                            res.append(data)
                        else:
                            res.append(value)
                    return res
                    # decode_responses=True converts bytes to string
                    # value = r.get(topic)
                    # # print(value)
                    # if isXml(value):
                    #     data = json.dumps(xmltodict.parse(value))
                    #     return data
                    # else:
                    #     return value

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
    result_str = ''.join(random.choice(letters) for i in range(10))

    try:
        r.set("token", result_str)
        r.expire("token", 2000)
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
