import os
from google.cloud import storage
from flask import Flask, request, render_template

app = Flask(__name__)

# Set the path to your Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"bubbly-mantis.json"

# Initialize the Google Cloud Storage client and bucket
BUCKET_NAME = 'gcp-bucket-62'
storage_client = storage.Client()

def upload_to_bucket(file):
    """Uploads a file to the specified Google Cloud Storage bucket."""
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(file.filename)
    blob.upload_from_file(file)
    return blob.public_url

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if a file was provided in the form
        if 'file' not in request.files:
            return render_template('upload.html', message="No file part in the request.")
        
        file = request.files['file']
        
        # Check if the filename is valid
        if file.filename == '':
            return render_template('upload.html', message="No file selected.")
        
        if file:
            # Upload the file to the GCP bucket
            file_url = upload_to_bucket(file)
            # Render the upload page with a success message to trigger the pop-up
            return render_template('upload.html', message=f"File successfully uploaded to: {file_url}")
    
    # Render the upload form when accessed via GET
    return render_template('upload.html', message=None)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
