from flask import render_template, url_for,flash,redirect,request,abort,Blueprint,jsonify
from app import db,bcrypt,create_app
import random
from flask_cors import CORS,cross_origin
from flask_wkhtmltopdf import Wkhtmltopdf
import os
import base64


app= create_app()

wkhtmltopdf =Wkhtmltopdf(app)

pd_f =Blueprint('pd_f',__name__)

@cross_origin(origin=["http://127.0.0.1:5274","http://195.15.228.250","*"],headers=['Content-Type','Authorization'],automatic_options=False)
@pd_f.route('/print/file', methods=['POST'])
def printer():
    facture=request.json
    res=wkhtmltopdf.render_template_to_pdf('print.html', download=True, save=False,facture=facture)
    return res