#This program is a restful API using Bottle as the framework and python as the language to allow for basic CRUD
#functionality. I used a MongoDB as the database to hold the data for my zoo and my animals.
#Author: Nicholas Richards
#SNHU
#February 6,2021


import json
from bson import json_util
import bottle
from bottle import route, run, request, abort
import datetime
import pymongo 
from pymongo import MongoClient
import pprint

#Connection to my database and collection
myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017")

mydb = myclient["NicksZoo"]

mycol = mydb["Animals"]

@route('/animals', method='POST')#route to create new animals 
def putAnimals():
	data = request.body.readline()
	if not data:
		abort(400, 'No data received')
	entity = json.loads(data)
	try:
		mydb['Animals'].save(entity)
	except ValidationError as ve:
		abort(400, str(ve))
	return "Insert Successful"

@route('/read/<name>', method='GET')#gets a specific animal by name
def get_animal(name):
    animal_result = name
    file = {"name":animal_result}
    query_result = mycol.find_one(file,{'_id':0})
    result = mycol.find_one(query_result)
    return json.loads(json.dumps(query_result, indent=4, default= json_util.default))


@route('/animals', method = 'GET')#gets all the animals
def getAllAnimals():
	query = mycol.find({},{"_id":0})
	results = []
	for q in query:
		print(q)
		results.append({'name':q['name'], 'type': q['type']})
	return("Animals : ",json.dumps(results))

@route('/updateAnimal/<name>', method = 'PUT')#updates the type of animal based on name
def updateAnimal(name):
	animal_result = name
	file = {"name":animal_result}
	data = request.body.readline()
	entity = json.loads(data)
	query_result = mycol.find_one_and_update(file,{"$set": {"type":entity}})
	return "Update successful"


@route('/delete/<name>', method ='DELETE')#deletes a specific animal
def delete_document(name):
    animal_result = name
    file = {"name":animal_result}
    query_result = mycol.find_one(file)
    result = mycol.delete_one(query_result)
    return "Delete Successful"
 
run(host='localhost', post=8080, debug=True, reloader=True)

