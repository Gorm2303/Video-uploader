from pymongo import MongoClient
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import uuid


app = Flask(__name__)
cors = CORS(app)
cors = CORS(app, origins=["http://localhost:3000"])

# Connect to MongoDB instance
client = MongoClient('mongodb+srv://admin:admin@cluster0.acahawh.mongodb.net/?retryWrites=true&w=majority')
#client = MongoClient('mongodb://root:root@localhost:27017')
db = client['video_db']
videosCollection = db['videos']

@app.route('/')
def index():
    return 'Welcome to the Uploader API!'

#Endpoint for uploading video metadata
@app.route('/videometadata', methods=['POST'])
def upload_video_metadata():
    # Parse JSON request body
    data = request.json

    # Insert video into MongoDB
    result = videosCollection.insert_one(data)

    # Return JSON response
    response = {
        'success': True,
        'message': 'Video added successfully',
        'id': str(result.inserted_id)
    }
    return jsonify(response)

@app.route('/api/v1/video', methods=['POST'])
def upload_video():
    file = request.files['file']
    # generate a UUID4
    filename = 'video' + str(uuid.uuid4())
    filepath = os.path.join('/app/data/videos', filename)
    file.save(filepath)
    response = {
        'success': True,
        "message": "File uploaded successfully",
        "url": filepath,
    }
    return response

@app.route('/api/v1/poster', methods=['POST'])
def upload_poster():
    file = request.files['file']
    # generate a UUID4
    filename = 'image' + str(uuid.uuid4())
    filepath = os.path.join('/app/data/images', filename)
    file.save(filepath)
    response = {
        'success': True,
        "message": "File uploaded successfully",
        "url": filepath,
    }
    return response

if __name__ == '__main__':
    app.run()
