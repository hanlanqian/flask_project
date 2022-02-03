from turtle import up
from flask import Blueprint, render_template, send_from_directory, request, redirect, url_for
from config import files_path
from models import Resource
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


@resource.route('/upload', methods=["POST"])
def upload_file():
    upload = request.files['upload']
    upload.seek(0, 2)
    size = upload.tell()/1024
    if upload:
        upload.seek(0, 0)        
        upload.save(f'./files/{upload.filename}')
        file = Resource.upsert({'file_name': upload.filename, 'file_size': size})


    return redirect(url_for('resource.hello'))





@resource.route('/test')
def test():
    data = {'file_name': '123', 'file_size': 123}
    # m = Resource.get_or_404(id=2)
    file = Resource.upsert(data=data)
    print(file[0].__dict__)
    return "0"