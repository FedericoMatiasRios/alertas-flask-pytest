import io
import pytest
from app import create_app
from werkzeug.datastructures import FileStorage

@pytest.fixture
def app():
    return create_app()

@pytest.fixture
def client(app):
    return app.test_client()

def test_root_endpoint(client):
    response = client.get('/')
    assert response.status_code == 200
    assert 'La aplicación de alerta temprana está en funcionamiento!'.encode('utf-8') in response.data

def test_send_alert(client):
    file_content = b'simulated image content'
    file = FileStorage(
        stream=io.BytesIO(file_content),
        filename='test_image.png',
        content_type='image/png'
    )

    response = client.post(
        '/api/alertas',
        data={
            'imagen': (file, 'test_image.png'),
            'ubicacion': 'Test Location',
            'latitud': '123',
            'longitud': '456',
            'descripcion': 'Test Description'
        }
    )

    assert response.status_code == 201
    assert b'Alerta recibida correctamente' in response.data

def test_get_alerts(client):
    response = client.get('/api/alertas')
    assert response.status_code == 200
    assert b'"alertas":' in response.data

def test_send_alert_missing_data(client):
    response = client.post('/api/alertas', data={})
    assert response.status_code == 500
    assert b'"error":' in response.data

def test_error_handling(client):
    response = client.post('/api/alertas', data={'imagen': 'invalid_data'})
    assert response.status_code == 500
    assert b'"error":' in response.data