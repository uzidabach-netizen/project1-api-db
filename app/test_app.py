from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}[cite: 1]

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to FastAPI + MySQL"}

@patch("app.get_db_connection")
def test_get_items(mock_get_db):
    # נגדיר Mock עבור החיבור וה-Cursor למסד הנתונים
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    
    # נגדיר מה ה-cursor.fetchall() אמור להחזיר
    mock_cursor.fetchall.return_value = [{"id": 1, "name": "Apple"}]
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_db.return_value = mock_conn

    response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == [{"id": 1, "name": "Apple"}][cite: 1]

@patch("app.get_db_connection")
def test_add_item(mock_get_db):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_db.return_value = mock_conn

    response = client.post("/items/Banana")
    assert response.status_code == 200
    # בדוק שמחזיר JSON עם message ו-name
    data = response.json()
    assert "message" in data[cite: 1]
    assert data["name"] == "Banana"
    