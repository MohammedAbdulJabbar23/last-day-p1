import pytest
from starlette.testclient import TestClient
from main import app

@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client

@pytest.fixture
def websocket_client():
    with TestClient(app) as client:
        with client.websocket_connect("/ws/testo_room") as websocket:
            yield websocket

def test_websocket_endpoint(websocket_client):
    websocket_client.send_text("Hello, server!")
    response = websocket_client.receive_text()
    assert response == "Hello, server!"

    websocket_client.send_text("Hello, there!")
    response = websocket_client.receive_text()
    assert response == "Hello, there!"

def test_websocket_endpoint_large_message(websocket_client):
    # Send a large message to the server
    large_message = "a" * 100000  # Creating a large string
    websocket_client.send_text(large_message)

    # Receive the echoed message from the server
    response = websocket_client.receive_text()
    assert response == large_message

def test_history_of_chat_room(client):
    response = client.get("/history/test_room")
    assert response.status_code == 200
    assert len(response.json()) == 7  
    print(response.json()[1])
    post_data = response.json()[0]  
    assert post_data == {
            "sender": "anonymous",
            "message": "hahah",
            "timestamp": "2024-03-06T12:33:27.220268+00:00",
        }
