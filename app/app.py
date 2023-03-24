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

""" @app.route('/api/v1/video', methods=['POST'])
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
        return jsonify({'error': 'No file found'}) """

@app.route('/api/v1/video', methods=['POST'])
@cross_origin()
def upload():
    chunk_index = request.form['chunk-index']
    total_chunks = request.form['total-chunk']
    chunk_file = request.files['chunkFile']
    file_name = chunk_file.filename
    video_folder = '/app/data/videos'
    video_file_path = os.path.join(video_folder, file_name)

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


""" @app.route('/upload_image', methods=['POST'])
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
    return response """


if __name__ == '__main__':
    app.run()
