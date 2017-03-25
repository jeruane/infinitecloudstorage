from flask import Flask, render_template, jsonify, redirect, url_for, request
from werkzeug.utils import secure_filename
from datetime import datetime
import sys
import httplib
import uuid
sys.stdout = sys.stderr

app = Flask(__name__)

from warp_drive import WarpDrive

WARP_DRIVE = WarpDrive("1RNNyvtmW0dbSzVTew_FyoUsfYmQOmvMoNH_FeP_yAn4")

@app.route('/')
def hello_world():
  return render_template('index.html')

def _pr(strin):
    print(strin)

@app.route('/upload_file', methods=['POST'])
def add_file():
    file = request.files['file']
    if file and allowed_file(file.filename):
        now = datetime.now()
        current_time = now.isoformat()
        filename = secure_filename(file.filename)
        data = file.read()
        file_id = uuid.uuid4()
        _pr('-------filename-------')
        _pr(filename)
        _pr('-------file_id-------')
        _pr(file_id)
        _pr('-------time-------')
        _pr(current_time)
        # _pr('-------file-------')
        # _pr(data)

        WARP_DRIVE.add_file(file_id, filename, len(data), current_time, data)
        return success((file_id, filename, len(data), now.isoformat()))
    else:
        return error(httplib.BAD_REQUEST, 'No file/bad file')

def allowed_file(filename):
    return '.' in filename

@app.route('/get_file', methods=['GET'])
def get_file():
    print 'get_file'
    file_id = request.values.get('id')
    file_name = request.values.get('file_name')
    file_data = WARP_DRIVE.read_file(file_id)
    return success((file_name, file_data))

@app.route('/update_file', methods=['POST'])
def update_file():
    return success('update_file')

@app.route('/delete_file', methods=['POST'])
def delete_file():
    print 'delete_file'
    file_id = request.values.get('id')
    WARP_DRIVE.delete_file(file_id)
    return success(file_id)

@app.route('/get_all', methods=['GET'])
def get_all():
    print 'get_all'
    return success(WARP_DRIVE.list_files())

def success(data):
    if not isinstance(data, dict):
        results = dict(data=data)
    else:
        results = data
    return jsonify(**results)


def error(code, message):
    response = jsonify(code=code, message=message)
    response.status_code = code
    return response

if __name__ == "__main__":
    app.run(debug=True)
