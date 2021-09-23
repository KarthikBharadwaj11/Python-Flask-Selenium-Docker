from flask import Flask, request, make_response, jsonify, url_for, redirect
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'static/uploads/'

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#Image/Media config
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#To post an image
@app.route('/post', methods=['POST'])
def post_image():
    file = request.files['image']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return make_response(jsonify({"result": filename}), 200)

#To get an image
@app.route('/get/<imagename>')
def get_image(imagename):
    return redirect(url_for( 'static', filename='uploads/' + imagename), code=301)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)