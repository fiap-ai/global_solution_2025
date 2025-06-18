#!/bin/bash

# Gerador de Logs Demo - Global Solution 2025
# Script para gerar logs de demonstração no CloudWatch

echo "📝 GERADOR DE LOGS DEMO - LAMBDA CLOUDWATCH"
echo "==========================================="
echo "Gabriel Mule Monteiro - RM560586"
echo "Gerando logs de demonstração para demo_lambda_logs.sh"
echo ""

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
PURPLE='\033[0;35m'
NC='\033[0m'

log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_step() {
    echo -e "${CYAN}🔧 $1${NC}"
}

log_demo() {
    echo -e "${PURPLE}📝 $1${NC}"
}

# Verificar se a função Lambda existe
echo "=== VERIFICAÇÃO INICIAL ==="
echo ""

log_step "Verificando função Lambda 'flood-data-processor'..."
lambda_check=$(aws lambda get-function --function-name "flood-data-processor" 2>/dev/null)

if [[ $? -eq 0 ]]; then
    log_success "Função Lambda encontrada e acessível"
else
    echo -e "${RED}❌ Função Lambda não encontrada ou não acessível${NC}"
    exit 1
fi

echo ""
echo "=== GERAÇÃO DE LOGS DE DEMONSTRAÇÃO ==="
echo ""

log_demo "Gerando 6 cenários diferentes para demonstração completa..."

# Cenário 1: Normal - Baixo Risco
echo ""
log_step "1/6 - Cenário NORMAL (baixo risco de enchente)"

normal_payload='{
  "device_id": "FloodMonitor01",
  "timestamp": "'$(date -u +"%Y-%m-%dT%H:%M:%SZ")'",
  "sensors": {
    "water_level": 3.2,
    "humidity": 65.0,
    "temperature": 24.5,
    "pressure": 1015.2,
    "light_level": 75.0,
    "motion_detected": false
  },
  "alert_level": 0,
  "alert_name": "NORMAL",
  "battery_level": 92.5,
  "wifi_signal": -38
}'

temp_response1=$(mktemp)
aws lambda invoke \
  --function-name "flood-data-processor" \
  --payload "$normal_payload" \
  --cli-binary-format raw-in-base64-out \
  "$temp_response1" >/dev/null 2>&1

if [[ $? -eq 0 ]]; then
    log_success "Cenário normal executado"
else
    echo -e "${RED}❌ Falha no cenário normal${NC}"
fi
rm -f "$temp_response1"

sleep 2

# Cenário 2: Atenção - Risco Médio
echo ""
log_step "2/6 - Cenário ATENÇÃO (risco médio de enchente)"

attention_payload='{
  "device_id": "FloodMonitor01",
  "timestamp": "'$(date -u +"%Y-%m-%dT%H:%M:%SZ")'",
  "sensors": {
    "water_level": 15.8,
    "humidity": 82.0,
    "temperature": 21.2,
    "pressure": 1008.5,
    "light_level": 45.0,
    "motion_detected": true
  },
  "alert_level": 1,
  "alert_name": "ATTENTION",
  "battery_level": 87.3,
  "wifi_signal": -48
}'

temp_response2=$(mktemp)
aws lambda invoke \
  --function-name "flood-data-processor" \
  --payload "$attention_payload" \
  --cli-binary-format raw-in-base64-out \
  "$temp_response2" >/dev/null 2>&1

if [[ $? -eq 0 ]]; then
    log_success "Cenário atenção executado"
else
    echo -e "${RED}❌ Falha no cenário atenção${NC}"
fi
rm -f "$temp_response2"

sleep 2

# Cenário 3: Crítico - Alto Risco
echo ""
log_step "3/6 - Cenário CRÍTICO (alto risco de enchente)"

critical_payload='{
  "device_id": "FloodMonitor01",
  "timestamp": "'$(date -u +"%Y-%m-%dT%H:%M:%SZ")'",
  "sensors": {
    "water_level": 28.5,
    "humidity": 95.0,
    "temperature": 18.8,
    "pressure": 998.2,
    "light_level": 15.0,
    "motion_detected": true
  },
  "alert_level": 2,
  "alert_name": "CRITICAL",
  "battery_level": 78.9,
  "wifi_signal": -65
}'

temp_response3=$(mktemp)
aws lambda invoke \
  --function-name "flood-data-processor" \
  --payload "$critical_payload" \
  --cli-binary-format raw-in-base64-out \
  "$temp_response3" >/dev/null 2>&1

if [[ $? -eq 0 ]]; then
    log_success "Cenário crítico executado"
else
    echo -e "${RED}❌ Falha no cenário crítico${NC}"
fi
rm -f "$temp_response3"

sleep 2

# Cenário 4: Simulação IoT via MQTT
echo ""
log_step "4/6 - Simulação via IoT Core (MQTT trigger)"

iot_payload='{
  "device_id": "FloodMonitor01",
  "timestamp": "'$(date -u +"%Y-%m-%dT%H:%M:%SZ")'",
  "source": "IoT_Core_Rule",
  "sensors": {
    "water_level": 12.3,
    "humidity": 88.5,
    "temperature": 20.1,
    "pressure": 1005.8,
    "light_level": 35.0,
    "motion_detected": true
  },
  "alert_level": 1,
  "alert_name": "ATTENTION",
  "location": {
    "latitude": -22.4034,
    "longitude": -42.9821,
    "city": "Teresópolis"
  }
}'

# Publicar via IoT Core também
payload_b64=$(echo "$iot_payload" | base64)
aws iot-data publish \
  --topic "flood/sensors/data" \
  --payload "$payload_b64" >/dev/null 2>&1

if [[ $? -eq 0 ]]; then
    log_success "Evento IoT Core publicado (acionará Lambda automaticamente)"
else
    echo -e "${YELLOW}⚠️  Publicação IoT falhou, executando Lambda diretamente${NC}"
    
    temp_response4=$(mktemp)
    aws lambda invoke \
      --function-name "flood-data-processor" \
      --payload "$iot_payload" \
      --cli-binary-format raw-in-base64-out \
      "$temp_response4" >/dev/null 2>&1
    rm -f "$temp_response4"
fi

sleep 2

# Cenário 5: Dados de madrugada
echo ""
log_step "5/6 - Cenário NOTURNO (monitoramento contínuo)"

night_payload='{
  "device_id": "FloodMonitor01",
  "timestamp": "'$(date -u +"%Y-%m-%dT%H:%M:%SZ")'",
  "sensors": {
    "water_level": 7.1,
    "humidity": 75.5,
    "temperature": 19.2,
    "pressure": 1012.8,
    "light_level": 5.0,
    "motion_detected": false
  },
  "alert_level": 0,
  "alert_name": "NORMAL",
  "battery_level": 89.7,
  "wifi_signal": -42,
  "notes": "Monitoramento noturno - sem atividade"
}'

temp_response5=$(mktemp)
aws lambda invoke \
  --function-name "flood-data-processor" \
  --payload "$night_payload" \
  --cli-binary-format raw-in-base64-out \
  "$temp_response5" >/dev/null 2>&1

if [[ $? -eq 0 ]]; then
    log_success "Cenário noturno executado"
else
    echo -e "${RED}❌ Falha no cenário noturno${NC}"
fi
rm -f "$temp_response5"

sleep 2

# Cenário 6: Teste de stress/erro
echo ""
log_step "6/6 - Cenário TESTE (validação robustez)"

test_payload='{
  "device_id": "FloodMonitor01",
  "timestamp": "'$(date -u +"%Y-%m-%dT%H:%M:%SZ")'",
  "sensors": {
    "water_level": 22.0,
    "humidity": 91.2,
    "temperature": 17.5,
    "pressure": 1001.1,
    "light_level": 20.0,
    "motion_detected": true
  },
  "alert_level": 2,
  "alert_name": "CRITICAL",
  "battery_level": 71.2,
  "wifi_signal": -58,
  "test_mode": true
}'

temp_response6=$(mktemp)
aws lambda invoke \
  --function-name "flood-data-processor" \
  --payload "$test_payload" \
  --cli-binary-format raw-in-base64-out \
  "$temp_response6" >/dev/null 2>&1

if [[ $? -eq 0 ]]; then
    log_success "Cenário teste executado"
else
    echo -e "${RED}❌ Falha no cenário teste${NC}"
fi
rm -f "$temp_response6"

echo ""
echo "=== FINALIZAÇÃO ==="
echo ""

log_demo "Aguardando logs se propagarem no CloudWatch..."
sleep 5

log_success "🎊 LOGS DE DEMONSTRAÇÃO GERADOS COM SUCESSO!"
echo ""
echo "📋 Cenários criados:"
echo "   1. ✅ Normal (baixo risco)"
echo "   2. ✅ Atenção (risco médio)" 
echo "   3. ✅ Crítico (alto risco)"
echo "   4. ✅ IoT Core (trigger automático)"
echo "   5. ✅ Noturno (monitoramento)"
echo "   6. ✅ Teste (validação)"
echo ""
echo "🎬 PRONTO PARA DEMONSTRAÇÃO:"
echo "   Execute agora: ./demo_lambda_logs.sh"
echo ""
echo "📊 Os logs devem aparecer nos próximos 1-2 minutos no CloudWatch"
echo ""
echo "========================================="
echo "📝 Geração de logs concluída com sucesso!"
echo "========================================="
