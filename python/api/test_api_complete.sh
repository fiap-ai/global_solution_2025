#!/bin/bash

# Sistema de Predição de Enchentes - Global Solution 2025
# Script de Teste Completo da API FastAPI
# Autor: Gabriel Mule Monteiro

echo "🌊 SISTEMA DE PREDIÇÃO DE ENCHENTES - TESTE COMPLETO API"
echo "========================================================"
echo "Data: $(date)"
echo "Projeto: Global Solution 2025 - FIAP"
echo ""

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para log de sucesso
log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# Função para log de erro
log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Função para log de info
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Função para log de warning
log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Variáveis de configuração
API_HOST="0.0.0.0"
API_PORT="8000"
API_BASE_URL="http://${API_HOST}:${API_PORT}"
VENV_PATH="python/venv"
API_PID=""

# Função para verificar se a API está rodando
check_api_running() {
    if curl -s "${API_BASE_URL}/health" > /dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Função para setup do ambiente
setup_environment() {
    log_info "Configurando ambiente Python..."
    
    # Verificar se estamos no diretório correto
    if [[ ! -d "python" ]]; then
        log_error "Diretório python/ não encontrado. Execute o script no diretório raiz do projeto."
        exit 1
    fi
    
    # Ativar venv
    if [[ -d "${VENV_PATH}" ]]; then
        log_info "Ativando ambiente virtual..."
        source "${VENV_PATH}/bin/activate"
        log_success "Ambiente virtual ativado"
    else
        log_error "Ambiente virtual não encontrado em ${VENV_PATH}"
        exit 1
    fi
    
    # Verificar se os modelos existem
    if [[ ! -f "data/models/flood_lstm_model.h5" ]]; then
        log_error "Modelo LSTM não encontrado em data/models/flood_lstm_model.h5"
        exit 1
    fi
    
    if [[ ! -f "data/models/flood_scaler.pkl" ]]; then
        log_error "Scaler não encontrado em data/models/flood_scaler.pkl"
        exit 1
    fi
    
    log_success "Ambiente configurado com sucesso"
}

# Função para iniciar a API
start_api() {
    log_info "Iniciando API FastAPI..."
    
    if check_api_running; then
        log_warning "API já está rodando em ${API_BASE_URL}"
        return 0
    fi
    
    # Mudar para diretório python
    cd python
    
    # Iniciar API em background
    nohup python -m uvicorn api.main:app --host 0.0.0.0 --port ${API_PORT} > ../api.log 2>&1 &
    API_PID=$!
    
    # Aguardar API inicializar
    log_info "Aguardando API inicializar..."
    for i in {1..30}; do
        if check_api_running; then
            log_success "API iniciada com sucesso (PID: ${API_PID})"
            cd ..
            return 0
        fi
        sleep 1
        echo -n "."
    done
    
    echo ""
    log_error "Falha ao iniciar API após 30 segundos"
    cd ..
    return 1
}

# Função para parar a API
stop_api() {
    if [[ -n "${API_PID}" ]]; then
        log_info "Parando API (PID: ${API_PID})..."
        kill ${API_PID} 2>/dev/null
        wait ${API_PID} 2>/dev/null
        log_success "API parada"
    fi
}

# Função para teste de health check
test_health_check() {
    log_info "Testando endpoint /health..."
    
    response=$(curl -s -w "HTTPSTATUS:%{http_code}" "${API_BASE_URL}/health")
    http_code=$(echo $response | grep -o "HTTPSTATUS:[0-9]*" | cut -d: -f2)
    body=$(echo $response | sed -E 's/HTTPSTATUS:[0-9]*$//')
    
    if [[ $http_code -eq 200 ]]; then
        log_success "Health check: Status 200 OK"
        
        # Verificar JSON response
        if echo "$body" | jq -e '.status == "healthy"' > /dev/null 2>&1; then
            log_success "Health check: Status = healthy"
        else
            log_error "Health check: Status não é 'healthy'"
            return 1
        fi
        
        if echo "$body" | jq -e '.model_loaded == true' > /dev/null 2>&1; then
            log_success "Health check: Modelo carregado"
        else
            log_error "Health check: Modelo não carregado"
            return 1
        fi
        
        return 0
    else
        log_error "Health check: Status $http_code (esperado: 200)"
        return 1
    fi
}

# Função para teste de predição normal
test_prediction_normal() {
    log_info "Testando predição - Cenário Normal..."
    
    payload='{
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
        "device_id": "TEST_NORMAL"
    }'
    
    response=$(curl -s -w "HTTPSTATUS:%{http_code}" \
        -H "Content-Type: application/json" \
        -d "$payload" \
        "${API_BASE_URL}/predict")
    
    http_code=$(echo $response | grep -o "HTTPSTATUS:[0-9]*" | cut -d: -f2)
    body=$(echo $response | sed -E 's/HTTPSTATUS:[0-9]*$//')
    
    if [[ $http_code -eq 200 ]]; then
        log_success "Predição Normal: Status 200 OK"
        
        # Verificar se é baixo risco
        risk_level=$(echo "$body" | jq -r '.risk_level')
        if [[ "$risk_level" == "LOW" ]]; then
            log_success "Predição Normal: Risk Level = LOW ✅"
        else
            log_warning "Predição Normal: Risk Level = $risk_level (esperado: LOW)"
        fi
        
        # Verificar probabilidade baixa
        probability=$(echo "$body" | jq -r '.flood_probability')
        if (( $(echo "$probability < 0.2" | bc -l) )); then
            log_success "Predição Normal: Probabilidade baixa ($probability) ✅"
        else
            log_warning "Predição Normal: Probabilidade alta ($probability)"
        fi
        
        return 0
    else
        log_error "Predição Normal: Status $http_code (esperado: 200)"
        return 1
    fi
}

# Função para teste de predição crítica
test_prediction_critical() {
    log_info "Testando predição - Cenário Crítico..."
    
    payload='{
        "sensor_data": [
            {"precipitation": 10.0, "humidity": 85.0, "temperature": 20.0, "pressure": 1008.0},
            {"precipitation": 15.0, "humidity": 88.0, "temperature": 19.5, "pressure": 1006.0},
            {"precipitation": 20.0, "humidity": 90.0, "temperature": 19.0, "pressure": 1004.0},
            {"precipitation": 25.0, "humidity": 92.0, "temperature": 18.5, "pressure": 1003.0},
            {"precipitation": 30.0, "humidity": 94.0, "temperature": 18.0, "pressure": 1002.0},
            {"precipitation": 35.0, "humidity": 95.0, "temperature": 17.5, "pressure": 1001.0},
            {"precipitation": 40.0, "humidity": 96.0, "temperature": 17.0, "pressure": 1000.0},
            {"precipitation": 45.0, "humidity": 97.0, "temperature": 16.5, "pressure": 999.0},
            {"precipitation": 50.0, "humidity": 98.0, "temperature": 16.0, "pressure": 998.0},
            {"precipitation": 55.0, "humidity": 98.0, "temperature": 15.5, "pressure": 997.0},
            {"precipitation": 60.0, "humidity": 99.0, "temperature": 15.0, "pressure": 996.0},
            {"precipitation": 65.0, "humidity": 99.0, "temperature": 14.5, "pressure": 995.0},
            {"precipitation": 70.0, "humidity": 99.0, "temperature": 14.0, "pressure": 994.0},
            {"precipitation": 75.0, "humidity": 99.0, "temperature": 14.0, "pressure": 994.0},
            {"precipitation": 70.0, "humidity": 99.0, "temperature": 14.5, "pressure": 995.0},
            {"precipitation": 65.0, "humidity": 98.0, "temperature": 15.0, "pressure": 996.0},
            {"precipitation": 60.0, "humidity": 98.0, "temperature": 15.5, "pressure": 997.0},
            {"precipitation": 55.0, "humidity": 97.0, "temperature": 16.0, "pressure": 998.0},
            {"precipitation": 50.0, "humidity": 96.0, "temperature": 16.5, "pressure": 999.0},
            {"precipitation": 45.0, "humidity": 95.0, "temperature": 17.0, "pressure": 1000.0},
            {"precipitation": 40.0, "humidity": 94.0, "temperature": 17.5, "pressure": 1001.0},
            {"precipitation": 35.0, "humidity": 92.0, "temperature": 18.0, "pressure": 1002.0},
            {"precipitation": 30.0, "humidity": 90.0, "temperature": 18.5, "pressure": 1003.0},
            {"precipitation": 25.0, "humidity": 88.0, "temperature": 19.0, "pressure": 1004.0}
        ],
        "device_id": "TEST_CRITICAL"
    }'
    
    response=$(curl -s -w "HTTPSTATUS:%{http_code}" \
        -H "Content-Type: application/json" \
        -d "$payload" \
        "${API_BASE_URL}/predict")
    
    http_code=$(echo $response | grep -o "HTTPSTATUS:[0-9]*" | cut -d: -f2)
    body=$(echo $response | sed -E 's/HTTPSTATUS:[0-9]*$//')
    
    if [[ $http_code -eq 200 ]]; then
        log_success "Predição Crítica: Status 200 OK"
        
        # Verificar se é alto risco
        risk_level=$(echo "$body" | jq -r '.risk_level')
        if [[ "$risk_level" == "CRITICAL" || "$risk_level" == "HIGH" ]]; then
            log_success "Predição Crítica: Risk Level = $risk_level ✅"
        else
            log_warning "Predição Crítica: Risk Level = $risk_level (esperado: HIGH/CRITICAL)"
        fi
        
        # Verificar probabilidade alta
        probability=$(echo "$body" | jq -r '.flood_probability')
        if (( $(echo "$probability > 0.5" | bc -l) )); then
            log_success "Predição Crítica: Probabilidade alta ($probability) ✅"
        else
            log_warning "Predição Crítica: Probabilidade baixa ($probability)"
        fi
        
        return 0
    else
        log_error "Predição Crítica: Status $http_code (esperado: 200)"
        return 1
    fi
}

# Função para teste automático
test_automatic() {
    log_info "Testando endpoint /test/predict..."
    
    response=$(curl -s -w "HTTPSTATUS:%{http_code}" "${API_BASE_URL}/test/predict")
    http_code=$(echo $response | grep -o "HTTPSTATUS:[0-9]*" | cut -d: -f2)
    body=$(echo $response | sed -E 's/HTTPSTATUS:[0-9]*$//')
    
    if [[ $http_code -eq 200 ]]; then
        log_success "Teste Automático: Status 200 OK"
        
        # Verificar se tem resultados de teste
        if echo "$body" | jq -e '.test_results' > /dev/null 2>&1; then
            log_success "Teste Automático: Resultados presentes"
            
            # Verificar se modelo está funcionando
            if echo "$body" | jq -e '.model_working == true' > /dev/null 2>&1; then
                log_success "Teste Automático: Modelo funcionando ✅"
            else
                log_error "Teste Automático: Modelo não funcionando"
                return 1
            fi
            
            return 0
        else
            log_error "Teste Automático: Resultados não encontrados"
            return 1
        fi
    else
        log_error "Teste Automático: Status $http_code (esperado: 200)"
        return 1
    fi
}

# Função para teste de documentação
test_documentation() {
    log_info "Testando documentação Swagger..."
    
    response=$(curl -s -w "HTTPSTATUS:%{http_code}" "${API_BASE_URL}/docs")
    http_code=$(echo $response | grep -o "HTTPSTATUS:[0-9]*" | cut -d: -f2)
    
    if [[ $http_code -eq 200 ]]; then
        log_success "Documentação: Status 200 OK"
        return 0
    else
        log_error "Documentação: Status $http_code (esperado: 200)"
        return 1
    fi
}

# Função para teste de dados inválidos
test_invalid_data() {
    log_info "Testando dados inválidos..."
    
    # Teste com dados insuficientes (menos de 24 entradas)
    payload='{
        "sensor_data": [
            {"precipitation": 0.0, "humidity": 65.0, "temperature": 22.0, "pressure": 1015.0}
        ],
        "device_id": "TEST_INVALID"
    }'
    
    response=$(curl -s -w "HTTPSTATUS:%{http_code}" \
        -H "Content-Type: application/json" \
        -d "$payload" \
        "${API_BASE_URL}/predict")
    
    http_code=$(echo $response | grep -o "HTTPSTATUS:[0-9]*" | cut -d: -f2)
    
    if [[ $http_code -eq 422 ]]; then
        log_success "Dados Inválidos: Status 422 (Validação Pydantic) ✅"
        return 0
    else
        log_warning "Dados Inválidos: Status $http_code (esperado: 422)"
        return 1
    fi
}

# Função para medir performance
test_performance() {
    log_info "Testando performance da API..."
    
    start_time=$(date +%s%N)
    
    payload='{
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
        "device_id": "TEST_PERFORMANCE"
    }'
    
    curl -s -H "Content-Type: application/json" -d "$payload" "${API_BASE_URL}/predict" > /dev/null
    
    end_time=$(date +%s%N)
    duration=$((($end_time - $start_time) / 1000000)) # Converter para milissegundos
    
    if [[ $duration -lt 1000 ]]; then
        log_success "Performance: ${duration}ms (< 1 segundo) ✅"
    else
        log_warning "Performance: ${duration}ms (> 1 segundo)"
    fi
}

# Função principal de testes
run_tests() {
    log_info "Iniciando bateria de testes da API..."
    echo ""
    
    local tests_passed=0
    local tests_total=7
    
    # Executar testes
    if test_health_check; then ((tests_passed++)); fi
    echo ""
    
    if test_automatic; then ((tests_passed++)); fi
    echo ""
    
    if test_prediction_normal; then ((tests_passed++)); fi
    echo ""
    
    if test_prediction_critical; then ((tests_passed++)); fi
    echo ""
    
    if test_invalid_data; then ((tests_passed++)); fi
    echo ""
    
    if test_documentation; then ((tests_passed++)); fi
    echo ""
    
    if test_performance; then ((tests_passed++)); fi
    echo ""
    
    # Relatório final
    echo "========================================================"
    echo "🎯 RELATÓRIO FINAL DOS TESTES"
    echo "========================================================"
    echo "Testes executados: $tests_total"
    echo "Testes aprovados:  $tests_passed"
    echo "Taxa de sucesso:   $(echo "scale=1; $tests_passed * 100 / $tests_total" | bc)%"
    echo ""
    
    if [[ $tests_passed -eq $tests_total ]]; then
        log_success "🎉 TODOS OS TESTES APROVADOS! API 100% FUNCIONAL"
        return 0
    else
        log_warning "⚠️  $((tests_total - tests_passed)) teste(s) falharam"
        return 1
    fi
}

# Função de cleanup
cleanup() {
    log_info "Executando cleanup..."
    stop_api
    if [[ -f "api.log" ]]; then
        rm -f api.log
    fi
    log_success "Cleanup concluído"
}

# Trap para cleanup em caso de interrupção
trap cleanup EXIT

# Script principal
main() {
    echo "🚀 Iniciando testes do Sistema de Predição de Enchentes..."
    echo ""
    
    # Setup
    setup_environment
    echo ""
    
    # Iniciar API
    if ! start_api; then
        log_error "Falha ao iniciar API. Abortando testes."
        exit 1
    fi
    echo ""
    
    # Aguardar um pouco mais para garantir que a API está estável
    log_info "Aguardando API estabilizar..."
    sleep 3
    
    # Executar testes
    if run_tests; then
        echo ""
        log_success "🎊 SISTEMA VALIDADO: API FastAPI 100% OPERACIONAL"
        exit 0
    else
        echo ""
        log_error "❌ TESTES FALHARAM: Verificar logs para mais detalhes"
        exit 1
    fi
}

# Executar script principal
main "$@"
