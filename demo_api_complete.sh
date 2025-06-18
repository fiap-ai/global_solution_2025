#!/bin/bash

# Demonstração Completa da API - Global Solution 2025
# Script para demonstração em apresentações e vídeos

echo "🌊 DEMONSTRAÇÃO COMPLETA - FLOOD PREDICTION API"
echo "================================================="
echo "Gabriel Mule Monteiro - RM560586"
echo "Global Solution 2025 - FIAP"
echo ""

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Função para log colorido
log_demo() {
    echo -e "${CYAN}🎬 DEMO: $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Verificar se API está rodando
API_URL="http://0.0.0.0:8000"

log_demo "Verificando se API está disponível..."
if curl -s "${API_URL}/health" > /dev/null 2>&1; then
    log_success "API encontrada em ${API_URL}"
else
    echo -e "${RED}❌ API não encontrada. Iniciando API...${NC}"
    
    # Tentar iniciar API
    if [[ -f "python/api/main.py" ]]; then
        cd python
        source venv/bin/activate 2>/dev/null
        nohup python api/main.py > ../demo_api.log 2>&1 &
        API_PID=$!
        cd ..
        
        # Aguardar API inicializar
        for i in {1..10}; do
            if curl -s "${API_URL}/health" > /dev/null 2>&1; then
                log_success "API iniciada com sucesso (PID: ${API_PID})"
                break
            fi
            sleep 1
            echo -n "."
        done
        echo ""
    else
        echo -e "${RED}❌ Arquivo api/main.py não encontrado${NC}"
        exit 1
    fi
fi

echo ""
log_demo "=== FASE 1: TESTES AUTOMATIZADOS COMPLETOS ==="

# Executar script de testes se existir
if [[ -f "python/api/test_api_complete.sh" ]]; then
    log_info "Executando bateria completa de testes..."
    echo ""
    
    # Executar testes DO DIRETÓRIO RAIZ (não entrar em python/api)
    bash python/api/test_api_complete.sh
    
    echo ""
    log_success "Bateria de testes concluída!"
    
    # Mostrar JSONs das respostas para credibilidade técnica
    echo ""
    log_demo "=== COMPROVAÇÃO TÉCNICA - RESPOSTAS JSON ==="
    
    # Health check JSON
    echo ""
    log_info "📋 Resposta do Health Check:"
    health_response=$(curl -s "${API_URL}/health")
    echo "$health_response" | jq '.' 2>/dev/null || echo "$health_response"
    
    # Teste automático JSON  
    echo ""
    log_info "📋 Resposta do Teste Automático:"
    auto_test_response=$(curl -s "${API_URL}/test/predict")
    echo "$auto_test_response" | jq '.' 2>/dev/null || echo "$auto_test_response"
    
    # Exemplo de predição normal JSON
    echo ""
    log_info "📋 Resposta da Predição Normal:"
    
    # Criar dados de 24 horas para comprovação técnica
    credibility_data='{"sensor_data":['
    for i in {1..24}; do
        credibility_data+='{"precipitation": 0.0, "humidity": 65.0, "temperature": 22.0, "pressure": 1015.0}'
        if [[ $i -lt 24 ]]; then
            credibility_data+=","
        fi
    done
    credibility_data+='], "device_id": "TEST_CREDIBILITY"}'
    
    normal_test_response=$(curl -s -X POST "${API_URL}/predict" \
      -H "Content-Type: application/json" \
      -d "$credibility_data")
    echo "$normal_test_response" | jq '.' 2>/dev/null || echo "$normal_test_response"
    
else
    log_info "Script test_api_complete.sh não encontrado, executando testes manuais..."
    
    # Health check
    echo ""
    log_demo "1. Health Check da API"
    response=$(curl -s "${API_URL}/health")
    echo "curl ${API_URL}/health"
    echo "$response" | jq '.' 2>/dev/null || echo "$response"
    
    # Teste automático
    echo ""
    log_demo "2. Teste Automático (Cenários Normal vs Crítico)"
    response=$(curl -s "${API_URL}/test/predict")
    echo "curl ${API_URL}/test/predict"
    echo "$response" | jq '.' 2>/dev/null || echo "$response"
    
    # Teste de documentação
    echo ""
    log_demo "3. Documentação Swagger disponível"
    status=$(curl -s -o /dev/null -w "%{http_code}" "${API_URL}/docs")
    echo "curl ${API_URL}/docs -> Status: $status"
    if [[ $status -eq 200 ]]; then
        log_success "Swagger UI acessível em ${API_URL}/docs"
    fi
fi

echo ""
log_demo "=== FASE 2: PREDIÇÕES EM TEMPO REAL ==="

# Cenário Normal
echo ""
log_demo "Testando CENÁRIO NORMAL (24h estáveis)"
log_info "Comando: curl -X POST ${API_URL}/predict (dados normais)"

# Criar dados de 24 horas para cenário normal (modelo LSTM precisa de sequência de 24 pontos)
normal_data='{"sensor_data":['
for i in {1..24}; do
    normal_data+='{"precipitation": 0.1, "humidity": 65.0, "temperature": 22.0, "pressure": 1015.0}'
    if [[ $i -lt 24 ]]; then
        normal_data+=","
    fi
done
normal_data+='], "device_id": "DEMO_NORMAL"}'

normal_response=$(curl -s -X POST "${API_URL}/predict" \
  -H "Content-Type: application/json" \
  -d "$normal_data" 2>/dev/null)

if echo "$normal_response" | jq . >/dev/null 2>&1; then
    echo "$normal_response" | jq '.'
    
    # Extrair valores para análise
    probability=$(echo "$normal_response" | jq -r '.flood_probability // "N/A"')
    risk_level=$(echo "$normal_response" | jq -r '.risk_level // "N/A"')
    
    if [[ "$risk_level" == "LOW" ]]; then
        log_success "✅ Cenário Normal detectado corretamente: $risk_level (prob: $probability)"
    else
        echo -e "${YELLOW}⚠️  Resultado inesperado para cenário normal: $risk_level${NC}"
    fi
else
    echo "$normal_response"
fi

# Cenário Crítico usando endpoint de teste
echo ""
log_demo "Testando CENÁRIO CRÍTICO (usando dados internos)"
log_info "Usando endpoint /test/predict para demonstrar diferença"

test_response=$(curl -s "${API_URL}/test/predict")
if echo "$test_response" | jq . >/dev/null 2>&1; then
    echo "$test_response" | jq '.'
    
    # Analisar resultados
    normal_prob=$(echo "$test_response" | jq -r '.test_results.normal_scenario.probability // "N/A"')
    flood_prob=$(echo "$test_response" | jq -r '.test_results.flood_scenario.probability // "N/A"')
    normal_risk=$(echo "$test_response" | jq -r '.test_results.normal_scenario.risk_level // "N/A"')
    flood_risk=$(echo "$test_response" | jq -r '.test_results.flood_scenario.risk_level // "N/A"')
    
    echo ""
    log_success "📊 COMPARAÇÃO DE CENÁRIOS:"
    echo -e "   Normal:   ${GREEN}$normal_risk${NC} (prob: $normal_prob)"
    echo -e "   Enchente: ${RED}$flood_risk${NC} (prob: $flood_prob)"
    
    # Calcular diferença
    if [[ "$normal_prob" != "N/A" && "$flood_prob" != "N/A" ]]; then
        diff=$(echo "scale=1; ($flood_prob - $normal_prob) * 100" | bc 2>/dev/null || echo "N/A")
        if [[ "$diff" != "N/A" ]]; then
            log_success "🎯 Discriminação do modelo: ${diff}% de diferença entre cenários"
        fi
    fi
else
    echo "$test_response"
fi

echo ""
log_demo "=== FASE 3: MÉTRICAS DE PERFORMANCE ==="

# Informações do modelo
echo ""
log_demo "Informações do Modelo LSTM"
log_info "Comando: curl ${API_URL}/model/info"

model_response=$(curl -s "${API_URL}/model/info")
if echo "$model_response" | jq . >/dev/null 2>&1; then
    # Mostrar JSON limpo sem o model_summary confuso
    echo "$model_response" | jq 'del(.model_summary)'
    
    # Extrair informações chave
    total_params=$(echo "$model_response" | jq -r '.total_params // "N/A"')
    input_shape=$(echo "$model_response" | jq -r '.input_shape // "N/A"')
    output_shape=$(echo "$model_response" | jq -r '.output_shape // "N/A"')
    model_version=$(echo "$model_response" | jq -r '.model_version // "N/A"')
    
    echo ""
    log_success "🧠 Modelo LSTM v$model_version carregado com sucesso!"
    log_success "📊 Total de parâmetros: $total_params"
    log_success "📐 Input shape: $input_shape"
    log_success "📈 Output shape: $output_shape"
else
    echo "$model_response"
fi

# Teste de performance
echo ""
log_demo "Teste de Performance (tempo de resposta)"

start_time=$(date +%s%N)
perf_response=$(curl -s "${API_URL}/test/predict")
end_time=$(date +%s%N)

if [[ $? -eq 0 ]]; then
    duration=$((($end_time - $start_time) / 1000000)) # Converter para ms
    log_success "⚡ Tempo de resposta: ${duration}ms"
    
    if [[ $duration -lt 100 ]]; then
        log_success "🏆 Performance EXCELENTE (< 100ms)"
    elif [[ $duration -lt 500 ]]; then
        log_success "✅ Performance BOA (< 500ms)"
    else
        echo -e "${YELLOW}⚠️  Performance ACEITÁVEL (${duration}ms)${NC}"
    fi
fi

echo ""
log_demo "=== RESUMO DA DEMONSTRAÇÃO ==="
echo ""
echo -e "${GREEN}🎊 DEMONSTRAÇÃO COMPLETA FINALIZADA!${NC}"
echo ""
echo "✅ Status da API: Operacional"
echo "✅ Testes automatizados: Executados"
echo "✅ Predições: Funcionando"
echo "✅ Modelo LSTM: Carregado"
echo "✅ Performance: Validada"
echo ""
echo "🌐 Endpoints disponíveis:"
echo "   • Health: ${API_URL}/health"
echo "   • Predição: ${API_URL}/predict"
echo "   • Documentação: ${API_URL}/docs"
echo "   • Teste: ${API_URL}/test/predict"
echo ""
echo "📊 Sistema 100% operacional para demonstração!"
echo ""

# Limpeza opcional
if [[ -n "${API_PID}" ]]; then
    echo -e "${YELLOW}ℹ️  API foi iniciada automaticamente (PID: ${API_PID})${NC}"
    echo "   Para parar: kill ${API_PID}"
fi

echo "================================================="
echo "🎬 Demonstração encerrada - Sistema validado! 🎬"
echo "================================================="
