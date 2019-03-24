from flask import Flask,request
from pymongo import  MongoClient
import math
import dialogflow_v2 as dialogflow

client = MongoClient('localhost',27017)
WA = client.WA
app = Flask(__name__)


@app.route('/')
def display():
    return "Ard Index"


@app.route('/arduino/speech/<user>',methods=['GET', 'POST'])
def speech(user):
    db_find = WA.speech.find_one({'username': user})
    text = db_find["text"]
    print(text)  
    return text

@app.route('/arduino/movement/<user>',methods=['GET', 'POST'])
def movement(user):
    db_find = WA.move.find_one({'username': user})
    if(db_find != None):
        x_param = db_find["x"]
        y_param = db_find["y"]
        req_num = db_find["req_num"]        
        query_reply = str(x_param)+","+str(y_param)+","+str(req_num)
        print("Reply : " +query_reply)
        return query_reply
        
    return "Failed"


if __name__=='__main__':
    app.run(host = "0.0.0.0",port = '5000',debug=True)
