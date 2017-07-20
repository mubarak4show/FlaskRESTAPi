import os

from flask import Flask, render_template, request, jsonify, redirect, send_from_directory
from werkzeug.utils import secure_filename

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'zip'])

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("upload.html")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploadPic', methods=['GET', 'POST'])
def uploadPic():
    target = os.path.join(APP_ROOT, 'RocketImages/')
    print(target)
    if not os.path.isdir(target):
        os.mkdir(target)
    if request.method == 'POST':
        # check if the post request has the file part

        if 'file' not in request.files:
            print('No File Part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser submits an empty part
        # without filename
        if file.filename == '':
            print('No Selected File')
            return jsonify({'Response': "No file was selected. Please Select a Valid File and Try Again"})
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            destination = "/".join([target, filename])
            file.save(destination)
            return jsonify({'Response': "SUCCESSFULLY UPLOADED FILE "})
        else:
            return jsonify({'Response': 'FAILED. Make sure it is an image or a zip file'})
    return render_template("upload.html")


@app.route('/uploadPic/<filename>', methods=['GET'])
def uploaded_file(filename):
    target = os.path.join(APP_ROOT, 'RocketImages/')
    if filename in target:
        return send_from_directory(target, filename)
    else:
        return jsonify({'Response': "File Does Not Exist"})

if __name__ == '__main__':
    app.run(debug=True)
