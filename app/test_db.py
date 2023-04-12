import json
import os
import pytest
from pymongo import MongoClient
from app import app, videosCollection

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def setup_db():
    # Connect to MongoDB database
    mongo_uri = os.environ.get("MONGO_URI")
    mongo_client = MongoClient(mongo_uri)
    db = mongo_client['video_db']
    videos_collection = db['videos']

    # Insert sample data
    sample_video = {'title': 'Test Video', 'description': 'This is a test video'}
    inserted_video = videos_collection.insert_one(sample_video)

    return videos_collection, inserted_video

def teardown_db(videos_collection, inserted_video):
    # Clean up the test data
    videos_collection.delete_one({'_id': inserted_video.inserted_id})

def test_upload_video_metadata(client):
    videos_collection, inserted_video = setup_db()
    data = {'title': 'Test Video', 'description': 'This is a test video'}
    response = client.post('/api/v1/videometadata', json=data)
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data['success']
    assert response_data['id']
    teardown_db(videos_collection, inserted_video)
