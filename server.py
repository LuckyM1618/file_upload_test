import os
from flask import Flask, render_template, request, flash, redirect, session
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "Sphinx of Black Quartz, Judge My Vow!"

UPLOAD_FOLDER = 'static\\img'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = { 'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif' }

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/uploader', methods=['GET','POST'])
def upload_file():
    # check if the post request has a file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect('/')
    
    file = request.files['file']

    # if the user does not select a file, browser submits an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect('/')

    # if valid file submitted
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # "static\img\filename"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    # sending filename directly in route, since there is no database or 3rd party integration here
    # with a database, the filename would be saved in the database, and the route would use the id to fetch it
    return redirect(f'/view-image/{filename}')



@app.route('/view-image/<filename>')
def view_image(filename):
    return render_template('view_image.html', filename=filename)



if __name__=="__main__":
    app.run(debug = True)