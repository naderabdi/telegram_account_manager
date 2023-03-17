import pytest
from app import app
from manager import AccountManager

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    response = client.get("/")
    assert response.status_code == 200

def test_add_account(client):
    response = client.post("/", data={"phone_number": "+1234567890", "api_id": "12345", "api_hash": "abcdefgh"})
    assert response.status_code == 200
    assert b"Account added successfully" in response.data

def test_switch_account(client):
    AccountManager("+1234567890", "12345", "abcdefgh")
    response = client.post("/", data={"account_id": "1"})
    assert response.status_code == 200
    assert b"Switched to account 1" in response.data

def test_send_message(client):
    response = client.post("/", data={"telegram_id": "123456789", "message": "Hello, world!"})
    assert response.status_code == 200
    if AccountManager.get_active_manager() is not None:
        assert b"Message sent successfully" in response.data
    else:
        assert b"Please select an account before sending messages" in response.data
