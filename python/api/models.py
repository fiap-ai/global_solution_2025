#!/usr/bin/env python3
"""
Pydantic Models - Flood Prediction API
Modelos de dados para validação da API.
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime
import numpy as np

class SensorReading(BaseModel):
    """Leitura individual de sensor (1 hora)"""
    
    precipitation: float = Field(
        ..., 
        ge=0.0, 
        le=300.0,
        description="Precipitação horária em mm"
    )
    humidity: float = Field(
        ..., 
        ge=0.0, 
        le=100.0,
        description="Umidade relativa em %"
    )
    temperature: float = Field(
        ..., 
        ge=-20.0, 
        le=50.0,
        description="Temperatura do ar em °C"
    )
    pressure: float = Field(
        ..., 
        ge=800.0, 
        le=1100.0,
        description="Pressão atmosférica em mB"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "precipitation": 15.5,
                "humidity": 85.2,
                "temperature": 24.8,
                "pressure": 1013.2
            }
        }

class PredictionRequest(BaseModel):
    """Requisição de predição com dados de 24h"""
    
    sensor_data: List[SensorReading] = Field(
        ...,
        min_items=24,
        max_items=24,
        description="Dados de 24 horas consecutivas"
    )
    timestamp: Optional[str] = Field(
        None,
        description="Timestamp da predição (ISO format)"
    )
    device_id: Optional[str] = Field(
        "unknown",
        description="ID do dispositivo ESP32"
    )
    
    @validator('sensor_data')
    def validate_sensor_data_length(cls, v):
        if len(v) != 24:
            raise ValueError('Exatamente 24 leituras são necessárias (24 horas)')
        return v
    
    @validator('timestamp')
    def validate_timestamp(cls, v):
        if v is not None:
            try:
                datetime.fromisoformat(v.replace('Z', '+00:00'))
            except ValueError:
                raise ValueError('Timestamp deve estar no formato ISO')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "sensor_data": [
                    {
                        "precipitation": 0.0,
                        "humidity": 65.0,
                        "temperature": 22.5,
                        "pressure": 1015.0
                    }
                ] * 24,  # 24 horas de dados
                "timestamp": "2025-06-17T19:30:00",
                "device_id": "ESP32_001"
            }
        }

class PredictionResponse(BaseModel):
    """Resposta da predição"""
    
    flood_probability: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Probabilidade de enchente (0-1)"
    )
    risk_level: str = Field(
        ...,
        description="Nível de risco: LOW, MEDIUM, HIGH, CRITICAL"
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confiança da predição (0-1)"
    )
    timestamp: str = Field(
        ...,
        description="Timestamp da predição"
    )
    device_id: str = Field(
        ...,
        description="ID do dispositivo"
    )
    model_version: str = Field(
        "1.0.0",
        description="Versão do modelo"
    )
    processing_time_ms: Optional[float] = Field(
        None,
        description="Tempo de processamento em ms"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "flood_probability": 0.75,
                "risk_level": "HIGH",
                "confidence": 0.85,
                "timestamp": "2025-06-17T19:30:00",
                "device_id": "ESP32_001",
                "model_version": "1.0.0",
                "processing_time_ms": 45.2
            }
        }

class HealthResponse(BaseModel):
    """Resposta do status de saúde"""
    
    status: str = Field(..., description="Status da API: healthy, degraded, unhealthy")
    model_loaded: bool = Field(..., description="Se o modelo está carregado")
    model_version: str = Field(..., description="Versão do modelo")
    uptime_seconds: float = Field(..., description="Tempo de atividade em segundos")
    last_prediction: Optional[str] = Field(None, description="Timestamp da última predição")
    total_predictions: int = Field(0, description="Total de predições realizadas")
    
    class Config:
        schema_extra = {
            "example": {
                "status": "healthy",
                "model_loaded": True,
                "model_version": "1.0.0",
                "uptime_seconds": 3600.5,
                "last_prediction": "2025-06-17T19:25:00",
                "total_predictions": 142
            }
        }

class ErrorResponse(BaseModel):
    """Resposta de erro"""
    
    error: str = Field(..., description="Tipo do erro")
    message: str = Field(..., description="Mensagem detalhada")
    timestamp: str = Field(..., description="Timestamp do erro")
    
    class Config:
        schema_extra = {
            "example": {
                "error": "ValidationError",
                "message": "Dados de entrada inválidos",
                "timestamp": "2025-06-17T19:30:00"
            }
        }

class APIInfo(BaseModel):
    """Informações da API"""
    
    name: str = "Flood Prediction API"
    version: str = "1.0.0"
    description: str = "API para predição de enchentes usando LSTM"
    model_type: str = "LSTM"
    input_features: List[str] = ["precipitation", "humidity", "temperature", "pressure"]
    sequence_length: int = 24
    endpoints: List[str] = ["/health", "/predict", "/docs"]
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Flood Prediction API",
                "version": "1.0.0",
                "description": "API para predição de enchentes usando LSTM",
                "model_type": "LSTM",
                "input_features": ["precipitation", "humidity", "temperature", "pressure"],
                "sequence_length": 24,
                "endpoints": ["/health", "/predict", "/docs"]
            }
        }

# Função utilitária para converter dados do ESP32
def esp32_to_sensor_reading(esp32_data: dict) -> SensorReading:
    """Converte dados do formato ESP32 para SensorReading"""
    
    # Mapeia campos do ESP32 para nomes padrão
    field_mapping = {
        'water_level': 'precipitation',  # Conversão aproximada
        'humidity': 'humidity',
        'temperature': 'temperature',
        'pressure': 'pressure'
    }
    
    mapped_data = {}
    for esp32_field, api_field in field_mapping.items():
        if esp32_field in esp32_data:
            mapped_data[api_field] = esp32_data[esp32_field]
    
    # Se faltarem campos, preenche com valores padrão
    defaults = {
        'precipitation': 0.0,
        'humidity': 50.0,
        'temperature': 20.0,
        'pressure': 1013.25
    }
    
    for field, default_value in defaults.items():
        if field not in mapped_data:
            mapped_data[field] = default_value
    
    return SensorReading(**mapped_data)

# Função para determinar nível de risco
def get_risk_level(probability: float) -> str:
    """Determina nível de risco baseado na probabilidade"""
    
    if probability >= 0.8:
        return "CRITICAL"
    elif probability >= 0.6:
        return "HIGH"
    elif probability >= 0.3:
        return "MEDIUM"
    else:
        return "LOW"

# Função para calcular confiança
def calculate_confidence(probability: float) -> float:
    """Calcula confiança baseada na distância de 0.5"""
    
    # Confiança é maior quando a probabilidade está longe de 0.5
    distance_from_center = abs(probability - 0.5)
    confidence = distance_from_center * 2  # Normaliza para 0-1
    
    # Garante que confiança está entre 0.5 e 1.0
    confidence = max(0.5, min(1.0, confidence + 0.5))
    
    return confidence
