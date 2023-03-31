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

@app.route('/api/v1/poster', methods=['POST'])
@cross_origin()
def upload_image():
    chunk_index = request.form['chunkIndex']
    total_chunks = request.form['chunks']
    chunk_file = request.files['chunk']
    file_name = chunk_file.filename
    image_folder = '/app/data/images'
    image_name = 'image_' + str(uuid.uuid4())
    image_file_path = os.path.join(image_folder, image_name)

    chunk_folder = '/app/data/images/chunks'
    if not os.path.exists(chunk_folder):
        os.makedirs(chunk_folder)

    chunk_file_path = os.path.join(chunk_folder, f'{file_name}.{chunk_index}')

    chunk_file.save(chunk_file_path)

    if int(chunk_index) == int(total_chunks) - 1:

        with open(image_file_path, 'wb') as output_file:
            for i in range(int(total_chunks)):
                chunk_path = os.path.join(chunk_folder, f'{file_name}.{i}')
                with open(chunk_path, 'rb') as input_file:
                    output_file.write(input_file.read())

                os.remove(chunk_path)

    return jsonify({'url': image_file_path})
    
@app.route('/api/v1/video', methods=['POST'])
@cross_origin()
def upload_video():
    chunk_index = request.form['chunkIndex']
    total_chunks = request.form['chunks']
    chunk_file = request.files['chunk']
    file_name = chunk_file.filename
    video_folder = '/app/data/videos'
    video_name = 'video_' + str(uuid.uuid4())
    video_file_path = os.path.join(video_folder, video_name)

    chunk_folder = '/app/data/videos/chunks'
    if not os.path.exists(chunk_folder):
        os.makedirs(chunk_folder)

    chunk_file_path = os.path.join(chunk_folder, f'{file_name}.{chunk_index}')

    chunk_file.save(chunk_file_path)

    if int(chunk_index) == int(total_chunks) - 1:

        with open(video_file_path, 'wb') as output_file:
            for i in range(int(total_chunks)):
                chunk_path = os.path.join(chunk_folder, f'{file_name}.{i}')
                with open(chunk_path, 'rb') as input_file:
                    output_file.write(input_file.read())

                os.remove(chunk_path)

    return jsonify({'url': video_file_path})

if __name__ == '__main__':
    app.run()
