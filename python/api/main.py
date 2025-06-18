#!/usr/bin/env python3
"""
FastAPI Main - Flood Prediction API
Aplicação principal da API para predição de enchentes.
"""

import os
import time
import logging
from datetime import datetime
from typing import Optional
import asyncio
import numpy as np
import joblib
import tensorflow as tf

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from models import (
    PredictionRequest, PredictionResponse, HealthResponse, 
    ErrorResponse, APIInfo, get_risk_level, calculate_confidence
)

# Configuração de logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FloodPredictionAPI:
    """Classe principal da API de predição de enchentes"""
    
    def __init__(self):
        self.model = None
        self.scaler = None
        self.model_version = "1.0.0"
        self.start_time = time.time()
        self.prediction_count = 0
        self.last_prediction_time = None
        
        # Caminhos dos artefatos
        self.model_path = "../data/models/flood_lstm_model.h5"
        self.scaler_path = "../data/models/flood_scaler.pkl"
        
    def load_model_artifacts(self):
        """Carrega modelo e scaler"""
        
        try:
            # Carrega modelo
            if os.path.exists(self.model_path):
                self.model = tf.keras.models.load_model(self.model_path)
                logger.info(f"✅ Modelo carregado: {self.model_path}")
            else:
                logger.warning(f"⚠️  Modelo não encontrado: {self.model_path}")
                
            # Carrega scaler
            if os.path.exists(self.scaler_path):
                self.scaler = joblib.load(self.scaler_path)
                logger.info(f"✅ Scaler carregado: {self.scaler_path}")
            else:
                logger.warning(f"⚠️  Scaler não encontrado: {self.scaler_path}")
                
        except Exception as e:
            logger.error(f"❌ Erro ao carregar artefatos: {str(e)}")
            
    def is_model_ready(self) -> bool:
        """Verifica se modelo está pronto para uso"""
        return self.model is not None and self.scaler is not None
    
    def preprocess_data(self, sensor_data: list) -> np.ndarray:
        """Preprocessa dados de entrada"""
        
        # Converte para numpy array
        data_array = np.array([[
            reading.precipitation,
            reading.humidity, 
            reading.temperature,
            reading.pressure
        ] for reading in sensor_data])
        
        # Normaliza usando scaler treinado
        data_scaled = self.scaler.transform(data_array)
        
        # Reshape para formato LSTM: (1, 24, 4)
        data_lstm = data_scaled.reshape(1, 24, 4)
        
        return data_lstm
    
    async def predict_flood(self, request: PredictionRequest) -> PredictionResponse:
        """Faz predição de enchente"""
        
        start_time = time.time()
        
        if not self.is_model_ready():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Modelo não está carregado"
            )
        
        try:
            # Preprocessa dados
            processed_data = self.preprocess_data(request.sensor_data)
            
            # Faz predição
            probability = float(self.model.predict(processed_data)[0][0])
            
            # Calcula métricas
            risk_level = get_risk_level(probability)
            confidence = calculate_confidence(probability)
            
            # Estatísticas
            processing_time = (time.time() - start_time) * 1000
            self.prediction_count += 1
            self.last_prediction_time = datetime.now().isoformat()
            
            response = PredictionResponse(
                flood_probability=probability,
                risk_level=risk_level,
                confidence=confidence,
                timestamp=request.timestamp or datetime.now().isoformat(),
                device_id=request.device_id,
                model_version=self.model_version,
                processing_time_ms=processing_time
            )
            
            logger.info(f"Predição realizada: P={probability:.3f}, Risk={risk_level}, Device={request.device_id}")
            
            return response
            
        except Exception as e:
            logger.error(f"Erro na predição: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno na predição: {str(e)}"
            )
    
    def get_health_status(self) -> HealthResponse:
        """Retorna status de saúde da API"""
        
        uptime = time.time() - self.start_time
        model_loaded = self.is_model_ready()
        
        if model_loaded:
            status_value = "healthy"
        else:
            status_value = "degraded"
            
        return HealthResponse(
            status=status_value,
            model_loaded=model_loaded,
            model_version=self.model_version,
            uptime_seconds=uptime,
            last_prediction=self.last_prediction_time,
            total_predictions=self.prediction_count
        )

# Instância global da API
flood_api = FloodPredictionAPI()

# Aplicação FastAPI
app = FastAPI(
    title="Flood Prediction API",
    description="API para predição de enchentes usando modelo LSTM treinado com dados do INMET",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar domínios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Event handlers
@app.on_event("startup")
async def startup_event():
    """Inicialização da aplicação"""
    logger.info("🚀 Iniciando Flood Prediction API...")
    flood_api.load_model_artifacts()
    
    if flood_api.is_model_ready():
        logger.info("✅ API pronta para uso!")
    else:
        logger.warning("⚠️  API iniciada sem modelo carregado")

@app.on_event("shutdown")
async def shutdown_event():
    """Finalização da aplicação"""
    logger.info("🛑 Encerrando Flood Prediction API...")

# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.__class__.__name__,
            message=str(exc.detail),
            timestamp=datetime.now().isoformat()
        ).dict()
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Erro não tratado: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error=exc.__class__.__name__,
            message="Erro interno do servidor",
            timestamp=datetime.now().isoformat()
        ).dict()
    )

# Endpoints
@app.get("/", response_model=APIInfo)
async def root():
    """Informações básicas da API"""
    return APIInfo()

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Verificação de saúde da API"""
    return flood_api.get_health_status()

@app.post("/predict", response_model=PredictionResponse)
async def predict_flood(request: PredictionRequest):
    """
    Prediz risco de enchente baseado em dados meteorológicos de 24h
    
    - **sensor_data**: Lista com 24 leituras horárias de sensores
    - **timestamp**: Timestamp da predição (opcional)
    - **device_id**: ID do dispositivo ESP32 (opcional)
    
    Retorna probabilidade de enchente e nível de risco.
    """
    return await flood_api.predict_flood(request)

@app.post("/predict/esp32")
async def predict_flood_esp32(esp32_data: dict):
    """
    Endpoint específico para dados do ESP32
    Converte formato ESP32 para formato padrão da API
    """
    
    try:
        # Simula conversão de dados ESP32 (adaptável conforme necessário)
        if "sensor_history" in esp32_data and len(esp32_data["sensor_history"]) >= 24:
            
            from models import esp32_to_sensor_reading
            
            # Converte últimas 24 leituras
            sensor_readings = []
            for reading in esp32_data["sensor_history"][-24:]:
                sensor_readings.append(esp32_to_sensor_reading(reading))
            
            # Cria requisição padrão
            standard_request = PredictionRequest(
                sensor_data=sensor_readings,
                device_id=esp32_data.get("device_id", "ESP32_Unknown"),
                timestamp=esp32_data.get("timestamp")
            )
            
            return await flood_api.predict_flood(standard_request)
            
        else:
            raise HTTPException(
                status_code=400,
                detail="Dados ESP32 inválidos: necessário 'sensor_history' com 24 leituras"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Erro ao processar dados ESP32: {str(e)}"
        )

@app.get("/model/info")
async def model_info():
    """Informações sobre o modelo carregado"""
    
    if not flood_api.is_model_ready():
        raise HTTPException(
            status_code=503,
            detail="Modelo não carregado"
        )
    
    try:
        model_summary = []
        flood_api.model.summary(print_fn=lambda x: model_summary.append(x))
        
        return {
            "model_loaded": True,
            "model_version": flood_api.model_version,
            "input_shape": str(flood_api.model.input_shape),
            "output_shape": str(flood_api.model.output_shape),
            "total_params": flood_api.model.count_params(),
            "model_summary": model_summary[:10],  # Primeiras 10 linhas
            "scaler_loaded": flood_api.scaler is not None
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao obter informações do modelo: {str(e)}"
        )

# Endpoint para teste rápido
@app.get("/test/predict")
async def test_prediction():
    """Endpoint para teste rápido com dados simulados"""
    
    # Dados simulados de condição normal
    normal_data = [
        {
            "precipitation": 0.0,
            "humidity": 65.0,
            "temperature": 22.0,
            "pressure": 1015.0
        }
    ] * 24
    
    # Dados simulados de risco de enchente
    flood_data = [
        {
            "precipitation": 25.0 if i > 18 else 0.0,  # Chuva intensa nas últimas horas
            "humidity": 95.0 if i > 18 else 70.0,
            "temperature": 24.0,
            "pressure": 1008.0 if i > 18 else 1015.0
        }
        for i in range(24)
    ]
    
    try:
        from models import SensorReading
        
        # Testa cenário normal
        normal_readings = [SensorReading(**data) for data in normal_data]
        normal_request = PredictionRequest(
            sensor_data=normal_readings,
            device_id="TEST_NORMAL"
        )
        normal_result = await flood_api.predict_flood(normal_request)
        
        # Testa cenário de risco
        flood_readings = [SensorReading(**data) for data in flood_data]
        flood_request = PredictionRequest(
            sensor_data=flood_readings,
            device_id="TEST_FLOOD"
        )
        flood_result = await flood_api.predict_flood(flood_request)
        
        return {
            "test_results": {
                "normal_scenario": {
                    "probability": normal_result.flood_probability,
                    "risk_level": normal_result.risk_level
                },
                "flood_scenario": {
                    "probability": flood_result.flood_probability,
                    "risk_level": flood_result.risk_level
                }
            },
            "model_working": True
        }
        
    except Exception as e:
        return {
            "test_results": None,
            "model_working": False,
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    
    # Configurações de desenvolvimento
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
