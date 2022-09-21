from flask import render_template, url_for,flash,redirect,request,abort,Blueprint,jsonify
from app import db,bcrypt


admi_n = db.collection('Admin')





admin =Blueprint('admin',__name__)

@admin.route('/Admin/ajouter', methods=['POST'])
def create():
    id = request.json['id']
    request.json['pass']=bcrypt.generate_password_hash(request.json['pass']).decode('utf-8')
    if id:
        todo = admi_n.document(id).get()
        if  todo.to_dict() is None :
            admi_n.document(id).set(request.json)
            return jsonify({"success": True}), 200
        else:
            return jsonify({"Fail": "donnee exist deja"}), 400
    else:
        return 400

@admin.route('/Admin/tous', methods=['GET'])
def read():
    all_todos = [doc.to_dict() for doc in admi_n.stream()]
    return jsonify(all_todos), 200

@admin.route('/Admin/<int:ide>', methods=['GET'])
def read_ind(ide):
    todo_id = str(ide)
    
    if todo_id:
        todo = admi_n.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            return jsonify(todo.to_dict()), 200

@admin.route('/Admin/update/<int:ide>', methods=['POST', 'PUT'])
def update(ide):
        todo_id = str(ide)
        todo = admi_n.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            admi_n.document(todo_id).update(request.json)
            return jsonify({"success": True}), 200

@admin.route('/Admin/delete/<int:ide>', methods=['GET', 'DELETE'])
def delete(ide):
    todo_id = str(ide)
    todo = admi_n.document(todo_id).get()
    if todo.to_dict() is None:
        return jsonify({"Fail": "donnee n'exist pas"}), 400
    else:
        admi_n.document(todo_id).delete()
        return jsonify({"success": True}), 200