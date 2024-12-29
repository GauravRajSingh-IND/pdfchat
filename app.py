from flask import Flask, request, render_template
import os
from vector_store import PineconeDB


app = Flask(__name__)

# Folder to store uploaded files
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if a file is part of the request
        if 'pdf_file' not in request.files:
            return render_template('index.html', message="No file part in the request")

        file = request.files['pdf_file']

        # Check if a file is selected
        if file.filename == '':
            return render_template('index.html', message="No file selected")

        # Validate the file type
        if file and file.filename.endswith('.pdf'):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            pinecone = PineconeDB(file_path=file_path)
            pinecone.upload_pdf_s3()

            return render_template('index.html', message=f"File successfully uploaded: {file.filename}")

        return render_template('index.html', message="Invalid file type. Please upload a PDF file.")

    # Render the upload form
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
