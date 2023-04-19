from flask import render_template, url_for,flash,redirect,request,abort,Blueprint,jsonify
from app import db,bcrypt
from flask_cors import CORS,cross_origin

admi_n = db.collection('Admin')
agent_sec = db.collection('Agentsec')
agent_con = db.collection('Agentcon')
clien_t= db.collection('Client')





admin =Blueprint('admin',__name__)

@cross_origin(origin=["http://127.0.0.1:5274","http://195.15.228.250","*"],headers=['Content-Type','Authorization'],automatic_options=False)
@admin.route('/Admin/ajouter', methods=['POST'])
def create():
    try:
        id=[doc.to_dict() for doc in admi_n.stream()]#[-1]['id']
        id=str(len(id))
    except:
        id='0'
    if id:
        request.json['id']=str(id)
        request.json['password']=bcrypt.generate_password_hash(request.json['password']).decode('utf-8')
        todo = admi_n.document(id).get()
        if  todo.to_dict() is None :
            admi_n.document(id).set(request.json)
            all_=admi_n.document(id).get()
            return jsonify(all_.to_dict()), 200
        else:
            return jsonify({"Fail": "donnee exist deja"}), 400
    else:
        return 400

@cross_origin(origin=["http://127.0.0.1","http://195.15.228.250","*"],headers=['Content- Type','Authorization'])
@admin.route('/Admin/tous', methods=['GET'])
def read():
    all_todos = [doc.to_dict() for doc in admi_n.stream()]
    return jsonify(all_todos), 200

@cross_origin(origin=["http://127.0.0.1","http://195.15.228.250","*"],headers=['Content- Type','Authorization'])
@admin.route('/users/tous', methods=['GET'])
def read_all():
    all_admin = [doc.to_dict() for doc in admi_n.stream()]
    all_agent_sec = [doc.to_dict() for doc in agent_sec.stream()]
    all_client = [doc.to_dict() for doc in clien_t.stream()]
    all_con = [doc.to_dict() for doc in agent_con.stream()]
    return jsonify({"Admin": all_admin,
        "Agent_secteur": all_agent_sec,
        "Client": all_client,
        "Agent_Constat": all_con,
        }), 200
    

@cross_origin(origin=["http://127.0.0.1","http://195.15.228.250","*"],headers=['Content- Type','Authorization'])
@admin.route('/Admin/<string:ide>', methods=['GET'])#hide data
def read_ind(ide):
    todo_id = str(ide)
    
    if todo_id:
        todo = admi_n.where('email','==',todo_id)
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            return jsonify(todo.to_dict()), 200

@cross_origin(origin=["http://127.0.0.1:5274","http://195.15.228.250","*"],headers=['Content-Type','Authorization'],automatic_options=False)
@admin.route('/Admin/update/<int:ide>', methods=['POST', 'PUT'])
def update(ide):
        todo_id = str(ide)
        todo = admi_n.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            admi_n.document(todo_id).update(request.json)
            return jsonify({"success": True}), 200

@cross_origin(origin=["http://127.0.0.1:5274","http://195.15.228.250","*"],headers=['Content-Type','Authorization'],automatic_options=False)
@admin.route('/Admin/delete/<int:ide>', methods=['GET', 'DELETE'])
def delete(ide):
    todo_id = str(ide)
    todo = admi_n.document(todo_id).get()
    if todo.to_dict() is None:
        return jsonify({"Fail": "donnee n'exist pas"}), 400
    else:
        admi_n.document(todo_id).delete()
        return jsonify({"success": True}), 200