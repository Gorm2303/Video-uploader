from pymongo import MongoClient
from flask import Flask, request, jsonify
import os
import uuid


app = Flask(__name__)

# Connect to MongoDB instance
client = MongoClient(os.environ.get("MONGO_URI"))
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
def upload_image():
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg']
    file_name = request.form['filename']
    file_ext = os.path.splitext(file_name)[1]

    if file_ext.lower() in image_extensions:
        file_folder = '/data/images'
        file_prefix = 'image_'
    else:
        return jsonify({'error': 'Invalid file type'})

    return upload_file(request, file_folder, file_prefix, file_ext)
    
@app.route('/api/v1/video', methods=['POST'])
def upload_video():
    video_extensions = ['.mp4', '.avi', '.mov', '.wmv', '.mkv', '.flv', '.webm']
    file_name = request.form['filename']
    file_ext = os.path.splitext(file_name)[1]
    
    if file_ext.lower() in video_extensions:
        file_folder = '/data/videos'
        file_prefix = 'video_'
    else:
        return jsonify({'error': 'Invalid file type'})

    return upload_file(request, file_folder, file_prefix, file_ext)


def upload_file(request, file_folder, file_prefix, file_ext):
    chunk_index = request.form['chunkIndex']
    total_chunks = request.form['chunks']
    chunk_file = request.files['chunk']
    chunk_name = chunk_file.filename
    
    file_path = os.path.join(file_folder, file_prefix + str(uuid.uuid4()) + file_ext)

    chunk_folder = os.path.join(file_folder, 'chunks')
    if not os.path.exists(chunk_folder):
        os.makedirs(chunk_folder)

    chunk_file_path = os.path.join(chunk_folder, f'{chunk_name}.{chunk_index}')

    chunk_file.save(chunk_file_path)

    if int(chunk_index) == int(total_chunks) - 1:

        with open(file_path, 'wb') as output_file:
            for i in range(int(total_chunks)):
                chunk_path = os.path.join(chunk_folder, f'{chunk_name}.{i}')
                with open(chunk_path, 'rb') as input_file:
                    output_file.write(input_file.read())

                os.remove(chunk_path)

    return jsonify({'url': file_path})

if __name__ == '__main__':
    app.run()
