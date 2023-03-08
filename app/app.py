from pymongo import MongoClient
from flask import Flask, request, jsonify

app = Flask(__name__)

# Connect to MongoDB instance
client = MongoClient('mongodb://root:root@127.0.0.1:27017/video_db')
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

if __name__ == '__main__':
    app.run()
