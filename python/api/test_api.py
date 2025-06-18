#!/usr/bin/env python3
"""
Test API - Flood Prediction API
Testes automatizados para a API de predição de enchentes.
"""

import pytest
import asyncio
from httpx import AsyncClient
from fastapi.testclient import TestClient

from main import app

# Cliente de teste
client = TestClient(app)

class TestFloodPredictionAPI:
    """Testes da API de predição de enchentes"""
    
    def test_root_endpoint(self):
        """Testa endpoint raiz"""
        response = client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert data["name"] == "Flood Prediction API"
        assert data["version"] == "1.0.0"
        assert "endpoints" in data
    
    def test_health_endpoint(self):
        """Testa endpoint de saúde"""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert "status" in data
        assert "model_loaded" in data
        assert "uptime_seconds" in data
        assert data["model_version"] == "1.0.0"
    
    def test_predict_endpoint_valid_data(self):
        """Testa predição com dados válidos"""
        
        # Dados de teste válidos
        test_data = {
            "sensor_data": [
                {
                    "precipitation": 0.0,
                    "humidity": 65.0,
                    "temperature": 22.0,
                    "pressure": 1015.0
                }
            ] * 24,  # 24 horas
            "device_id": "TEST_001",
            "timestamp": "2025-06-17T19:30:00"
        }
        
        response = client.post("/predict", json=test_data)
        
        # Pode retornar 200 ou 503 dependendo se modelo está carregado
        assert response.status_code in [200, 503]
        
        if response.status_code == 200:
            data = response.json()
            assert "flood_probability" in data
            assert "risk_level" in data
            assert "confidence" in data
            assert data["device_id"] == "TEST_001"
            assert 0.0 <= data["flood_probability"] <= 1.0
            assert data["risk_level"] in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    
    def test_predict_endpoint_invalid_data(self):
        """Testa predição com dados inválidos"""
        
        # Dados incompletos (menos de 24 horas)
        invalid_data = {
            "sensor_data": [
                {
                    "precipitation": 0.0,
                    "humidity": 65.0,
                    "temperature": 22.0,
                    "pressure": 1015.0
                }
            ] * 10,  # Apenas 10 horas
            "device_id": "TEST_INVALID"
        }
        
        response = client.post("/predict", json=invalid_data)
        assert response.status_code == 422  # Validation error
    
    def test_predict_endpoint_out_of_range(self):
        """Testa predição com valores fora do range"""
        
        # Dados com valores inválidos
        invalid_data = {
            "sensor_data": [
                {
                    "precipitation": -10.0,  # Negativo inválido
                    "humidity": 150.0,       # Acima de 100%
                    "temperature": 100.0,    # Temperatura muito alta
                    "pressure": 500.0        # Pressão muito baixa
                }
            ] * 24
        }
        
        response = client.post("/predict", json=invalid_data)
        assert response.status_code == 422  # Validation error
    
    def test_model_info_endpoint(self):
        """Testa endpoint de informações do modelo"""
        response = client.get("/model/info")
        
        # Pode retornar 200 ou 503 dependendo se modelo está carregado
        assert response.status_code in [200, 503]
        
        if response.status_code == 200:
            data = response.json()
            assert "model_loaded" in data
            assert "model_version" in data
            assert "total_params" in data
    
    def test_test_predict_endpoint(self):
        """Testa endpoint de teste automático"""
        response = client.get("/test/predict")
        assert response.status_code == 200
        
        data = response.json()
        assert "test_results" in data
        assert "model_working" in data
        
        if data["model_working"]:
            test_results = data["test_results"]
            assert "normal_scenario" in test_results
            assert "flood_scenario" in test_results
    
    def test_esp32_endpoint_valid(self):
        """Testa endpoint ESP32 com dados válidos"""
        
        esp32_data = {
            "device_id": "ESP32_TEST",
            "timestamp": "2025-06-17T19:30:00",
            "sensor_history": [
                {
                    "water_level": 0.0,
                    "humidity": 65.0,
                    "temperature": 22.0,
                    "pressure": 1015.0
                }
            ] * 24
        }
        
        response = client.post("/predict/esp32", json=esp32_data)
        
        # Pode retornar 200 ou 503 dependendo se modelo está carregado
        assert response.status_code in [200, 503]
    
    def test_esp32_endpoint_invalid(self):
        """Testa endpoint ESP32 com dados inválidos"""
        
        esp32_data = {
            "device_id": "ESP32_TEST",
            "sensor_history": []  # Lista vazia
        }
        
        response = client.post("/predict/esp32", json=esp32_data)
        assert response.status_code == 400
    
    def test_cors_headers(self):
        """Testa headers CORS"""
        response = client.options("/")
        
        # Verifica se CORS está configurado
        # (Pode não ter headers em modo de teste)
        assert response.status_code in [200, 405]
    
    def test_docs_endpoint(self):
        """Testa documentação automática"""
        response = client.get("/docs")
        assert response.status_code == 200
        
        # Verifica se retorna HTML da documentação
        assert "text/html" in response.headers.get("content-type", "")
    
    def test_redoc_endpoint(self):
        """Testa documentação ReDoc"""
        response = client.get("/redoc")
        assert response.status_code == 200
        
        # Verifica se retorna HTML da documentação
        assert "text/html" in response.headers.get("content-type", "")

# Testes de integração (precisam do modelo carregado)
class TestIntegration:
    """Testes de integração que dependem do modelo"""
    
    @pytest.mark.skipif(
        not client.get("/health").json().get("model_loaded", False),
        reason="Modelo não está carregado"
    )
    def test_flood_prediction_scenarios(self):
        """Testa cenários específicos de predição"""
        
        # Cenário 1: Condições normais
        normal_scenario = {
            "sensor_data": [
                {
                    "precipitation": 0.0,
                    "humidity": 60.0,
                    "temperature": 22.0,
                    "pressure": 1015.0
                }
            ] * 24,
            "device_id": "TEST_NORMAL"
        }
        
        response = client.post("/predict", json=normal_scenario)
        assert response.status_code == 200
        
        data = response.json()
        # Em condições normais, risco deve ser baixo
        assert data["risk_level"] in ["LOW", "MEDIUM"]
        
        # Cenário 2: Chuva intensa
        rain_scenario = {
            "sensor_data": [
                {
                    "precipitation": 30.0 if i > 20 else 0.0,
                    "humidity": 95.0 if i > 20 else 70.0,
                    "temperature": 24.0,
                    "pressure": 1005.0 if i > 20 else 1015.0
                }
                for i in range(24)
            ],
            "device_id": "TEST_RAIN"
        }
        
        response = client.post("/predict", json=rain_scenario)
        assert response.status_code == 200
        
        data = response.json()
        # Com chuva intensa, risco deve ser maior
        assert data["flood_probability"] > 0.1  # Algum risco detectado

# Função para executar testes
def run_tests():
    """Executa todos os testes"""
    
    print("🧪 EXECUTANDO TESTES DA API")
    print("=" * 50)
    
    # Executa testes com pytest
    pytest.main([
        __file__,
        "-v",
        "--tb=short"
    ])

if __name__ == "__main__":
    run_tests()
