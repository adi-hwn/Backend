from flask import render_template,request,url_for,send_file,redirect
from werkzeug.utils import secure_filename
from app import app
from config import *
from code.stuff import anotherThingToDo
from PythonOMR.prototype2 import processLine


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def getdirectory():
    return url_for('static',filename='Actual WebFront/dummy.txt')[:-9]


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):

            filename = secure_filename(file.filename)
            file.save(os.path.join(basedir,app.config['UPLOAD_FOLDER'], filename))


            #outgoing = aThingToDo(os.path.join(basedir,app.config['UPLOAD_FOLDER'], filename))
            test = processLine(os.path.join(basedir,app.config['UPLOAD_FOLDER'], filename),True)

            outputName = "testOutput.txt"
            outputPath = os.path.join(basedir,app.config['UPLOAD_FOLDER'], outputName)
            outputFile = anotherThingToDo(os.path.join(basedir,app.config['UPLOAD_FOLDER'], filename),outputPath,test)
            #return render_template("result.html", outgoing = outgoing, outputPath = outputPath,
            #                       downloadLink = url_for('download',output = outputPath))
            return redirect(url_for('download',output = outputPath))

    return render_template("index.html", directory = getdirectory())


@app.route('/<output>', methods=['GET', 'POST'])
def download(output):
    return send_file(output, as_attachment=True)
