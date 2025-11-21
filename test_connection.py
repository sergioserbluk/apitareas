#!/usr/bin/env python3
import requests
import json

def test_backend():
    try:
        # Probar endpoint simple
        print("Probando GET /test...")
        response = requests.get('http://127.0.0.1:5001/test')
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        # Probar registro
        print("\nProbando POST /auth/register...")
        data = {
            "nombre": "testuser",
            "email": "test@example.com",
            "password": "123456"
        }
        response = requests.post('http://127.0.0.1:5001/auth/register', json=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        # Probar login
        print("\nProbando POST /auth/login...")
        login_data = {
            "email": "test@example.com",
            "password": "123456"
        }
        response = requests.post('http://127.0.0.1:5001/auth/login', json=login_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_backend()