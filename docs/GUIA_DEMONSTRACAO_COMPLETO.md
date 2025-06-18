# 🎬 GUIA DE DEMONSTRAÇÃO COMPLETA
## Sistema de Predição de Enchentes - Global Solution 2025

### 📋 **PREPARAÇÃO PRÉ-DEMONSTRAÇÃO**

#### ✅ **Checklist de Ambiente**
- [ ] Terminal no diretório raiz: `global_solution_2025/`
- [ ] venv ativado: `cd python && source venv/bin/activate && cd ..`
- [ ] Browser com abas abertas:
  - [ ] Wokwi: https://wokwi.com/projects/434060150016336897
  - [ ] API Docs: http://0.0.0.0:8000/docs
  - [ ] GitHub: https://github.com/fiap-ai/global_solution_2025
- [ ] Arquivos para exibir:
  - [ ] `docs/RESULTADOS_MODELO_LSTM.md`
  - [ ] `data/models/training_results.json`
  - [ ] `data/models/plots/training_history.png`
- [ ] Comandos testados previamente (todos funcionando)

#### 🚀 **Setup Rápido (2 minutos antes da gravação)**
```bash
# EXECUTAR TUDO DO DIRETÓRIO RAIZ: global_solution_2025/

# 1. Ativar ambiente (ir para python, ativar, voltar para root)
cd python && source venv/bin/activate && cd ..

# 2. Iniciar API (em background)
cd python && python api/main.py &

# 3. Voltar para root e verificar se tudo funciona
cd ..
curl http://0.0.0.0:8000/health
# Deve retornar: {"status":"healthy","model_loaded":true}

# 4. Abrir Wokwi no browser
# 5. Preparar slides/docs

# ⚠️ IMPORTANTE: TODOS OS SCRIPTS DEMO SÃO EXECUTADOS DO ROOT!
# ✅ Você deve estar em: ~/global_solution_2025/
# ✅ Scripts: ./demo_api_complete.sh, ./demo_aws_cli.sh, etc.
```

### **💡 SCRIPTS DE DEMONSTRAÇÃO AUTOMATIZADOS**

**Por que criamos scripts de demo:**
> "Para demonstrar funcionalidades complexas de forma fluida, criamos 4 scripts automatizados que encadeiam múltiplas ações e validações em sequência. Isso permite uma apresentação profissional sem digitação manual de comandos longos durante a gravação, garantindo demonstração sem falhas."

**Scripts disponíveis:**
- `./demo_api_complete.sh` - API + Modelo LSTM (7 testes automatizados)
- `./demo_aws_cli.sh` - Credenciais e configuração AWS
- `./demo_iot_mqtt.sh` - Comunicação MQTT + Pipeline IoT
- `./demo_lambda_logs.sh` - Lambda + CloudWatch + Métricas

---

## 🎥 **ROTEIRO CRONOMETRADO - 5 MINUTOS**

### 🎬 **MINUTO 1 (00:00-01:00): ABERTURA + CONTEXTO**

#### **[00:00-00:15] Apresentação**
**TELA**: Slide com logo FIAP + título do projeto  
**FALA**: 
> "Olá! Sou Gabriel Mule Monteiro, RM560586, e vou apresentar nosso sistema de predição de enchentes desenvolvido para a Global Solution 2025. O problema das enchentes urbanas é crítico - só em 2011, Teresópolis e Nova Friburgo tiveram mais de 900 vítimas por falta de alertas precoces."

#### **[00:15-00:30] Problema e Solução**
**TELA**: Mostrar arquivos do projeto:
- `data/images/` - Abrir pasta com imagens de satélite
- `data/images/satellite_05_Flooding_Event_in_Rio_Grande_do_Sul_Brazil_Post_di.jpg`
- `data/images/satellite_06_Flooding_Event_in_Rio_Grande_do_Sul_Brazil_Pre_dis.jpg`
- `data/disasters_charter/quickviews_flood_api_response.json` - JSON com eventos reais

**FALA**: 
> "Nossa solução integra IoT, Inteligência Artificial e Cloud Computing para detectar riscos 24 horas antes da enchente acontecer, permitindo evacuação preventiva e salvando vidas."

#### **[00:30-01:00] Arquitetura Overview**
**TELA**: Mostrar arquivos:
- `README.md` - Seção de arquitetura
- `global_solution_2025_final.md` - Visão geral completa do projeto

**FALA**: 
> "O sistema tem 3 camadas: ESP32 com sensores físicos, Python com modelo LSTM treinado com dados reais do INMET, e AWS para escalabilidade. Vamos ver cada componente funcionando."

---

### 🎬 **MINUTO 2 (01:00-02:00): ESP32 + SENSORES IOT**

#### **[01:00-01:15] Simulação Wokwi**
**TELA**: Wokwi - https://wokwi.com/projects/434060150016336897  
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
**TELA**: Abrir `docs/RESULTADOS_MODELO_LSTM.md` no VSCode/Browser  
**MOSTRAR**:
- Seção "Dataset Processado" 
- Estatísticas: 72.651 sequências
- Estações INMET: Teresópolis (A618) + Nova Friburgo (A624)
- Período temporal: 2021-2025 (4 anos)

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

#### **[03:00-04:00] Demonstração Automatizada da API**
**TELA**: Terminal  
**COMANDO**: `./demo_api_complete.sh`

**FALA INICIAL**: 
> "Agora vou executar nosso script de demonstração automatizada da API que testa todos os componentes em sequência..."

**DURANTE A EXECUÇÃO - EXPLICAR CADA OUTPUT:**

**Quando aparecer "Health Check":**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_version": "1.0.0"
}
```
> "Sistema saudável, modelo LSTM carregado e operacional."

**Quando aparecer "Bateria de testes":**
> "O script está executando 7 testes automatizados validando cada endpoint..."

**Quando aparecer "Teste Automático":**
```json
{
  "test_results": {
    "normal_scenario": {
      "probability": 0.0012,
      "risk_level": "LOW"
    },
    "flood_scenario": {
      "probability": 0.9924,
      "risk_level": "CRITICAL"
    }
  }
}
```
> "Vejam a discriminação perfeita: 0.12% vs 99.24% - o modelo distingue perfeitamente cenários normais de críticos!"

**Quando aparecer "Informações do Modelo":**
```json
{
  "model_loaded": true,
  "total_params": 52851,
  "input_shape": "(None, 24, 4)",
  "output_shape": "(None, 1)"
}
```
> "Modelo LSTM com 52.851 parâmetros, processando sequências de 24 horas com 4 variáveis meteorológicas."

**Quando aparecer "Performance":**
> "Tempo de resposta menor que 100ms - permitindo alertas instantâneos quando necessário."

**Quando aparecer "7/7 testes aprovados":**
> "Sistema 100% validado - API funcionando perfeitamente em produção!"

---

### 🎬 **MINUTO 5 (04:00-05:00): INTEGRAÇÃO AWS + CONCLUSÃO**

#### **[04:00-04:15] AWS CLI Demonstração**
**TELA**: Terminal  
**COMANDO**: `./demo_aws_cli.sh`

**FALA INICIAL**: 
> "Vou verificar toda nossa infraestrutura AWS configurada..."

**DURANTE A EXECUÇÃO - EXPLICAR CADA OUTPUT:**

**Quando aparecer "Verificando credenciais":**
```json
{
  "UserId": "AIDAXXXXXXXXXXXXXXXX",
  "Account": "8319XXXXX713", 
  "Arn": "arn:aws:iam::8319XXXXX713:user/flood-monitor-***"
}
```
> "Conta AWS autenticada com credenciais válidas."

**Quando aparecer "Things IoT":**
> "Thing 'FloodMonitor01' registrado no AWS IoT Core - nossa ponte entre sensores e nuvem."

**Quando aparecer "Certificados X.509":**
> "Certificados de segurança ativos garantindo comunicação criptografada."

#### **[04:15-04:30] MQTT + Pipeline IoT**
**COMANDO**: `./demo_iot_mqtt.sh`

**FALA INICIAL**: 
> "Agora vou demonstrar comunicação MQTT em tempo real..."

**DURANTE A EXECUÇÃO - EXPLICAR CADA OUTPUT:**

**Quando aparecer "Publicando dados":**
> "Simulando dados de sensores sendo enviados via MQTT - protocolo padrão para IoT."

**Quando aparecer "Status: Sucesso":**
> "Dados chegaram na AWS IoT Core - pipeline ESP32 → Cloud funcionando!"

#### **[04:30-04:45] Lambda + CloudWatch**
**COMANDO**: `./demo_lambda_logs.sh`

**FALA INICIAL**: 
> "E agora o processamento inteligente na nuvem..."

**DURANTE A EXECUÇÃO - EXPLICAR CADA OUTPUT:**

**Quando aparecer função Lambda:**
> "Função 'flood-data-processor' executando Python na AWS com nosso modelo."

**Quando aparecer métricas:**
> "26 invocações, 9.7ms duração média, 0% erro - performance excelente em produção!"

#### **[04:45-05:00] Impacto e Conclusão**
**FALA**: 
> "Fluxo completo funcionando: ESP32 → AWS IoT → Lambda → API → Predição. Sistema end-to-end operacional que pode salvar vidas: 99.2% de accuracy, zero falsos alarmes, alertas 24h antecipados. MVP pronto para implantação em qualquer cidade do Brasil. Obrigado!"

---

## 🎯 **SEQUÊNCIA DE DEMONSTRAÇÃO COM SCRIPTS**

### **📋 Ordem de Execução para Vídeo de 5 minutos:**

```bash
# MINUTO 4: Demonstração da API + Modelo LSTM
./demo_api_complete.sh

# MINUTO 5: Infraestrutura AWS (3 scripts sequenciais)
./demo_aws_cli.sh       # Credenciais + configuração
./demo_iot_mqtt.sh      # Comunicação MQTT
./demo_lambda_logs.sh   # Lambda + CloudWatch
```

### **🔍 O que cada script valida:**

#### **demo_api_complete.sh**
- ✅ Health check da API 
- ✅ Modelo LSTM carregado (52.851 parâmetros)
- ✅ Teste normal vs crítico (0.12% vs 99.24%)
- ✅ Performance < 100ms
- ✅ 7/7 testes aprovados

#### **demo_aws_cli.sh**
- ✅ Credenciais AWS autenticadas
- ✅ Thing "FloodMonitor01" registrado
- ✅ Certificados X.509 ativos
- ✅ Políticas IoT configuradas

#### **demo_iot_mqtt.sh**
- ✅ Publicação MQTT funcionando
- ✅ Pipeline ESP32 → IoT Core
- ✅ Tópicos ativos
- ✅ Comunicação segura

#### **demo_lambda_logs.sh**
- ✅ Função Lambda executando
- ✅ CloudWatch logs ativos
- ✅ Métricas de performance
- ✅ Pipeline completo IoT→Lambda

### **⚡ Para teste rápido de todos os componentes:**
```bash
# Validação completa do sistema (2 minutos)
./demo_api_complete.sh && ./demo_aws_cli.sh && ./demo_iot_mqtt.sh && ./demo_lambda_logs.sh
```

---

## 🚀 **SCRIPTS AUTOMATIZADOS DE DEMONSTRAÇÃO**

### **📜 Scripts Bash Criados**

Para facilitar a demonstração e automatizar sequências complexas, foram criados 4 scripts especializados:

#### **1. `demo_api_complete.sh` - Demonstração Completa da API**
```bash
./demo_api_complete.sh
```
**O que faz:**
- ✅ Verifica se API está rodando (inicia se necessário)
- ✅ Executa bateria completa de 7 testes automatizados
- ✅ Testa cenários normal vs crítico
- ✅ Valida performance (tempo de resposta)
- ✅ Verifica documentação Swagger
- ✅ Mostra métricas do modelo LSTM
- ✅ Relatório final com taxa de sucesso

**Demonstração ideal para:** Python/API + Modelo LSTM

#### **2. `demo_aws_cli.sh` - Verificação AWS CLI**
```bash
./demo_aws_cli.sh
```
**O que faz:**
- ✅ Verifica credenciais AWS (`aws sts get-caller-identity`)
- ✅ Lista Things IoT (`aws iot list-things`)
- ✅ Verifica certificados X.509 (`aws iot list-certificates`)
- ✅ Mostra políticas IoT (`aws iot list-policies`)
- ✅ Valida estrutura local de arquivos
- ✅ Obtém endpoint IoT Core
- ✅ Relatório de configuração completo

**Demonstração ideal para:** AWS Setup + Credenciais

#### **3. `demo_iot_mqtt.sh` - Comunicação MQTT**
```bash
./demo_iot_mqtt.sh
```
**O que faz:**
- ✅ Publica dados de sensores simulados
- ✅ Envia alertas críticos via MQTT
- ✅ Testa status do dispositivo
- ✅ Executa `./start.sh` automaticamente
- ✅ Verifica regras IoT ativas
- ✅ Simula pipeline ESP32→IoT→Lambda
- ✅ Mostra tópicos MQTT funcionando

**Demonstração ideal para:** IoT Core + MQTT + Pipeline

#### **4. `demo_lambda_logs.sh` - Lambda + CloudWatch**
```bash
./demo_lambda_logs.sh
```
**O que faz:**
- ✅ Executa função Lambda com evento de teste
- ✅ Mostra logs do CloudWatch em tempo real
- ✅ Exibe métricas de performance
- ✅ Testa pipeline IoT→Lambda automático
- ✅ Verifica integração completa
- ✅ Relatório de estatísticas finais

**Demonstração ideal para:** AWS Lambda + Logs + Métricas

### **🎬 Uso Durante Demonstração**

#### **Para Vídeo de 5 minutos:**
```bash
# Minuto 3 (API + Python)
./demo_api_complete.sh  # Mostra 7/7 testes aprovados

# Minuto 4-5 (AWS)
./demo_aws_cli.sh       # Credenciais + Things
./demo_iot_mqtt.sh      # MQTT funcionando
./demo_lambda_logs.sh   # Lambda + CloudWatch
```

#### **Para Demonstração Presencial:**
```bash
# Terminal 1: API
./demo_api_complete.sh

# Terminal 2: AWS
./demo_aws_cli.sh && ./demo_iot_mqtt.sh

# Terminal 3: Lambda
./demo_lambda_logs.sh
```

#### **Para Debug/Troubleshooting:**
```bash
# Se API não responde
./demo_api_complete.sh  # Auto-inicia API

# Se AWS não conecta
./demo_aws_cli.sh       # Diagnóstico completo

# Se MQTT falha
./demo_iot_mqtt.sh      # Testa conectividade

# Se Lambda não executa
./demo_lambda_logs.sh   # Verifica logs
```

### **🎯 Vantagens dos Scripts:**

1. **Automação Completa**: Elimina comandos longos e complexos
2. **Detecção de Problemas**: Identifica e reporta falhas automaticamente
3. **Saída Colorida**: Interface visual clara e profissional
4. **Auto-recuperação**: Tenta corrigir problemas simples automaticamente
5. **Métricas em Tempo Real**: Mostra performance e estatísticas
6. **Relatórios Estruturados**: Sumário final de cada componente

### **⚡ Execução Rápida para Demonstração:**

```bash
# Setup completo em 2 minutos
./demo_api_complete.sh     # 30s - API + Modelo
./demo_aws_cli.sh          # 30s - AWS Setup  
./demo_iot_mqtt.sh         # 45s - MQTT + Pipeline
./demo_lambda_logs.sh      # 45s - Lambda + Logs

# Resultado: Sistema 100% validado automaticamente
```

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
