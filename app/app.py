from pymongo import MongoClient
from flask import Flask, request, jsonify

app = Flask(__name__)

# Connect to MongoDB instance
client = MongoClient('localhost', 27017, username='root', password='root')
db = client['video_db']
videos = db['videos']

#Endpoint for uploading video metadata
@app.route('/videos', methods=['POST'])
def upload_video_metadata():
    # Parse JSON request body
    data = request.json

    # Insert video into MongoDB
    result = videos.insert_one(data)

    # Return JSON response
    response = {
        'success': True,
        'message': 'Video added successfully',
        'id': str(result.inserted_id)
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run()
