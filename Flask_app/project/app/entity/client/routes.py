from flask import render_template, url_for,flash,redirect,request,abort,Blueprint,jsonify
from app import db
from flask_cors import CORS,cross_origin


clien_t= db.collection('Agentsec')





client =Blueprint('client',__name__)

@cross_origin(origin=["http://127.0.0.1:5274","http://195.15.228.250","*"],headers=['Content-Type','Authorization'],automatic_options=False)
@client.route('/Client/ajouter', methods=['POST'])
def create():
    try:
        id=[doc.to_dict() for doc in clien_t.stream()]#[-1]['id']
        id=[int(i['id']) for i in id]
        id.sort()
        id=str(id[-1]+1)
    except:
        id='0'
    if id:
        request.json['id']=str(id)
        #request.json['pass']=bcrypt.generate_password_hash(request.json['pass']).decode('utf-8')
        todo = clien_t.document(id).get()
        if  todo.to_dict() is None :
            clien_t.document(id).set
            (request.json)
            return jsonify({"success": True}), 200
        else:
            return jsonify({"Fail": "donnee exist deja"}), 400
    else:
        return 400

@cross_origin(origin=["http://127.0.0.1","http://195.15.228.250","*"],headers=['Content- Type','Authorization'])
@client.route('/Client/tous', methods=['GET'])
def read():
    all_todos = [doc.to_dict() for doc in clien_t.stream()]
    return jsonify(all_todos), 200

@cross_origin(origin=["http://127.0.0.1","http://195.15.228.250","*"],headers=['Content- Type','Authorization'])
@client.route('/Client/<ide>', methods=['GET'])
def read_ind(ide):
    todo_id = str(ide)
    
    if todo_id:
        todo = clien_t.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            return jsonify(todo.to_dict()), 200

@cross_origin(origin=["http://127.0.0.1:5274","http://195.15.228.250","*"],headers=['Content-Type','Authorization'],automatic_options=False)
@client.route('/Client/update/<ide>', methods=['POST', 'PUT'])
def update(ide):
        todo_id = str(ide)
        todo = clien_t.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            clien_t.document(todo_id).update(request.json)
            return jsonify({"success": True}), 200

@cross_origin(origin=["http://127.0.0.1:5274","http://195.15.228.250","*"],headers=['Content-Type','Authorization'],automatic_options=False)
@client.route('/Client/delete/<int:ide>', methods=['GET', 'DELETE'])
def delete(ide):
    todo_id = str(ide)
    todo = clien_t.document(todo_id).get()
    if todo.to_dict() is None:
        return jsonify({"Fail": "donnee n'exist pas"}), 400
    else:
        clien_t.document(todo_id).delete()
        return jsonify({"success": True}), 200