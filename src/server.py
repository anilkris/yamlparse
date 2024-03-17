from flask import Flask, Response, jsonify, request,send_file,     abort
from werkzeug.utils import safe_join
import os


from src.utils.path_utils import get_resource_directories

app = Flask(__name__)


input_directory, output_directory = get_resource_directories() 
BASE_DIRECTORY=output_directory

def build_directory_json(directory, base_path=BASE_DIRECTORY):
    directory_json = {"files": []}
    for item in os.listdir(directory):
        full_path = os.path.join(directory, item)
        relative_path = os.path.relpath(full_path, start=base_path)
        if os.path.isdir(full_path):
            directory_json[item] = build_directory_json(full_path, base_path)
        else:
            directory_json["files"].append(relative_path)  
    return directory_json


@app.route('/api/files', methods=['GET'])
def get_files():

    file_path = request.args.get('path')  

    if file_path:
        try:
            safe_path = safe_join(BASE_DIRECTORY, file_path)
            print("safe path is " + safe_path)
            with open(safe_path, 'r', encoding='utf-8') as file:
                content = file.read()
            content_type = "text/plain"  
            return Response(content, mimetype=content_type)
        except Exception as e:
            abort(404, description="File not found or access denied.")
    else:
        directory_json = build_directory_json(BASE_DIRECTORY)
        return jsonify(directory_json)

if __name__ == '__main__':
    app.run(debug=True)
