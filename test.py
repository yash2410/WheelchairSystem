from pprint import pprint
from flask import Flask,request
from pymongo import  MongoClient
import math
import dialogflow_v2 as dialogflow

client = MongoClient('localhost',27017)
WA = client.WA
app = Flask(__name__)


cursor = WA.move.find()
for document in cursor: 
    pprint(document)

WA.move.drop()

curso = WA.move.find()
for document in curso: 
    pprint(document)

print("#"*850)
