from pymongo import MongoClient
import requests


# Connect to MongoDB instance
#client = MongoClient('localhost', 27017, username='root', password='root')
#db = client['video_db']
#videos = db['videos']
def test_create_video():
    url = 'http://localhost:80/videometadata'
    data = {
        'title': 'Test Video',
        'description': 'A test video',
        'genre': ['Action', 'Adventure'],
        'length': 120,
        'release_date': '2022-01-01',
        'image': 'https://example.com/image.png'
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200
    assert 'success' in response.json()
    assert response.json()['success'] == True
    assert 'message' in response.json()
    assert response.json()['message'] == 'Video created successfully'
    assert 'id' in response.json()
    assert isinstance(response.json()['id'], str)

test_create_video()
# Query and print all video documents
#for video in videos.find():
 #   print(video)
