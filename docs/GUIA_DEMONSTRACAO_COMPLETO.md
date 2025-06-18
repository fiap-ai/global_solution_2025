# 🎬 GUIA DE DEMONSTRAÇÃO COMPLETA
## Sistema de Predição de Enchentes - Global Solution 2025

### 📋 **PREPARAÇÃO PRÉ-DEMONSTRAÇÃO**

#### ✅ **Checklist de Ambiente**
- [ ] Terminal com venv ativado: `cd python && source venv/bin/activate`
- [ ] Browser com abas abertas:
  - [ ] Wokwi: https://wokwi.com/projects/434060150016336897
  - [ ] API Docs: http://localhost:8000/docs
  - [ ] GitHub: (será atualizado na entrega)
- [ ] Arquivos para exibir:
  - [ ] `docs/RESULTADOS_MODELO_LSTM.md`
  - [ ] `data/models/training_results.json`
  - [ ] `data/models/plots/training_history.png`
- [ ] Comandos testados previamente (todos funcionando)

#### 🚀 **Setup Rápido (2 minutos antes da gravação)**
```bash
# 1. Ativar ambiente
cd python && source venv/bin/activate

# 2. Iniciar API (em background)
python api/main.py &

# 3. Verificar se tudo funciona
curl http://localhost:8000/health
# Deve retornar: {"status":"healthy","model_loaded":true}

# 4. Abrir Wokwi no browser
# 5. Preparar slides/docs
```

---

## 🎥 **ROTEIRO CRONOMETRADO - 5 MINUTOS**

### 🎬 **MINUTO 1 (00:00-01:00): ABERTURA + CONTEXTO**

#### **[00:00-00:15] Apresentação**
**TELA**: Slide com logo FIAP + título do projeto  
**FALA**: 
> "Olá! Sou Gabriel Mule Monteiro, RM XXXXX, e vou apresentar nosso sistema de predição de enchentes desenvolvido para a Global Solution 2025. O problema das enchentes urbanas é crítico - só em 2011, Teresópolis e Nova Friburgo tiveram mais de 900 vítimas por falta de alertas precoces."

#### **[00:15-00:30] Problema e Solução**
**TELA**: Estatísticas de enchentes + imagens de satélite coletadas  
**FALA**: 
> "Nossa solução integra IoT, Inteligência Artificial e Cloud Computing para detectar riscos 24 horas antes da enchente acontecer, permitindo evacuação preventiva e salvando vidas."

#### **[00:30-01:00] Arquitetura Overview**
**TELA**: Diagrama de arquitetura (README.md)  
**FALA**: 
> "O sistema tem 3 camadas: ESP32 com sensores físicos, Python com modelo LSTM treinado com dados reais do INMET, e AWS para escalabilidade. Vamos ver cada componente funcionando."

---

### 🎬 **MINUTO 2 (01:00-02:00): ESP32 + SENSORES IOT**

#### **[01:00-01:15] Simulação Wokwi**
**TELA**: Wokwi - https://wokwi.com/projects/417497659530992641  
**AÇÃO**: Clicar "▶️ Start Simulation"  
**FALA**: 
> "Nosso ESP32 monitora 4 sensores críticos em tempo real. Vou iniciar a simulação para mostrar o funcionamento."

#### **[01:15-01:30] Demonstração dos Sensores**
**TELA**: Wokwi rodando - focar no LCD e sensores  
**DEMONSTRAR**:
- HC-SR04: "Sensor ultrassônico mede nível da água - aqui mostra 25cm, situação normal"
- DHT22: "Temperatura 22°C, umidade 65% - condições estáveis"
- PIR: "Sensor de movimento para detectar pessoas na área de risco"
- LDR: "Luminosidade para identificar tempestades"

**FALA**: 
> "O LCD mostra todos os dados em tempo real. Vamos modificar os valores para simular uma situação crítica."

#### **[01:30-02:00] Simulação de Alerta**
**TELA**: Modificar sensores no Wokwi  
**AÇÃO**: 
- Alterar DHT22: umidade para 95%
- Alterar distância para 10cm (nível água alto)
**MOSTRAR**: 
- LED vermelho acende
- Buzzer toca 3 vezes
- LCD mostra "CRÍTICO!"

**FALA**: 
> "Quando detecta risco, o sistema alerta imediatamente: LED vermelho, buzzer de emergência e display crítico. Mas o verdadeiro poder está na predição inteligente."

---

### 🎬 **MINUTO 3 (02:00-03:00): MODELO LSTM + DADOS REAIS**

#### **[02:00-02:20] Dados de Treinamento**
**TELA**: Terminal + arquivo `data/processed/inmet_stats.json`  
**FALA**: 
> "Treinamos um modelo LSTM com dados reais: 72.651 sequências de 24 horas das estações meteorológicas de Teresópolis e Nova Friburgo, cobrindo 4 anos de histórico do INMET de 2021 a 2025."

#### **[02:20-02:40] Resultados Excepcionais**
**TELA**: `docs/RESULTADOS_MODELO_LSTM.md` + `training_history.png`  
**MOSTRAR**:
- Accuracy: 99.2%
- Precision: 100% (zero falsos positivos!)
- Confusion Matrix
- Training history graph

**FALA**: 
> "Os resultados superaram expectativas: 99.2% de accuracy e precision perfeita - zero falsos alarmes! Isso significa confiabilidade total para autoridades e população."

#### **[02:40-03:00] Dados DisastersCharter**
**TELA**: `data/disasters_charter/` + imagens de satélite  
**FALA**: 
> "Além do INMET, coletamos 27 eventos reais de enchentes do DisastersCharter.org, incluindo imagens de satélite de antes e depois dos desastres para validação."

---

### 🎬 **MINUTO 4 (03:00-04:00): API FASTAPI + PREDIÇÕES**

#### **[03:00-03:15] API Health Check**
**TELA**: Terminal com split screen  
**COMANDO**: `curl http://localhost:8000/health`  
**MOSTRAR SAÍDA**:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_version": "1.0.0",
  "uptime_seconds": 120.5
}
```
**FALA**: 
> "A API FastAPI serve o modelo em produção. Health check confirma: sistema saudável, modelo carregado e operacional."

#### **[03:15-03:35] Teste Automático**
**COMANDO**: `curl http://localhost:8000/test/predict`  
**MOSTRAR SAÍDA**:
```json
{
  "test_results": {
    "normal_scenario": {
      "probability": 0.0014,
      "risk_level": "LOW"
    },
    "flood_scenario": {
      "probability": 0.9924,
      "risk_level": "CRITICAL"
    }
  },
  "model_working": true
}
```
**FALA**: 
> "Teste automático compara cenários: condições normais resultam em 0.14% de risco, enquanto tempestade intensa dispara 99.24% - discriminação perfeita!"

#### **[03:35-04:00] Interface Swagger**
**TELA**: Browser - http://localhost:8000/docs  
**AÇÃO**: 
1. Expandir endpoint `/predict`
2. Clicar "Try it out"
3. Mostrar JSON schema
4. Executar predição manual

**FALA**: 
> "Interface Swagger permite testes interativos. Qualquer desenvolvedor pode integrar facilmente. Tempo de resposta: menos de 100 milissegundos."

---

### 🎬 **MINUTO 5 (04:00-05:00): INTEGRAÇÃO AWS + CONCLUSÃO**

#### **[04:00-04:20] AWS IoT Core**
**TELA**: Arquivos em `aws/iot/`  
**MOSTRAR**:
- Certificados X.509
- Policy configurada
- Thing "FloodMonitor01" criado

**FALA**: 
> "Integração com AWS IoT Core permite escalabilidade global. Certificados de segurança configurados, device registrado e pronto para envio de dados em tempo real."

#### **[04:20-04:40] Fluxo Completo**
**TELA**: Diagrama de fluxo de dados  
**EXPLICAR**:
1. ESP32 coleta dados sensors
2. Envia via WiFi para AWS IoT
3. Lambda processa e chama API
4. Modelo LSTM faz predição
5. Resultado retorna para alertas

**FALA**: 
> "O fluxo completo funciona: ESP32 → AWS → API → Predição → Alerta. Sistema end-to-end operacional."

#### **[04:40-05:00] Impacto e Conclusão**
**TELA**: Resultados consolidados + métricas  
**FALA**: 
> "Entregamos um MVP funcional que pode salvar vidas: 99.2% de accuracy, zero falsos alarmes, alertas 24h antecipados. Sistema validado com dados reais, pronto para implantação em qualquer cidade do Brasil. Obrigado!"

---

## 🎯 **CENÁRIOS DE TESTE DETALHADOS**

### **Cenário A: Condição Normal (24h estáveis)**
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "sensor_data": [
      {"precipitation": 0.0, "humidity": 65.0, "temperature": 22.0, "pressure": 1015.0},
      {"precipitation": 0.0, "humidity": 64.0, "temperature": 22.5, "pressure": 1015.2},
      {"precipitation": 0.0, "humidity": 63.0, "temperature": 23.0, "pressure": 1015.1},
      {"precipitation": 0.0, "humidity": 62.0, "temperature": 23.5, "pressure": 1015.3},
      {"precipitation": 0.0, "humidity": 61.0, "temperature": 24.0, "pressure": 1015.4},
      {"precipitation": 0.0, "humidity": 60.0, "temperature": 24.5, "pressure": 1015.5},
      {"precipitation": 0.0, "humidity": 59.0, "temperature": 25.0, "pressure": 1015.6},
      {"precipitation": 0.0, "humidity": 58.0, "temperature": 25.5, "pressure": 1015.7},
      {"precipitation": 0.0, "humidity": 57.0, "temperature": 26.0, "pressure": 1015.8},
      {"precipitation": 0.0, "humidity": 56.0, "temperature": 26.5, "pressure": 1015.9},
      {"precipitation": 0.0, "humidity": 55.0, "temperature": 27.0, "pressure": 1016.0},
      {"precipitation": 0.0, "humidity": 54.0, "temperature": 27.5, "pressure": 1016.1},
      {"precipitation": 0.0, "humidity": 55.0, "temperature": 27.0, "pressure": 1016.0},
      {"precipitation": 0.0, "humidity": 56.0, "temperature": 26.5, "pressure": 1015.9},
      {"precipitation": 0.0, "humidity": 57.0, "temperature": 26.0, "pressure": 1015.8},
      {"precipitation": 0.0, "humidity": 58.0, "temperature": 25.5, "pressure": 1015.7},
      {"precipitation": 0.0, "humidity": 59.0, "temperature": 25.0, "pressure": 1015.6},
      {"precipitation": 0.0, "humidity": 60.0, "temperature": 24.5, "pressure": 1015.5},
      {"precipitation": 0.0, "humidity": 61.0, "temperature": 24.0, "pressure": 1015.4},
      {"precipitation": 0.0, "humidity": 62.0, "temperature": 23.5, "pressure": 1015.3},
      {"precipitation": 0.0, "humidity": 63.0, "temperature": 23.0, "pressure": 1015.2},
      {"precipitation": 0.0, "humidity": 64.0, "temperature": 22.5, "pressure": 1015.1},
      {"precipitation": 0.0, "humidity": 65.0, "temperature": 22.0, "pressure": 1015.0},
      {"precipitation": 0.0, "humidity": 66.0, "temperature": 21.5, "pressure": 1014.9}
    ],
    "device_id": "DEMO_NORMAL"
  }'
```

**SAÍDA ESPERADA**:
```json
{
  "flood_probability": 0.0014,
  "risk_level": "LOW",
  "confidence": 0.99,
  "processing_time_ms": 45
}
```

**EXPLICAÇÃO**: "24h de tempo seco, pressão estável alta, umidade normal - modelo detecta segurança total"

### **Cenário B: Alerta Moderado (Chuva progressiva)**
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "sensor_data": [
      {"precipitation": 0.0, "humidity": 70.0, "temperature": 22.0, "pressure": 1015.0},
      {"precipitation": 1.0, "humidity": 72.0, "temperature": 21.5, "pressure": 1014.5},
      {"precipitation": 2.0, "humidity": 74.0, "temperature": 21.0, "pressure": 1014.0},
      {"precipitation": 3.0, "humidity": 76.0, "temperature": 20.5, "pressure": 1013.5},
      {"precipitation": 4.0, "humidity": 78.0, "temperature": 20.0, "pressure": 1013.0},
      {"precipitation": 5.0, "humidity": 80.0, "temperature": 19.5, "pressure": 1012.5},
      {"precipitation": 6.0, "humidity": 82.0, "temperature": 19.0, "pressure": 1012.0},
      {"precipitation": 7.0, "humidity": 84.0, "temperature": 18.5, "pressure": 1011.5},
      {"precipitation": 8.0, "humidity": 86.0, "temperature": 18.0, "pressure": 1011.0},
      {"precipitation": 9.0, "humidity": 88.0, "temperature": 17.5, "pressure": 1010.5},
      {"precipitation": 10.0, "humidity": 89.0, "temperature": 17.0, "pressure": 1010.0},
      {"precipitation": 11.0, "humidity": 90.0, "temperature": 16.5, "pressure": 1009.5},
      {"precipitation": 12.0, "humidity": 88.0, "temperature": 17.0, "pressure": 1010.0},
      {"precipitation": 10.0, "humidity": 86.0, "temperature": 17.5, "pressure": 1010.5},
      {"precipitation": 8.0, "humidity": 84.0, "temperature": 18.0, "pressure": 1011.0},
      {"precipitation": 6.0, "humidity": 82.0, "temperature": 18.5, "pressure": 1011.5},
      {"precipitation": 4.0, "humidity": 80.0, "temperature": 19.0, "pressure": 1012.0},
      {"precipitation": 3.0, "humidity": 78.0, "temperature": 19.5, "pressure": 1012.5},
      {"precipitation": 2.0, "humidity": 76.0, "temperature": 20.0, "pressure": 1013.0},
      {"precipitation": 1.0, "humidity": 74.0, "temperature": 20.5, "pressure": 1013.5},
      {"precipitation": 1.0, "humidity": 72.0, "temperature": 21.0, "pressure": 1014.0},
      {"precipitation": 0.5, "humidity": 70.0, "temperature": 21.5, "pressure": 1014.5},
      {"precipitation": 0.0, "humidity": 68.0, "temperature": 22.0, "pressure": 1015.0},
      {"precipitation": 0.0, "humidity": 66.0, "temperature": 22.5, "pressure": 1015.0}
    ],
    "device_id": "DEMO_MODERADO"
  }'
```

**SAÍDA ESPERADA**:
```json
{
  "flood_probability": 0.408,
  "risk_level": "MEDIUM",
  "confidence": 0.68,
  "processing_time_ms": 54
}
```

### **Cenário C: Crítico (Tempestade intensa 24h)**
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "sensor_data": [
      {"precipitation": 5.0, "humidity": 80.0, "temperature": 20.0, "pressure": 1010.0},
      {"precipitation": 8.0, "humidity": 85.0, "temperature": 19.5, "pressure": 1008.0},
      {"precipitation": 12.0, "humidity": 88.0, "temperature": 19.0, "pressure": 1006.0},
      {"precipitation": 15.0, "humidity": 90.0, "temperature": 18.5, "pressure": 1005.0},
      {"precipitation": 18.0, "humidity": 92.0, "temperature": 18.0, "pressure": 1004.0},
      {"precipitation": 22.0, "humidity": 94.0, "temperature": 17.5, "pressure": 1003.0},
      {"precipitation": 25.0, "humidity": 95.0, "temperature": 17.0, "pressure": 1002.0},
      {"precipitation": 28.0, "humidity": 96.0, "temperature": 16.5, "pressure": 1001.0},
      {"precipitation": 30.0, "humidity": 97.0, "temperature": 16.0, "pressure": 1000.0},
      {"precipitation": 32.0, "humidity": 98.0, "temperature": 15.5, "pressure": 999.0},
      {"precipitation": 35.0, "humidity": 98.0, "temperature": 15.0, "pressure": 998.0},
      {"precipitation": 38.0, "humidity": 99.0, "temperature": 14.5, "pressure": 997.0},
      {"precipitation": 40.0, "humidity": 99.0, "temperature": 14.0, "pressure": 996.0},
      {"precipitation": 42.0, "humidity": 99.0, "temperature": 14.0, "pressure": 996.0},
      {"precipitation": 45.0, "humidity": 99.0, "temperature": 14.5, "pressure": 997.0},
      {"precipitation": 40.0, "humidity": 98.0, "temperature": 15.0, "pressure": 998.0},
      {"precipitation": 35.0, "humidity": 98.0, "temperature": 15.5, "pressure": 999.0},
      {"precipitation": 30.0, "humidity": 97.0, "temperature": 16.0, "pressure": 1000.0},
      {"precipitation": 25.0, "humidity": 96.0, "temperature": 16.5, "pressure": 1001.0},
      {"precipitation": 20.0, "humidity": 95.0, "temperature": 17.0, "pressure": 1002.0},
      {"precipitation": 15.0, "humidity": 94.0, "temperature": 17.5, "pressure": 1003.0},
      {"precipitation": 12.0, "humidity": 92.0, "temperature": 18.0, "pressure": 1004.0},
      {"precipitation": 8.0, "humidity": 90.0, "temperature": 18.5, "pressure": 1005.0},
      {"precipitation": 5.0, "humidity": 88.0, "temperature": 19.0, "pressure": 1006.0}
    ],
    "device_id": "DEMO_CRITICO"
  }'
```

**SAÍDA ESPERADA**:
```json
{
  "flood_probability": 0.9924,
  "risk_level": "CRITICAL",
  "confidence": 0.98,
  "processing_time_ms": 45
}
```

**EXPLICAÇÃO**: "24h de tempestade progressiva: chuva torrencial + umidade máxima + pressão baixa = risco extremo detectado"

### **Cenário D: Dados Históricos Reais (Teresópolis 2011)**
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "sensor_data": [
      {"precipitation": 10.0, "humidity": 85.0, "temperature": 22.0, "pressure": 1008.0},
      {"precipitation": 15.0, "humidity": 88.0, "temperature": 21.0, "pressure": 1006.0},
      {"precipitation": 20.0, "humidity": 90.0, "temperature": 20.0, "pressure": 1004.0},
      {"precipitation": 25.0, "humidity": 92.0, "temperature": 19.5, "pressure": 1003.0},
      {"precipitation": 30.0, "humidity": 94.0, "temperature": 19.0, "pressure": 1002.0},
      {"precipitation": 35.0, "humidity": 95.0, "temperature": 18.5, "pressure": 1001.0},
      {"precipitation": 40.0, "humidity": 96.0, "temperature": 18.0, "pressure": 1000.0},
      {"precipitation": 45.0, "humidity": 97.0, "temperature": 17.5, "pressure": 999.0},
      {"precipitation": 50.0, "humidity": 98.0, "temperature": 17.0, "pressure": 998.0},
      {"precipitation": 55.0, "humidity": 98.0, "temperature": 16.5, "pressure": 997.0},
      {"precipitation": 60.0, "humidity": 99.0, "temperature": 16.0, "pressure": 996.0},
      {"precipitation": 65.0, "humidity": 99.0, "temperature": 15.5, "pressure": 995.0},
      {"precipitation": 70.0, "humidity": 99.0, "temperature": 15.0, "pressure": 994.0},
      {"precipitation": 75.0, "humidity": 99.0, "temperature": 15.0, "pressure": 994.0},
      {"precipitation": 80.0, "humidity": 99.0, "temperature": 15.5, "pressure": 995.0},
      {"precipitation": 75.0, "humidity": 99.0, "temperature": 16.0, "pressure": 996.0},
      {"precipitation": 70.0, "humidity": 98.0, "temperature": 16.5, "pressure": 997.0},
      {"precipitation": 65.0, "humidity": 98.0, "temperature": 17.0, "pressure": 998.0},
      {"precipitation": 60.0, "humidity": 97.0, "temperature": 17.5, "pressure": 999.0},
      {"precipitation": 55.0, "humidity": 96.0, "temperature": 18.0, "pressure": 1000.0},
      {"precipitation": 50.0, "humidity": 95.0, "temperature": 18.5, "pressure": 1001.0},
      {"precipitation": 45.0, "humidity": 94.0, "temperature": 19.0, "pressure": 1002.0},
      {"precipitation": 40.0, "humidity": 92.0, "temperature": 19.5, "pressure": 1003.0},
      {"precipitation": 35.0, "humidity": 90.0, "temperature": 20.0, "pressure": 1004.0}
    ],
    "device_id": "TERESOPOLIS_2011"
  }'
```

**OBJETIVO**: Mostrar que modelo detectaria a tragédia real (expectativa: > 95% probabilidade)

---

## 📱 **DEMONSTRAÇÃO ALTERNATIVA (PRESENCIAL)**

### **Setup para Apresentação ao Vivo**

#### **Estação 1: ESP32 + Sensores**
- Wokwi rodando em loop
- Demonstrar interação em tempo real
- Modificar sensores durante apresentação

#### **Estação 2: Modelo + Dados**
- Gráficos impressos de performance
- Confusion matrix em alta resolução
- Timeline de dados processados

#### **Estação 3: API + Integração**
- Interface Swagger rodando
- Testes automáticos em execução
- Métricas de performance em tempo real

---

## 🔧 **TROUBLESHOOTING DURANTE DEMONSTRAÇÃO**

### **Problema: API não responde**
```bash
# Solução rápida
ps aux | grep python  # Verificar se está rodando
kill [PID]            # Matar processo se necessário
python api/main.py    # Reiniciar
```

### **Problema: Modelo não carregado**
```bash
# Verificar arquivos
ls -la data/models/
# Deve mostrar: flood_lstm_model.h5 e flood_scaler.pkl
```

### **Problema: Wokwi não carrega**
- Link alternativo preparado
- Screenshots de backup
- Vídeo gravado como fallback

### **Problema: Conexão internet**
- Demos offline preparadas
- Dados locais funcionando
- API rodando localhost

---

## 📝 **FALAS ENSAIADAS**

### **Abertura (30 segundos)**
> "Enchentes matam mais pessoas no Brasil que qualquer outro desastre natural. Em 2011, mais de 900 vítimas em Teresópolis e Nova Friburgo poderiam ter sido salvas com apenas 24 horas de antecedência. Hoje apresento um sistema que resolve exatamente isso."

### **Transição ESP32 → Python**
> "Os sensores coletam dados, mas a inteligência está no que fazemos com esses dados. Vamos ver como transformamos números em predições que salvam vidas."

### **Destacar Resultados Técnicos**
> "99.2% de accuracy significa que a cada 100 predições, erramos menos de 1. Mas o mais importante: precision de 100% significa zero falsos alarmes - nunca vamos causar pânico desnecessário."

### **Conclusão Impactante**
> "Este não é apenas um projeto acadêmico. É um sistema funcional que pode ser implantado amanhã em qualquer cidade brasileira. Tecnologia salvando vidas - este é o futuro da prevenção de desastres."

---

## 📊 **METRICS PARA DESTACAR**

### **Performance Técnica**
- ✅ **99.2% Accuracy** - Quase perfeito
- ✅ **100% Precision** - Zero falsos positivos
- ✅ **96.3% Recall** - Detecta 96% eventos reais
- ✅ **<100ms** - Tempo resposta API
- ✅ **52,851 parâmetros** - Modelo otimizado

### **Dados Processados**
- ✅ **72,651 sequências** - Dados de treinamento
- ✅ **4 anos** - Histórico INMET (2021-2025)
- ✅ **27 eventos** - DisastersCharter coletados
- ✅ **407 riscos** - Eventos detectados automaticamente

### **Impacto Esperado**
- 🎯 **24 horas** - Antecedência de alerta
- 🎯 **40% redução** - Tempo de resposta
- 🎯 **Zero pânico** - Sem falsos alarmes
- 🎯 **Escalável** - Para qualquer região

---

## 🎬 **ROTEIRO ALTERNATIVO (3 MINUTOS)**

### **Versão Resumida para Pitch**

#### **Minuto 1: Problema + Solução**
- Estatísticas de enchentes Brasil
- Apresentação da arquitetura completa
- Diferencial da predição antecipada

#### **Minuto 2: Demo Técnica**
- ESP32 funcionando (30s)
- API + predições (30s)
- Resultados modelo (30s)

#### **Minuto 3: Resultados + Impacto**
- Métricas de performance
- Dados reais processados
- Potencial de salvamento de vidas

---

## 📋 **CHECKLIST PÓS-DEMONSTRAÇÃO**

- [ ] Vídeo gravado em qualidade HD
- [ ] Áudio claro e sem ruídos
- [ ] Todos os comandos funcionaram
- [ ] Métricas exibidas corretamente
- [ ] Transições suaves entre telas
- [ ] Tempo respeitado (5 minutos máximo)
- [ ] Conclusão impactante
- [ ] Links e referências mencionados

---

**🎯 Este guia garante uma demonstração profissional, técnica e impactante que comprova a funcionalidade completa do sistema de predição de enchentes desenvolvido.**
