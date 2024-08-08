from flask import Blueprint, render_template, request, redirect, url_for, current_app
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime
from app.google_drive import upload_to_drive

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    return render_template('upload.html')

@bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    screens = request.form.getlist('screens')
    if not screens:
        return "Please select at least one screen.", 400

    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)

    if file:
        timestamp = datetime.now().strftime('%d_%m_%H_%M')
        screen_numbers = "_".join(f"screen_{screen}" for screen in screens)
        file_extension = os.path.splitext(file.filename)[1]
        drive_filename = f"{timestamp}_{screen_numbers}{file_extension}"
        
        upload_folder = current_app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        
        filepath = os.path.join(upload_folder, secure_filename(file.filename))
        file.save(filepath)
        
        folder_name = "Visulart"
        file_id = upload_to_drive(filepath, drive_filename, folder_name)
        
        upload_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        file_info = {
            "file_id": file_id,
            "file_name": drive_filename,
            "upload_date": upload_date,
            "screen_number": screens
        }
        
        update_json(file_info)
        os.remove(filepath)
        
        return 'File uploaded and metadata saved successfully'

def update_json(file_info):
    json_file = 'uploads_metadata.json'
    
    if os.path.exists(json_file):
        with open(json_file, 'r') as f:
            data = json.load(f)
    else:
        data = []
    
    data.append(file_info)
    
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=4)
