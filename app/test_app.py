import os
import pytest
import tempfile
from unittest.mock import patch
from app import app
from app import upload_file
from werkzeug.datastructures import FileStorage



@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.data == b'Welcome to the Uploader API!'

def test_upload_small_image(client):
    temp_file = tempfile.NamedTemporaryFile()

    data = {
        'chunkIndex': '0',
        'chunks': '1',
        'chunk': temp_file,
        'filename': 'video_1.jpg'
    }

    response = client.post(
        '/api/v1/poster', 
        data=data,
        content_type='multipart/form-data'
    )
    assert response.status_code == 200
    assert response.json['url']

def test_upload_small_video(client):
    temp_file = tempfile.NamedTemporaryFile()

    data = {
        'chunkIndex': '0',
        'chunks': '1',
        'chunk': temp_file,
        'filename': 'video_1.mp4'
    }

    response = client.post(
        '/api/v1/video', 
        data=data,
        content_type='multipart/form-data'
    )
    assert response.status_code == 200
    assert response.json['url']

def test_upload_large_image(client):
    temp_file = tempfile.NamedTemporaryFile(delete=False)

    chunks = 20
    response = ''
    for i in range(0, chunks):
        with open(temp_file.name, 'rb') as f:
            response = client.post(
                '/api/v1/poster', 
                data= {
                    'chunkIndex': i,
                    'chunks': chunks,
                    'chunk': f,
                    'filename': 'image_2.png'
                },
                content_type='multipart/form-data'
            )
            assert response.status_code == 200
    
    assert response.json['url']


def test_upload_large_video(client):
    temp_file = tempfile.NamedTemporaryFile(delete=False)

    chunks = 20
    
    for i in range(0, chunks):
        with open(temp_file.name, 'rb') as f:
            response = client.post(
                '/api/v1/video', 
                data= {
                    'chunkIndex': i,
                    'chunks': chunks,
                    'chunk': f,
                    'filename': 'video_2.mp4'
                },
                content_type='multipart/form-data'
            )
            assert response.status_code == 200
    
    assert response.json['url']


def test_upload_video_invalid_type(client):
    data = {
        'filename': 'test.py',
        'chunkIndex': 0,
        'chunks': 1
    }
    temp_file = tempfile.NamedTemporaryFile(delete=False)

    data['chunk'] = (temp_file, 'test.py')

    response = client.post('/api/v1/video', data=data, content_type='multipart/form-data')

    assert 'error' in response.json
    assert response.json['error'] == 'Invalid file type'

def test_upload_poster_invalid_type(client):
    data = {
        'filename': 'test.py',
        'chunkIndex': 0,
        'chunks': 1
    }
    temp_file = tempfile.NamedTemporaryFile(delete=False)

    data['chunk'] = (temp_file, 'test.py')

    response = client.post('/api/v1/poster', data=data, content_type='multipart/form-data')

    assert 'error' in response.json
    assert response.json['error'] == 'Invalid file type'
