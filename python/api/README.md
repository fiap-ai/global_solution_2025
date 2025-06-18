# 🚀 Flood Prediction API - FastAPI Module

## 🎯 Descrição
API REST para predição de enchentes em tempo real usando modelo LSTM treinado. Recebe dados meteorológicos de 24h e retorna probabilidade de enchente e nível de risco.

## 🚀 Quick Start
```bash
# Setup ambiente único
cd python/
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Executar API
pip install -r api/requirements.txt
uvicorn api.main:app --reload --port 8000

# Testar API
curl http://localhost:8000/health
```

## 📋 Pré-requisitos
- **Python 3.8+** (mesmo do módulo flood_prediction)
- **Modelo treinado** (deve executar `python/flood_prediction/train.py` primeiro)
- **8GB+ RAM** (para carregar modelo TensorFlow)
- **Porta 8000 livre** (ou configurar outra porta)

## 📁 Estrutura do Módulo
```
api/
├── requirements.txt        # Dependências FastAPI, TensorFlow, etc.
├── README.md              # Esta documentação
├── models.py              # Validação Pydantic dos dados
├── main.py                # Aplicação FastAPI principal
└── test_api.py            # Testes automatizados
```

## 🌐 Endpoints Disponíveis

### 📍 **GET /** - Informações da API
```bash
curl http://localhost:8000/
```
**Resposta:**
```json
{
  "name": "Flood Prediction API",
  "version": "1.0.0",
  "description": "API para predição de enchentes usando LSTM",
  "model_type": "LSTM",
  "input_features": ["precipitation", "humidity", "temperature", "pressure"],
  "sequence_length": 24,
  "endpoints": ["/health", "/predict", "/docs"]
}
```

### 🏥 **GET /health** - Status do Sistema
```bash
curl http://localhost:8000/health
```
**Resposta:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_version": "1.0.0",
  "uptime_seconds": 3600.5,
  "last_prediction": "2025-06-17T19:25:00",
  "total_predictions": 142
}
```

### 🌧️ **POST /predict** - Predição Principal
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "sensor_data": [
      {
        "precipitation": 15.5,
        "humidity": 85.2,
        "temperature": 24.8,
        "pressure": 1013.2
      }
    ],
    "device_id": "ESP32_001",
    "timestamp": "2025-06-17T19:30:00"
  }'
```
**Resposta:**
```json
{
  "flood_probability": 0.75,
  "risk_level": "HIGH",
  "confidence": 0.85,
  "timestamp": "2025-06-17T19:30:00",
  "device_id": "ESP32_001",
  "model_version": "1.0.0",
  "processing_time_ms": 45.2
}
```

### 🔧 **POST /predict/esp32** - Formato ESP32
```bash
curl -X POST http://localhost:8000/predict/esp32 \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "ESP32_001",
    "timestamp": "2025-06-17T19:30:00",
    "sensor_history": [
      {
        "water_level": 0.0,
        "humidity": 65.0,
        "temperature": 22.0,
        "pressure": 1015.0
      }
    ]
  }'
```

### 🧪 **GET /test/predict** - Teste Automático
```bash
curl http://localhost:8000/test/predict
```
**Resposta:**
```json
{
  "test_results": {
    "normal_scenario": {
      "probability": 0.15,
      "risk_level": "LOW"
    },
    "flood_scenario": {
      "probability": 0.85,
      "risk_level": "HIGH"
    }
  },
  "model_working": true
}
```

### 📚 **GET /docs** - Documentação Swagger
Abra no navegador: `http://localhost:8000/docs`

## ⚙️ Setup Detalhado

### 1. Preparar Ambiente
```bash
# Setup ambiente único
cd python/
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Verificar Python
python --version  # Deve ser 3.8+
```

### 2. Instalar Dependências
```bash
# Instalar requirements específicos
pip install -r api/requirements.txt

# Verificar instalações principais
python -c "import fastapi; print(f'FastAPI: {fastapi.__version__}')"
python -c "import tensorflow as tf; print(f'TensorFlow: {tf.__version__}')"
python -c "import uvicorn; print('Uvicorn: OK')"
```

### 3. Verificar Modelo Treinado
```bash
# Verificar se modelo existe
ls ../../data/models/flood_lstm_model.h5
ls ../../data/models/flood_scaler.pkl

# Se não existir, treinar primeiro:
# cd ../flood_prediction
# python train.py
# cd ../api
```

## 🔧 Como Usar

### Passo 1: Rodar API
```bash
# Método 1: Desenvolvimento (com reload automático)
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Método 2: Produção (sem reload)
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 1

# Método 3: Executar diretamente
python main.py
```

**Resultado esperado:**
```
🚀 Iniciando Flood Prediction API...
✅ Modelo carregado: ../../data/models/flood_lstm_model.h5
✅ Scaler carregado: ../../data/models/flood_scaler.pkl
✅ API pronta para uso!

INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using statreload
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Passo 2: Testar Endpoints

#### Teste 1: Verificar Status
```bash
curl http://localhost:8000/health
```

#### Teste 2: Predição Simples
```bash
# Criar arquivo de teste
cat > test_normal.json << EOF
{
  "sensor_data": [
    {
      "precipitation": 0.0,
      "humidity": 65.0,
      "temperature": 22.0,
      "pressure": 1015.0
    }
  ] * 24,
  "device_id": "TEST_NORMAL"
}
EOF

# Fazer predição
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d @test_normal.json
```

#### Teste 3: Cenário de Chuva
```bash
# Criar cenário de chuva intensa
cat > test_rain.json << EOF
{
  "sensor_data": [
    {
      "precipitation": 25.0,
      "humidity": 95.0,
      "temperature": 24.0,
      "pressure": 1005.0
    }
  ] * 24,
  "device_id": "TEST_RAIN"
}
EOF

# Fazer predição
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d @test_rain.json
```

## ✅ Como Testar

### Teste 1: Testes Automatizados
```bash
# Executar todos os testes
python test_api.py

# OU usar pytest
pip install pytest httpx
pytest test_api.py -v
```

**Resultado esperado:**
```
🧪 EXECUTANDO TESTES DA API
==================================================
test_api.py::TestFloodPredictionAPI::test_root_endpoint PASSED
test_api.py::TestFloodPredictionAPI::test_health_endpoint PASSED
test_api.py::TestFloodPredictionAPI::test_predict_endpoint_valid_data PASSED
test_api.py::TestFloodPredictionAPI::test_predict_endpoint_invalid_data PASSED
test_api.py::TestFloodPredictionAPI::test_model_info_endpoint PASSED
test_api.py::TestFloodPredictionAPI::test_test_predict_endpoint PASSED

============================== 6 passed ==============================
```

### Teste 2: Teste Manual via Browser
1. Abrir: `http://localhost:8000/docs`
2. Testar endpoint `/health`
3. Testar endpoint `/predict` com dados de exemplo
4. Verificar `/test/predict`

### Teste 3: Teste de Carga
```bash
# Instalar Apache Bench
# Ubuntu: sudo apt install apache2-utils
# Mac: brew install httpie

# Teste de 100 requests
ab -n 100 -c 10 http://localhost:8000/health

# Teste com POST
echo '{"sensor_data":[{"precipitation":0,"humidity":65,"temperature":22,"pressure":1015}]}' > test.json
ab -n 50 -c 5 -p test.json -T application/json http://localhost:8000/predict
```

## 📊 Interpretação das Respostas

### Níveis de Risco
- **LOW** (0.0 - 0.3): Condições normais, sem risco
- **MEDIUM** (0.3 - 0.6): Atenção, monitorar condições
- **HIGH** (0.6 - 0.8): Risco elevado, preparar ações
- **CRITICAL** (0.8 - 1.0): Risco iminente, ações imediatas

### Confiança (Confidence)
- **> 0.8**: Predição muito confiável
- **0.6 - 0.8**: Predição confiável
- **< 0.6**: Predição com incerteza

### Tempo de Processamento
- **< 100ms**: Performance excelente
- **100-500ms**: Performance boa
- **> 500ms**: Verificar recursos do servidor

## 🐛 Troubleshooting

### Erro: "Modelo não está carregado"
```bash
# Verificar se modelo existe
ls ../../data/models/flood_lstm_model.h5

# Se não existe, treinar primeiro
cd ../flood_prediction
python train.py
cd ../api

# Reiniciar API
uvicorn main:app --reload
```

### Erro: "Address already in use"
```bash
# Porta 8000 ocupada, usar outra
uvicorn main:app --reload --port 8001

# OU matar processo na porta 8000
lsof -ti:8000 | xargs kill -9  # Linux/Mac
```

### Erro: "Validation Error" na predição
```bash
# Verificar formato dos dados
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "sensor_data": [  # Deve ter exatamente 24 elementos
      {"precipitation": 0, "humidity": 65, "temperature": 22, "pressure": 1015}
    ]
  }'
```

### API lenta ou travando
```bash
# Verificar uso de memória
python -c "
import psutil
print(f'RAM: {psutil.virtual_memory().percent}%')
print(f'CPU: {psutil.cpu_percent()}%')
"

# Reduzir workers se necessário
uvicorn main:app --workers 1 --max-workers 1
```

### Performance baixa
- **Latência alta**: Verificar se modelo está em GPU/CPU adequado
- **Memory leaks**: Reiniciar API periodicamente em produção
- **Timeout**: Aumentar timeout do cliente HTTP

## 🔒 Configurações de Produção

### Variáveis de Ambiente
```bash
# Criar arquivo .env
cat > .env << EOF
API_HOST=0.0.0.0
API_PORT=8000
MODEL_PATH=../../data/models/flood_lstm_model.h5
SCALER_PATH=../../data/models/flood_scaler.pkl
LOG_LEVEL=INFO
CORS_ORIGINS=*
EOF
```

### Deploy com Docker (opcional)
```dockerfile
# Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Nginx Reverse Proxy (opcional)
```nginx
# /etc/nginx/sites-available/flood-api
server {
    listen 80;
    server_name flood-api.local;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 📊 Monitoramento

### Logs da API
```bash
# Logs em tempo real
tail -f /var/log/flood-api.log

# Filtrar por nível
grep "ERROR" /var/log/flood-api.log
grep "prediction" /var/log/flood-api.log
```

### Métricas de Performance
```bash
# Dentro da API (implementar endpoints de métricas)
curl http://localhost:8000/metrics
```

## 🔗 Integração com Outros Módulos

### Com ESP32
- ESP32 envia dados via HTTP POST para `/predict/esp32`
- Formato adaptado automaticamente para API padrão
- Resposta processada pelo ESP32 para alertas locais

### Com AWS Lambda
- Lambda chama endpoint `/predict` com dados dos sensores
- API retorna predição para processamento na nuvem
- Integração via requests HTTP simples

### Com Dashboard
- Frontend consome endpoints da API
- Dados em tempo real via polling ou WebSockets
- Visualizações baseadas nas respostas da API

## 📞 Suporte e Debugging

### Logs Detalhados
- API gera logs estruturados automaticamente
- Cada predição é logada com timestamp e device_id
- Erros incluem stack trace completo

### Debug Mode
```bash
# Rodar em modo debug
export PYTHONPATH=.
python -m debugpy --listen 5678 --wait-for-client main.py
```

### Health Checks
- Endpoint `/health` sempre disponível
- Verifica status do modelo e estatísticas
- Usado para monitoramento automático

---

**🎯 A API está pronta para integração com ESP32 e AWS!**
