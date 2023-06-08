from flask import render_template, url_for,flash,redirect,request,abort,Blueprint,jsonify
from app import db,bcrypt
import random
from flask_cors import CORS,cross_origin
from firebase_admin import credentials, firestore
#from google.cloud.firestore_v1.base_query import FieldFilter, Or


agent_sec = db.collection('Utilisateurs')





users =Blueprint('users',__name__)

@cross_origin(origin=["http://127.0.0.1:5274","http://195.15.228.250","*"],headers=['Content-Type','Authorization'],automatic_options=False)
@users.route('/Agentsec/ajouter', methods=['POST'])
def create():
    try:
        id=request.json['id']
        request.json['id']=str(id)
        todo = agent_sec.document(id).get()
        if  todo.to_dict() is None :
            agent_sec.document(id).set(request.json)
            return jsonify({"success": True}), 200
        else:
            return jsonify({"Fail": "donnee exist deja"}), 400
    except:
        return 400

@cross_origin(origin=["http://127.0.0.1","http://195.15.228.250","*"],headers=['Content-Type','Authorization'])
@users.route('/Agentsec/tous/<start>/<limit>/', methods=['GET'])
def read(start,limit):
    if start !='0':
        last_doc=agent_sec.document(start).get()
        last_pos=last_doc.to_dict()['id']      
        sec=agent_sec.order_by('id').start_after({'id':last_pos}).limit(int(limit))
        
        all_todos = [doc.to_dict() for doc in sec.stream()]
        return jsonify(all_todos), 200
    else:
        sec=agent_sec.order_by('id', direction=firestore.Query.ASCENDING).limit(int(limit))
        all_todos = [doc.to_dict() for doc in sec.stream()]
        return jsonify(all_todos), 200
        #all_todos = [doc.to_dict() for doc in agent_sec.stream()]
    
    return  401

'''@users.route('/Agentsec/search/<Type>/<category>', methods=['GET'])
def search_ind(Type=None,category=None):
    if Type == None:
        filter_1 = FieldFilter("email", "==", category)
        filter_2 = FieldFilter("nom", "==", category)
        filter_3 = FieldFilter("prenom", "==", category)
        or_filter = Or(filters=[filter_1, filter_2,filter_3])
        todo = agent_sec.where(filter=or_filter)
        all_todos=[]
        for doc in todo.stream():
            v=doc.to_dict()
            v["id"]=doc.id
            all_todos.append(v)
        return jsonify(all_todos), 200
    if category == None:
        todo = agent_sec.where('role', '==',Type)
        all_todos=[]
        for doc in todo.stream():
            v=doc.to_dict()
            v["id"]=doc.id
            all_todos.append(v)
        return jsonify(all_todos), 200
    else:
        filter_1 = FieldFilter("email", "==", category)
        filter_2 = FieldFilter("nom", "==", category)
        filter_3 = FieldFilter("prenom", "==", category)
        or_filter = Or(filters=[filter_1, filter_2,filter_3])
        todo = agent_sec.where('role', '==',Type).where(filter=or_filter)
        all_todos=[]
        for doc in todo.stream():
            v=doc.to_dict()
            v["id"]=doc.id
            all_todos.append(v)
        return jsonify(all_todos), 200'''
    

@cross_origin(origin=["http://127.0.0.1","http://195.15.228.250","*"],headers=['Content-Type','Authorization'])
@users.route('/Agentsec/<ide>', methods=['GET'])
def read_ind(ide):
    todo_id = str(ide)
    
    if todo_id:
        todo = agent_sec.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            return jsonify(todo.to_dict()), 200

@cross_origin(origin=["http://127.0.0.1:5274","http://195.15.228.250","*"],headers=['Content-Type','Authorization'],automatic_options=False)
@users.route('/Agentsec/update/<ide>', methods=['POST', 'PUT'])
def update(ide):
        todo_id = str(ide)
        todo = agent_sec.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            agent_sec.document(todo_id).update(request.json)
            return jsonify({"success": True}), 200

@cross_origin(origin=["http://127.0.0.1:5274","http://195.15.228.250","*"],headers=['Content-Type','Authorization'],automatic_options=False)
@users.route('/Agentsec/delete/<ide>', methods=['GET', 'DELETE'])
def delete(ide):
    todo_id = str(ide)
    todo = agent_sec.document(todo_id).get()
    if todo.to_dict() is None:
        return jsonify({"Fail": "donnee n'exist pas"}), 400
    else:
        agent_sec.document(todo_id).delete()
        return jsonify({"success": True}), 200
