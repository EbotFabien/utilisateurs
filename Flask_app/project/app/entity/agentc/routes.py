from flask import render_template, url_for,flash,redirect,request,abort,Blueprint,jsonify
from app import db,bcrypt


agent_con = db.collection('Agentcon')





agentcon =Blueprint('agentcon',__name__)

@agentcon.route('/Agentcon/ajouter', methods=['POST'])
def create():
    id = request.json['id']
    if id:
        request.json['pass']=bcrypt.generate_password_hash(request.json['pass']).decode('utf-8')
        todo = agent_con.document(id).get()
        if  todo.to_dict() is None :
            agent_con.document(id).set(request.json)
            return jsonify({"success": True}), 200
        else:
            return jsonify({"Fail": "donnee exist deja"}), 400
    else:
        return 400

@agentcon.route('/Agentsec/tous', methods=['GET'])
def read():
    all_todos = [doc.to_dict() for doc in agent_con.stream()]
    return jsonify(all_todos), 200

@agentcon.route('/Agentsec/<int:ide>', methods=['GET'])
def read_ind(ide):
    todo_id = str(ide)
    
    if todo_id:
        todo = agent_con.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            return jsonify(todo.to_dict()), 200

@agentcon.route('/Agentsec/update/<int:ide>', methods=['POST', 'PUT'])
def update(ide):
        todo_id = str(ide)
        todo = agent_con.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            agent_con.document(todo_id).update(request.json)
            return jsonify({"success": True}), 200

@agentcon.route('/Agentsec/delete/<int:ide>', methods=['GET', 'DELETE'])
def delete(ide):
    todo_id = str(ide)
    todo = agent_con.document(todo_id).get()
    if todo.to_dict() is None:
        return jsonify({"Fail": "donnee n'exist pas"}), 400
    else:
        agent_con.document(todo_id).delete()
        return jsonify({"success": True}), 200