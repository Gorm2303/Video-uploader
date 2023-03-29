from pymongo import MongoClient
from flask import Flask, request, jsonify, flash, Response
from flask_cors import CORS, cross_origin
import os
import uuid


app = Flask(__name__)
cors = CORS(app)

# Connect to MongoDB instance
client = MongoClient('mongodb+srv://admin:admin@cluster0.acahawh.mongodb.net/?retryWrites=true&w=majority')
#client = MongoClient('mongodb://root:root@localhost:27017')
db = client['video_db']
videosCollection = db['videos']

@app.route('/')
def index():
    return 'Welcome to the Uploader API!'

#Endpoint for uploading video metadata
@app.route('/api/v1/videometadata', methods=['POST'])
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

@app.route('/poster', methods=['POST'])
@cross_origin()
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
    file = request.files['file']
    if file:
        # generate a UUID4
        filename = 'image_' + str(uuid.uuid4())
        file_path = os.path.join('/app/data/images', filename)
        file.save(file_path)
        return jsonify({'url': file_path})
    else:
        return jsonify({'error': 'No file found'})

@app.route('/video', methods=['POST'])
@cross_origin()
def upload_video():
    file = request.files['file']
    if file:
        # generate a UUID4
        filename = 'video_' + str(uuid.uuid4())
        file_path = os.path.join('/app/data/videos', filename)
        file.save(file_path)
        return jsonify({'url': file_path})
    else:
        return jsonify({'error': 'No file found'})

if __name__ == '__main__':
    app.run()
