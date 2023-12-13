
from flask import Blueprint, current_app
from flask import request, jsonify
from werkzeug.utils import secure_filename
import os
from ..brain.person_tagging import tag_people_in

upload_route_bp = Blueprint('upload', __name__)


@upload_route_bp.route('/upload', methods=['POST'])
def upload():
    try:
        # Check if the 'files' key is in the request.files dictionary
        if 'files' not in request.files:
            return jsonify({'error': 'No files uploaded'})

        files = request.files.getlist('files')

        # Iterate through the uploaded files
        for file in files:
            if file.filename == '':
                continue  # Skip if the user didn't select a file

            # Save the file to the UPLOAD_FOLDER
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['STAGING_AREA'], filename))
            
        result = tag_people_in(current_app.config["STAGING_AREA"])
        return jsonify({'message': 'Files uploaded successfully', "tags": result})
    except Exception as e:
        return jsonify({'error': str(e)})