from pprint import pprint

from flask import Flask,request
from pymongo import  MongoClient
import math
import dialogflow_v2 as dialogflow
import serial

client = MongoClient('localhost',27017)
WA = client.WA
app = Flask(__name__)

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

project_id = "smart-home-f132a"
session_id = 8052
language_code = "en"
client_access_token = "2843c211bdfd47c4b33bbae512bc04cc"
dev_access_token = "c8a96705fdf44139b7152fb352d8d89d"

@app.route('/')
def display():
    return "Mobile Index"

def detect_intent_texts(text):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""

    import dialogflow_v2 as dialogflow
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session))
    text_input = dialogflow.types.TextInput(
        text=text, language_code=language_code)

    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(
        session=session, query_input=query_input)

    print('=' * 50)
    pprint('Query text: {}'.format(response.query_result.query_text))
    pprint('Detected intent: {} (confidence: {})\n'.format(
    response.query_result.intent.display_name,
    response.query_result.intent_detection_confidence))
    pprint('Fulfillment text: {}\n'.format(
    response.query_result.fulfillment_text)) 
    intent = response.query_result.intent.display_name
    set_action(intent,text)

def set_action(intent,text):
    print("setting ACtion  for {}".format(intent))
    on = 'smarthome.lights.switch.on'
    off = 'smarthome.lights.switch.off'

    gar = 'garage'
    bed = 'bedroom'
    kit = 'kitchen'
    bath = 'bathroom'

    if intent in on:
        if gar in text:
            print("room :" + gar)
            ser.write(b'1')
        elif bed in text :
            print("room :" + bed)
            ser.write(b'2')
        elif kit in text :
            print("room :" + kit)
            ser.write(b'3')
        elif bath in text :
            print("room :" + bath)
            ser.write(b'4')
        else :
            print("Unknown Room")
    elif intent in off:
        if gar in text:
            print("room :" + gar)
            ser.write(b'5')
        elif bed in text :
            print("room :" + bed)
            ser.write(b'6')
        elif kit in text :
            print("room :" + kit)
            ser.write(b'7')
        elif bath in text :
            print("room :" + bath)
            ser.write(b'8')
        else :
            print("Unknown Room")
    else:
        print("Unknown Intent")
            

@app.route('/mobile/avon',methods=['GET', 'POST'])
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
    detect_intent_texts(text)
    return "Success"

def ard_map(x, in_min, in_max, out_min, out_max):
    return ((x - in_min) * (out_max - out_min) / (in_max - in_min)) + out_min

@app.route('/mobile/movement',methods=['GET', 'POST'])
def movement_processing():
    angle = request.form['angle']
    strength = request.form['strength']
    username = request.form['username']
    x_param = float(strength)*math.cos(float(angle))
    x_param = ard_map(x_param,-100,100.0,0,255)
    y_param = float(strength)*math.sin(float(angle))
    y_param = ard_map(x_param,0,100.0,0,255)
    move_dict = {
        "username" : username,
        "x" : x_param,
        "y" : y_param
    }
    print(move_dict)
    
    if (x_param == 0.0 and y_param == 0.0):
        print("x and y are 0")
        return "Success"
    
    try:
        db_find = WA.move.find_one({'username': username})
        req_num = db_find["req_num"] + 1        
        WA.move.update_one(
            {"username": username},
            {
                "$set": {
                    "x": x_param,
                    "y": y_param,
                    "req_num" : req_num
                }
            }
        )
        print("+"*50)
    except:
        print("#"*50)
        movement_dict = {
            "username" : username,
            "x" : x_param,
            "y" : y_param,
            "req_num" : 0
        }
        WA.move.insert_one(movement_dict)
    
    db_ = WA.move.find_one({'username': username})
    print(db_)
    return "Success"

@app.route('/mobile/login',methods=['GET', 'POST'])
def login_processing():
    username = request.form['username']
    password = request.form['password']
    print(request.form)
    db_find = WA.users.find_one({'username': username})
    print("Login Processing :")
    if(password == db_find['password']):
        return "Success"
    return "Failed"



if __name__=='__main__':
    app.run(host = "0.0.0.0",port = '8080',debug=True)





"""
if x_param is 0 and y_param is 0 :
      return "Success"        
    elif(db_find != None):
        req_num = db_find["req_num"] + 1        
        WA.move.update_one(
            {"username": username},
            {
                "$set": {
                    "x": x_param,
                    "y": y_param,
                    "req_num" : req_num
                }
            }
        )
    else:
        movement_dict = {
            "username" : username,
            "x" : x_param,
            "y" : y_param,
            "req_num" : req_num
        }
        WA.move.insert_one(movement_dict)
    
"""