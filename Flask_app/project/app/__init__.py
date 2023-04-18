from flask import Flask, render_template, url_for,flash,redirect,request, jsonify,make_response
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt
from flask_login import  LoginManager
#from flask_mail import Mail
from app.config import Config
import os
from firebase_admin import credentials, firestore, initialize_app
from flask_cors import CORS
# Initialize Flask App

# Initialize Firestore DB



cred = credentials.Certificate('/work/www/microservice_edl/utilisateur/Flask_app/project/app/key.json')
default_app = initialize_app(cred)
db = firestore.client()
bcrypt = Bcrypt()



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    with app.app_context():
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "http://127.0.0.1")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")

   
    bcrypt.init_app(app)

    CORS(app, resources={r"/Admin/*": {"origins": ["http://127.0.0.1","http://195.15.218.172","*"]}},headers='Content-Type')
    CORS(app, resources={r"/users/*": {"origins": ["http://127.0.0.1","http://195.15.218.172","*"]}},headers='Content-Type')
    CORS(app, resources={r"/Client/*": {"origins": ["http://127.0.0.1","http://195.15.218.172","*"]}},headers='Content-Type')
    CORS(app, resources={r"/Agentsec/*": {"origins": ["http://127.0.0.1","http://195.15.218.172","*"]}},headers='Content-Type')
    CORS(app, resources={r"/Agentcon/*": {"origins": ["http://127.0.0.1","http://195.15.218.172","*"]}}, headers='Content-Type')

    app.config['CORS_HEADERS'] ='Content-Type'
   

    from app.entity.users.routes import users
    from app.entity.agentc.routes import agentcon
    from app.entity.admin.routes import admin
    from app.entity.client.routes import client
    
    app.register_blueprint(users)
    app.register_blueprint(agentcon)
    app.register_blueprint(admin)
    app.register_blueprint(client)

   
    


    return app
