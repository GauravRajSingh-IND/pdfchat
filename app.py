from flask import Flask, request, render_template, redirect, url_for
import os

app = Flask(__name__)

# Folder to store uploaded files
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    # Render the index.html where users can upload a file
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'pdf_file' not in request.files:
        return "No file part in the request", 400

    file = request.files['pdf_file']

    if file.filename == '':
        return "No file selected", 400

    if file and file.filename.endswith('.pdf'):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        return f"File successfully uploaded: {file.filename}", 200

    return "Invalid file type. Please upload a PDF file.", 400

if __name__ == '__main__':
    app.run(debug=True)
