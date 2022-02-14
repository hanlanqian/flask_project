from flask import Blueprint, render_template, send_from_directory, request, redirect, url_for, jsonify
from config import files_path
from models import Resource
import json
import os

resource = Blueprint('resource', __name__)

@resource.route('/')
def hello():
    files = Resource.query.all()
    files_name = []
    files_size = []
    files_create_time = []
    files_update_time = []
    for file in files:
        files_name.append(file.file_name)
        files_size.append(file.file_size)
        files_create_time.append(file.create_time)
        files_update_time.append(file.update_time)
    files = zip(files_name, files_size, files_create_time, files_update_time)
    return render_template('static.html', files=files)


@resource.route('/files/<filename>')
def download_file(filename):
    return send_from_directory(files_path, filename)


@resource.route('/file/upload', methods=["POST"])
def upload_file():
    form = request.form
    file_data = request.files
    for _, data in file_data.items():
        if os.path.exists(f"{files_path}/{data.filename}"):
            os.remove(f"{files_path}/{data.filename}")
        data.save(f"{files_path}/{data.filename}")
    for _, file_info_str in form.items():
        file_info = json.loads(file_info_str)
        Resource.upsert(file_info)
    return jsonify(code=200, msg="upload successfully!!")

@resource.route('/file/delete', methods=['POST']) 
def delete_file():
    files = request.json
    for file_name in files:
        Resource.delete(file_name)
    return jsonify(code=200, msg="delete successfully!!")


@resource.route('/file/get')
def get_files():
    ms = Resource.get_all()
    return jsonify(data=ms, code=200, msg='get data successfully!!')

@resource.route('/test')
def test():
    # file = Resource.get_or_none(file_name='激活.md')[0]
    # m = Resource.get_or_404(id=2)
    # file.to_dict()
    Resource.delete('激活.md')
    # print(file[0].__dict__)
    return "0"
