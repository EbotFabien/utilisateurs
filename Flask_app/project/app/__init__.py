from flask import Flask, render_template, url_for,flash,redirect,request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt
from flask_login import  LoginManager
#from flask_mail import Mail
from app.config import Config
import os
from firebase_admin import credentials, firestore, initialize_app
# Initialize Flask App

# Initialize Firestore DB



cred = credentials.Certificate('/work/www/microservice_edl/utilisateur/Flask_app/project/app/key.json')
default_app = initialize_app(cred)
db = firestore.client()
bcrypt = Bcrypt()



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

   
    bcrypt.init_app(app)
   

    from app.entity.users.routes import users
    from app.entity.agentc.routes import agentcon
    from app.entity.admin.routes import admin
    from app.entity.client.routes import client
    
    app.register_blueprint(users)
    app.register_blueprint(agentcon)
    app.register_blueprint(admin)
    app.register_blueprint(client)
    


    return app
