from pprint import pprint
from pymongo import  MongoClient
client = MongoClient('localhost',27017)
WA = client.WA


def addUser(user,password):
    user_dict = {"username":user, "password":password}
    WA.users.insert_one(user_dict)

def checkUser(user):
       db_find = WA.users.find_one({'username': user})

       print(db_find)

def addMove(username,x,y,req_num):
    move_dict = {"username": username,"x":x,"y":y,"req_num":req_num}
    WA.move.insert_one(move_dict)

def findMove(username):
    db_find = WA.move.find_one({"username":username})
    print(db_find)
    print("#"*50)

def print_move():
    cursor = WA.move.find()
    for document in cursor: 
        pprint(document)
    print("#"*50)

def drop_db(collection):
    if collection is "move":
        WA.move.drop()
    elif collection is "user":
        WA.user.drop()
    elif collection is "speech":
        WA.speech.drop()
    else:
        pprint("Invalid Collection")     
        

#drop_db("move")
findMove(u'yashdoshi')
