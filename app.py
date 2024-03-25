from flask import Flask, render_template, redirect, request,send_from_directory, url_for, abort
from werkzeug.utils import secure_filename
import os
import tlparser

app = Flask(__name__)

app.config['UPLOAD_PATH'] = 'static/uploads/'
app.config['UPLOAD_EXTENSIONS'] = ['.txt']

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/parser', methods=['GET', 'POST'])
def parser_file():
  files = os.listdir(app.config['UPLOAD_PATH'])
  return render_template('parser.html', files=files)

@app.route('/parser/<string:file_name>',methods = ['GET', 'POST'])
def parser(file_name):
  tl_out = tlparser.parserProgram(app.config['UPLOAD_PATH'] + file_name)
  if isinstance(tl_out, tuple):
    data = file_name + ' : <br>'+ str(tl_out[0])+ ' hours '+ str(tl_out[1])+ ' minutes'
    result(data)
    return redirect('parser')
  else:
    result(file_name +' : <br>' +tl_out)
    return redirect('parser')

@app.route("/file_name" , methods=['GET', 'POST'])
def file_name():
  if request.method == 'POST':
    select = request.form.get('comp_select')
    return(parser(str(select)))
  else:
    return render_template('parser.html')

@app.route('/upload')
def upload():
    files = os.listdir(app.config['UPLOAD_PATH'])
    return render_template('upload.html', files=files)

@app.route('/upload', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
    return redirect(url_for('upload'))

@app.route('/static/uploads/<filename>')
def upload_txt(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)

@app.route('/delete')
def delete():
    files = os.listdir(app.config['UPLOAD_PATH'])
    return render_template('delete.html', files=files)

@app.route('/delete_files/<string:delete>', methods=['GET','POST'])
def delete_files(delete):
    filename = os.path.join(app.config['UPLOAD_PATH'], delete)
    if (filename != '' and filename != 'None'):
      os.remove(filename)
      return redirect(url_for('delete'))
    else:
        return render_template('parser.html')

@app.route("/delete_txt", methods=['GET', 'POST'])
def delete_txt():
    if request.method == 'POST':
        select = request.form.get('comp_select')
        return delete_files(str(select))
    else:
        return render_template('delete.html')

@app.route('/result')
def result(data):
    f = open('static/result/result.txt', 'w+')
    f.write(data)

@app.route('/read_txt', methods = ['GET', 'POST'])
def read_txt():
    f = open('static/result/result.txt', 'r')
    content = f.read()
    return content

@app.route('/reference')
def reference():
  return render_template('referernce.html')

@app.route('/about')
def about():
  return render_template('about.html')


if __name__ == "__main__":
  app.run(debug=True)