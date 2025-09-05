import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_get_bookings():
    """Test de récupération des réservations"""
    print("=== Test GET /booking ===")
    response = requests.get(f"{BASE_URL}/booking")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_create_booking_success():
    """Test de création d'une réservation valide"""
    print("=== Test POST /booking (succès) ===")
    booking_data = {
        "customerName": "Jean Dupont",
        "phoneNumber": "+33123456789",
        "email": "jean.dupont@email.com",
        "roomNumber": 5,
        "roomDescription": "Chambre double avec vue sur mer",
        "reservationDate": "15/12/2025"
    }
    
    response = requests.post(
        f"{BASE_URL}/booking",
        json=booking_data,
        headers={"Content-Type": "application/json"}
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_create_booking_invalid_room():
    """Test avec numéro de chambre invalide (hors de 1-9)"""
    print("=== Test POST /booking (numéro de chambre invalide) ===")
    booking_data = {
        "customerName": "Marie Martin",
        "phoneNumber": "+33987654321",
        "email": "marie.martin@email.com",
        "roomNumber": 15,  
        "roomDescription": "Chambre simple",
        "reservationDate": "20/12/2025"
    }
    
    response = requests.post(
        f"{BASE_URL}/booking",
        json=booking_data,
        headers={"Content-Type": "application/json"}
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_create_booking_duplicate():
    """Test de création d'une réservation en double (même chambre, même date)"""
    print("=== Test POST /booking (réservation en double) ===")
    booking_data = {
        "customerName": "Pierre Durand",
        "phoneNumber": "+33555666777",
        "email": "pierre.durand@email.com",
        "roomNumber": 5,  
        "roomDescription": "Chambre triple",
        "reservationDate": "15/12/2025"
    }
    
    response = requests.post(
        f"{BASE_URL}/booking",
        json=booking_data,
        headers={"Content-Type": "application/json"}
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_create_booking_invalid_date():
    """Test avec format de date invalide"""
    print("=== Test POST /booking (format de date invalide) ===")
    booking_data = {
        "customerName": "Sophie Leroy",
        "phoneNumber": "+33111222333",
        "email": "sophie.leroy@email.com",
        "roomNumber": 3,
        "roomDescription": "Suite présidentielle",
        "reservationDate": "2025-12-25" 
    }
    
    response = requests.post(
        f"{BASE_URL}/booking",
        json=booking_data,
        headers={"Content-Type": "application/json"}
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_create_booking_invalid_email():
    """Test avec email invalide"""
    print("=== Test POST /booking (email invalide) ===")
    booking_data = {
        "customerName": "Paul Bernard",
        "phoneNumber": "+33444555666",
        "email": "email-invalide",  
        "roomNumber": 7,
        "roomDescription": "Chambre familiale",
        "reservationDate": "30/12/2025"
    }
    
    response = requests.post(
        f"{BASE_URL}/booking",
        json=booking_data,
        headers={"Content-Type": "application/json"}
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def run_all_tests():
    """Exécute tous les tests"""
    print("🚀 Démarrage des tests de l'API de réservation d'hôtel")
    print("=" * 60)
    
    try:
      
        test_get_bookings()
        
        test_create_booking_success()
        
        test_get_bookings()
        
        test_create_booking_invalid_room()
        
        test_create_booking_duplicate()
        
        test_create_booking_invalid_date()
        
       
        test_create_booking_invalid_email()
        
        print("✅ Tous les tests ont été exécutés")
        
    except requests.exceptions.ConnectionError:
        print("❌ Erreur: Impossible de se connecter à l'API")
        print("Assurez-vous que le serveur FastAPI est démarré sur http://localhost:8000")
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")

if __name__ == "__main__":
    run_all_tests()