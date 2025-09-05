from fastapi.testclient import TestClient
from main import app 

client = TestClient(app)


def test_create_booking_success():
    booking_data = {
        "customerName": "Jean Dupont",
        "phoneNumber": "0612345678",
        "email": "jean.dupont@example.com",
        "roomNumber": 3,
        "roomDescription": "Chambre avec vue sur mer",
        "reservationDate": "10/09/2025"
    }

    response = client.post("/booking", json=booking_data)
    assert response.status_code == 200
    data = response.json()
    assert data["customerName"] == booking_data["customerName"]
    assert data["roomNumber"] == booking_data["roomNumber"]


def test_create_booking_conflict():
    booking_data = {
        "customerName": "Alice Martin",
        "phoneNumber": "0698765432",
        "email": "alice.martin@example.com",
        "roomNumber": 3,
        "roomDescription": "Chambre avec vue sur mer",
        "reservationDate": "10/09/2025"  
    }

    response = client.post("/booking", json=booking_data)
    assert response.status_code == 400
    data = response.json()
    assert data["detail"]["message"] == "La chambre n'est plus disponible pour cette date"


def test_get_bookings():
    response = client.get("/booking")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
