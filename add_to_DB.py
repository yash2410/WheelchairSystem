from pymongo import  MongoClient
client = MongoClient('localhost',27017)
WA = client.WA


def addUser(user,password):
    user_dict = {"username":user, "password":password}
    WA.users.insert_one(user_dict)

def checkUser(user):
       db_find = WA.users.find_one({'username': user})

       print(db_find)

addUser("yashdoshi","yashdoshi")
checkUser("yashdoshi")
