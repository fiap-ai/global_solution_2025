# 🌩️ CENÁRIOS DE TESTE AWS - SISTEMA PREDIÇÃO ENCHENTES

## 🎯 **OBJETIVO**
Criar diferentes condições meteorológicas para demonstrar a versatilidade e precisão do modelo LSTM em cenários variados, validando predições através da API FastAPI.

---

## 🧪 **CENÁRIOS DEFINIDOS**

### **📊 Cenário 1: TEMPO BOM (Normal)**
```json
{
  "scenario_name": "TEMPO_BOM",
  "description": "Condições ideais, sem risco",
  "sensor_data": [
    {
      "precipitation": 0.0,
      "humidity": 60.0,
      "temperature": 25.0,
      "pressure": 1020.0
    }
  ],
  "expected_result": {
    "probability": "< 0.05",
    "risk_level": "LOW",
    "confidence": "> 0.95"
  }
}
```

**🎬 Para Demonstração:**
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "sensor_data": [
      {"precipitation": 0.0, "humidity": 60.0, "temperature": 25.0, "pressure": 1020.0}
    ],
    "device_id": "AWS_TEMPO_BOM",
    "timestamp": "2025-01-17T21:00:00"
  }'
```

---

### **⚠️ Cenário 2: CHUVA FRACA (Monitoramento)**
```json
{
  "scenario_name": "CHUVA_FRACA",
  "description": "Precipitação leve, monitoramento ativo",
  "sensor_data": [
    {
      "precipitation": 3.0,
      "humidity": 75.0,
      "temperature": 22.0,
      "pressure": 1015.0
    }
  ],
  "expected_result": {
    "probability": "0.05 - 0.15",
    "risk_level": "LOW",
    "confidence": "> 0.85"
  }
}
```

**🎬 Para Demonstração:**
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "sensor_data": [
      {"precipitation": 3.0, "humidity": 75.0, "temperature": 22.0, "pressure": 1015.0}
    ],
    "device_id": "AWS_CHUVA_FRACA"
  }'
```

---

### **🟡 Cenário 3: ALERTA MODERADO (Atenção)**
```json
{
  "scenario_name": "ALERTA_MODERADO",
  "description": "Condições que exigem atenção",
  "sensor_data": [
    {
      "precipitation": 8.0,
      "humidity": 85.0,
      "temperature": 20.0,
      "pressure": 1010.0
    }
  ],
  "expected_result": {
    "probability": "0.15 - 0.40",
    "risk_level": "MODERATE",
    "confidence": "> 0.80"
  }
}
```

**🎬 Para Demonstração:**
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "sensor_data": [
      {"precipitation": 8.0, "humidity": 85.0, "temperature": 20.0, "pressure": 1010.0}
    ],
    "device_id": "AWS_ALERTA_MODERADO"
  }'
```

---

### **🔴 Cenário 4: RISCO ALTO (Preparação)**
```json
{
  "scenario_name": "RISCO_ALTO",
  "description": "Tempestade intensa se aproximando",
  "sensor_data": [
    {
      "precipitation": 15.0,
      "humidity": 92.0,
      "temperature": 19.0,
      "pressure": 1008.0
    }
  ],
  "expected_result": {
    "probability": "0.40 - 0.70",
    "risk_level": "HIGH",
    "confidence": "> 0.85"
  }
}
```

**🎬 Para Demonstração:**
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "sensor_data": [
      {"precipitation": 15.0, "humidity": 92.0, "temperature": 19.0, "pressure": 1008.0}
    ],
    "device_id": "AWS_RISCO_ALTO"
  }'
```

---

### **🚨 Cenário 5: CRÍTICO (Evacuação)**
```json
{
  "scenario_name": "CRITICO_EVACUACAO",
  "description": "Enchente iminente - evacuar área",
  "sensor_data": [
    {
      "precipitation": 25.0,
      "humidity": 96.0,
      "temperature": 18.0,
      "pressure": 1005.0
    }
  ],
  "expected_result": {
    "probability": "> 0.70",
    "risk_level": "CRITICAL",
    "confidence": "> 0.90"
  }
}
```

**🎬 Para Demonstração:**
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "sensor_data": [
      {"precipitation": 25.0, "humidity": 96.0, "temperature": 18.0, "pressure": 1005.0}
    ],
    "device_id": "AWS_CRITICO"
  }'
```

---

### **📈 Cenário 6: HISTÓRICO REAL - Teresópolis 2011**
```json
{
  "scenario_name": "TERESOPOLIS_2011",
  "description": "Dados similares à tragédia real",
  "context": "11-12 Janeiro 2011 - Região Serrana RJ",
  "sensor_data": [
    {
      "precipitation": 32.0,
      "humidity": 98.0,
      "temperature": 19.0,
      "pressure": 1002.0
    }
  ],
  "expected_result": {
    "probability": "> 0.85",
    "risk_level": "CRITICAL",
    "confidence": "> 0.95"
  },
  "historical_impact": "900+ vítimas fatais"
}
```

**🎬 Para Demonstração:**
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "sensor_data": [
      {"precipitation": 32.0, "humidity": 98.0, "temperature": 19.0, "pressure": 1002.0}
    ],
    "device_id": "AWS_TERESOPOLIS_2011",
    "timestamp": "2011-01-12T02:00:00"
  }'
```

---

### **📊 Cenário 7: PROGRESSÃO TEMPORAL (24h)**
**Objetivo**: Mostrar evolução do risco ao longo de 24 horas

```json
{
  "scenario_name": "PROGRESSAO_24H",
  "description": "Evolução de tempo bom para crítico",
  "timeline": [
    {"hour": 0, "precipitation": 0.0, "humidity": 65.0, "risk_expected": "LOW"},
    {"hour": 6, "precipitation": 2.0, "humidity": 70.0, "risk_expected": "LOW"},
    {"hour": 12, "precipitation": 8.0, "humidity": 80.0, "risk_expected": "MODERATE"},
    {"hour": 18, "precipitation": 18.0, "humidity": 90.0, "risk_expected": "HIGH"},
    {"hour": 24, "precipitation": 28.0, "humidity": 95.0, "risk_expected": "CRITICAL"}
  ]
}
```

---

## 🎮 **SCRIPT DE DEMONSTRAÇÃO SEQUENCIAL**

### **🚀 Execução Automática de Todos os Cenários**

```bash
#!/bin/bash
# Script: test_all_scenarios.sh

echo "🌩️  TESTANDO TODOS OS CENÁRIOS AWS"
echo "================================="

# Cenário 1: Tempo Bom
echo "📊 Cenário 1: TEMPO BOM"
curl -s -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"sensor_data": [{"precipitation": 0.0, "humidity": 60.0, "temperature": 25.0, "pressure": 1020.0}], "device_id": "AWS_TEMPO_BOM"}' \
  | jq '.flood_probability, .risk_level'

sleep 2

# Cenário 2: Chuva Fraca
echo "⚠️  Cenário 2: CHUVA FRACA"
curl -s -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"sensor_data": [{"precipitation": 3.0, "humidity": 75.0, "temperature": 22.0, "pressure": 1015.0}], "device_id": "AWS_CHUVA_FRACA"}' \
  | jq '.flood_probability, .risk_level'

sleep 2

# Cenário 3: Alerta Moderado
echo "🟡 Cenário 3: ALERTA MODERADO"
curl -s -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"sensor_data": [{"precipitation": 8.0, "humidity": 85.0, "temperature": 20.0, "pressure": 1010.0}], "device_id": "AWS_ALERTA_MODERADO"}' \
  | jq '.flood_probability, .risk_level'

sleep 2

# Cenário 4: Risco Alto
echo "🔴 Cenário 4: RISCO ALTO"
curl -s -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"sensor_data": [{"precipitation": 15.0, "humidity": 92.0, "temperature": 19.0, "pressure": 1008.0}], "device_id": "AWS_RISCO_ALTO"}' \
  | jq '.flood_probability, .risk_level'

sleep 2

# Cenário 5: Crítico
echo "🚨 Cenário 5: CRÍTICO"
curl -s -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"sensor_data": [{"precipitation": 25.0, "humidity": 96.0, "temperature": 18.0, "pressure": 1005.0}], "device_id": "AWS_CRITICO"}' \
  | jq '.flood_probability, .risk_level'

sleep 2

# Cenário 6: Histórico Teresópolis 2011
echo "📈 Cenário 6: TERESÓPOLIS 2011"
curl -s -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"sensor_data": [{"precipitation": 32.0, "humidity": 98.0, "temperature": 19.0, "pressure": 1002.0}], "device_id": "AWS_TERESOPOLIS_2011"}' \
  | jq '.flood_probability, .risk_level'

echo "✅ TESTE COMPLETO FINALIZADO"
```

---

## 📱 **DEMONSTRAÇÃO INTERATIVA BROWSER**

### **Interface Web para Testes**

```html
<!DOCTYPE html>
<html>
<head>
    <title>🌩️ Teste Cenários AWS</title>
    <style>
        .scenario { margin: 20px; padding: 15px; border: 1px solid #ddd; }
        .low { background-color: #e8f5e8; }
        .moderate { background-color: #fff3cd; }
        .high { background-color: #f8d7da; }
        .critical { background-color: #d1ecf1; }
    </style>
</head>
<body>
    <h1>🌩️ Cenários de Teste AWS</h1>
    
    <div class="scenario low">
        <h3>📊 Tempo Bom</h3>
        <button onclick="testScenario('tempo_bom')">Testar</button>
        <div id="result_tempo_bom"></div>
    </div>
    
    <div class="scenario moderate">
        <h3>🟡 Alerta Moderado</h3>
        <button onclick="testScenario('moderado')">Testar</button>
        <div id="result_moderado"></div>
    </div>
    
    <div class="scenario critical">
        <h3>🚨 Crítico</h3>
        <button onclick="testScenario('critico')">Testar</button>
        <div id="result_critico"></div>
    </div>

    <script>
        const scenarios = {
            tempo_bom: {
                precipitation: 0.0, humidity: 60.0, temperature: 25.0, pressure: 1020.0
            },
            moderado: {
                precipitation: 8.0, humidity: 85.0, temperature: 20.0, pressure: 1010.0
            },
            critico: {
                precipitation: 25.0, humidity: 96.0, temperature: 18.0, pressure: 1005.0
            }
        };

        async function testScenario(name) {
            const scenario = scenarios[name];
            const response = await fetch('http://localhost:8000/predict', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    sensor_data: [scenario],
                    device_id: `WEB_${name.toUpperCase()}`
                })
            });
            
            const result = await response.json();
            document.getElementById(`result_${name}`).innerHTML = 
                `<strong>Probabilidade:</strong> ${(result.flood_probability * 100).toFixed(2)}% 
                 <strong>Risco:</strong> ${result.risk_level}`;
        }
    </script>
</body>
</html>
```

---

## 🔍 **VALIDAÇÃO DE RESULTADOS**

### **Métricas Esperadas por Cenário**

| Cenário | Precipitação | Umidade | Probabilidade | Risk Level | Tempo Resposta |
|---------|-------------|---------|---------------|------------|----------------|
| Tempo Bom | 0.0mm | 60% | < 5% | LOW | < 100ms |
| Chuva Fraca | 3.0mm | 75% | 5-15% | LOW | < 100ms |
| Moderado | 8.0mm | 85% | 15-40% | MODERATE | < 100ms |
| Risco Alto | 15.0mm | 92% | 40-70% | HIGH | < 100ms |
| Crítico | 25.0mm | 96% | > 70% | CRITICAL | < 100ms |
| Teresópolis 2011 | 32.0mm | 98% | > 85% | CRITICAL | < 100ms |

---

## 🎬 **ROTEIRO PARA DEMONSTRAÇÃO AO VIVO**

### **Sequência Recomendada (3 minutos)**

#### **Minuto 1: Setup + Tempo Bom**
1. Explicar objetivo dos testes
2. Executar cenário "Tempo Bom"
3. Mostrar probabilidade baixa (~1%)

#### **Minuto 2: Progressão de Risco**
1. Cenário "Moderado" - mostrar aumento
2. Cenário "Alto" - mostrar progressão
3. Destacar como modelo detecta gradualmente

#### **Minuto 3: Crítico + Histórico**
1. Cenário "Crítico" - probabilidade alta
2. Cenário "Teresópolis 2011" - validação histórica
3. Conclusão sobre precisão

---

## 📊 **LOGS E MONITORAMENTO**

### **Rastreamento de Testes**
```json
{
  "test_session": "2025-01-17T21:00:00",
  "scenarios_tested": [
    {
      "scenario": "TEMPO_BOM",
      "timestamp": "2025-01-17T21:01:00",
      "input": {"precipitation": 0.0, "humidity": 60.0},
      "output": {"probability": 0.0012, "risk_level": "LOW"},
      "response_time_ms": 45,
      "status": "PASS"
    }
  ],
  "summary": {
    "total_tests": 6,
    "passed": 6,
    "avg_response_time": 52,
    "accuracy_validation": "CONFIRMED"
  }
}
```

---

## 🎯 **PRÓXIMOS PASSOS**

### **Integração AWS Real**
1. **Lambda Function** para processar cenários
2. **CloudWatch** para logs de teste
3. **API Gateway** para acesso externo
4. **S3** para armazenar resultados

### **Automação de Testes**
1. **Script CI/CD** para execução automática
2. **Alertas** se resultados não esperados
3. **Dashboard** de monitoramento contínuo
4. **Relatórios** de performance

---

**🌩️ Este documento garante testes abrangentes e demonstrações convincentes da precisão do modelo em diferentes condições meteorológicas.**
