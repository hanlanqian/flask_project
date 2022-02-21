from flask import Blueprint, render_template, send_from_directory, request, redirect, url_for, jsonify
from models import User

user = Blueprint('user', __name__)



@user.route("/api/register", methods=['POST'])
def register():
    form = request.json
    print(form)
    result = User.register(form)
    print(result)
    # User.insert(form)
    


    return jsonify(code=200)

@user.route("/api/login", methods=['POST'])
def login():
    form = request.json
    print(form)
    result = User.authLogin(form)
    print(result)

    
    return jsonify(code=200)