from flask import Flask, request, jsonify, render_template
from azure.storage.blob import BlobServiceClient

# Initialize the Blob Service Client using your Azure connection string
bsc = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=systemscase07;AccountKey=5HXyInTprRuVxLzBKXmfwtTaplPyO7YfFZ7hBzomfJxgeeYREBLH0Zz0WISg+qNx4Qt0xmzWdMh++AStIq9EOQ==;EndpointSuffix=core.windows.net")

# Get the container client
container_name = "lanternfly-images-i5exza0c"
cc = bsc.get_container_client(container_name)

# Initialize the Flask app
app = Flask(__name__)

@app.get("/")
def index():
    return render_template("index.html")

@app.post("/api/v1/upload")
def upload():
    try:
        # Get the uploaded file
        f = request.files["file"]
        filename = f.filename

        # Upload the file to Azure Blob Storage
        blob_client = cc.get_blob_client(filename)  # Create blob client using filename
        blob_client.upload_blob(f, overwrite=True)  # Upload file and overwrite if it exists

        # Return the URL where the file is uploaded
        return jsonify(ok=True, url=f"{cc.url}/{filename}")
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500

@app.get("/api/v1/gallery")
def gallery():
    urls = [f"{cc.url}/{blob.name}" for blob in cc.list_blobs()]
    return jsonify(ok=True, gallery=urls)

@app.get("/api/v1/health")
def health():
    # Simple health check endpoint to see if the server is running
    return jsonify(status="Healthy")

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)