import os
from flask import Flask, render_template, request, redirect, url_for, abort
from pii_redactor import pii_redactor
import os
os.makedirs("results", exist_ok=True)

app=Flask(__name__)

# Files can be up to 16MB
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
# Allow these files
app.config['UPLOAD_EXTENSIONS'] = ['.txt', '.pdf', '.doc', '.docx']
# Send files to upload folder
app.config['UPLOAD_PATH'] = 'uploads/'
#Send redacted files to results folder
app.config['RESULT_PATH'] = 'results/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_files():

    # Upload multiple files
    for uploaded_file in request.files.getlist('file'):
        if uploaded_file.filename != '':
            # Save files to upload folder
            file_path = os.path.join(app.config['UPLOAD_PATH'], uploaded_file.filename)
            uploaded_file.save(file_path)  

            name, extension = os.path.splitext(uploaded_file.filename) 
            redacted_filename = f"{name}_redacted{extension}"       
            output_path = os.path.join(app.config['RESULT_PATH'], redacted_filename) 

            pii_redactor(file_path, output_path) 
    
    return uploaded_file.filename

@app.route('/results')
def results():
    # This just displays the results page
    return render_template('results.html')

if __name__ == "__main__":
    app.run(debug=True)