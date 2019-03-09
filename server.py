from flask import Flask,request
from pymongo import  MongoClient
import math
import dialogflow_v2 as dialogflow

client = MongoClient('localhost',27017)
WA = client.WA
app = Flask(__name__)

project_id = "smart-home-f132a"
session_id = 8052
language_code = "en"

@app.route('/')
def display():
    return "Index"

@app.route('/mobile/avon')
def speech_processing():
    text = request.form['Text']
    user = request.form['username']
    db_find = WA.speech.find_one({"username" : user})
    if(db_find != None):
        req_num = db_find["req_num"] + 1
        WA.speech.update_one(
            {"username": user},
            {
                "$set": {
                    "text": text,
                    "req_num" : req_num
                }
            }
        )
    else:
        speech_dict = {
            "username" : user,
            "text" : text,
            "req_num" : 0
        }
        db_find = speech_dict
        WA.speech.insert_one(speech_dict)
    print("Speech Processing :" + db_find)
    return "Success"

@app.route('/mobile/movement')
def movement_processing():
    angle = request.form['angle']
    strength = request.form['strength']
    username = request.form['username']
    x_param = strength*math.cos(float(angle))
    y_param = strength*math.sin(float(angle))

    move_dict = {
        "username" : username,
        "x" : x_param,
        "y" : y_param
    }

    db_find = WA.move.find_one({'username': username})
    if(db_find != None):
        WA.move.update_one(
            {"username": username},
            {
                "$set": {
                    "x": x_param,
                    "y": y_param
                }
            }
        )
    else:
        WA.move.insert_one(move_dict)
        db_find = move_dict
    
    print("Move Processing :" + db_find)
    return "Success"

@app.route('/mobile/login')
def login_processing():
    username = request.form['username']
    password = request.form['password']

    db_find = WA.users.find_one({'username': username})
    print("Login Processing :" + db_find)
    if(password == db_find['password']):
        return "Success"
    return "Failed"

@app.route('/arduino/movement/<user>')
def movement(user):
    db_find = WA.move.find_one({'username': user})
    if(db_find != None):
        angle = db_find["angle"]
        strength = db_find["strength"]
        query_reply = angle+","+strength
        return query_reply
        
    return "Failed"

@app.route('/arduino/speech/<user>')
def speech(user):
    db_find = WA.speech.find_one({'username': user})
    text = db_find["Text"]
    print(text)  

if __name__=='__main__':
    app.run(host = "0.0.0.0",port = '8080')
