from flask import render_template, url_for,flash,redirect,request,abort,Blueprint,jsonify
from app import db,bcrypt
from flask_cors import CORS,cross_origin

admi_n = db.collection('Admin')





admin =Blueprint('admin',__name__)

@cross_origin(origin=["http://127.0.0.1","http://195.15.228.250","*"],headers=['Content- Type','Authorization'])
@admin.route('/Admin/ajouter', methods=['POST'])
def create():
    try:
        id=[doc.to_dict() for doc in admi_n.stream()][-1]['id']
        id=str(int(id)+1)
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
@admin.route('/Admin/<string:ide>', methods=['GET'])#hide data
def read_ind(ide):
    todo_id = str(ide)
    
    if todo_id:
        todo = admi_n.where('email','==',todo_id)
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            return jsonify(todo.to_dict()), 200

@cross_origin(origin=["http://127.0.0.1","http://195.15.228.250","*"],headers=['Content- Type','Authorization'])
@admin.route('/Admin/update/<int:ide>', methods=['POST', 'PUT'])
def update(ide):
        todo_id = str(ide)
        todo = admi_n.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            admi_n.document(todo_id).update(request.json)
            return jsonify({"success": True}), 200

@cross_origin(origin=["http://127.0.0.1","http://195.15.228.250","*"],headers=['Content- Type','Authorization'])
@admin.route('/Admin/delete/<int:ide>', methods=['GET', 'DELETE'])
def delete(ide):
    todo_id = str(ide)
    todo = admi_n.document(todo_id).get()
    if todo.to_dict() is None:
        return jsonify({"Fail": "donnee n'exist pas"}), 400
    else:
        admi_n.document(todo_id).delete()
        return jsonify({"success": True}), 200