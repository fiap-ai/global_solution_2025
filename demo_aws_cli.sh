#!/bin/bash

# Demonstração AWS CLI - Global Solution 2025
# Script para demonstrar configuração e conectividade AWS

echo "☁️  DEMONSTRAÇÃO AWS CLI - GLOBAL SOLUTION 2025"
echo "==============================================="
echo "Gabriel Mule Monteiro - RM560586"
echo "Sistema de Predição de Enchentes"
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
    echo -e "${CYAN}🎬 DEMO AWS: $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

echo ""
log_demo "=== FASE 1: VERIFICAÇÃO DE CREDENCIAIS AWS ==="

# Verificar AWS CLI
echo ""
log_demo "1. Verificando instalação do AWS CLI"
if command -v aws >/dev/null 2>&1; then
    aws_version=$(aws --version 2>&1 | head -n1)
    log_success "AWS CLI instalado: $aws_version"
else
    log_error "AWS CLI não encontrado. Instale com: pip install awscli"
    exit 1
fi

# Verificar credenciais
echo ""
log_demo "2. Testando credenciais AWS"
log_info "Comando: aws sts get-caller-identity"

caller_identity=$(aws sts get-caller-identity 2>/dev/null)
if [[ $? -eq 0 ]]; then
    echo "$caller_identity" | jq '.' 2>/dev/null || echo "$caller_identity"
    
    # Extrair informações
    account_id=$(echo "$caller_identity" | jq -r '.Account // "N/A"' 2>/dev/null)
    user_arn=$(echo "$caller_identity" | jq -r '.Arn // "N/A"' 2>/dev/null)
    user_id=$(echo "$caller_identity" | jq -r '.UserId // "N/A"' 2>/dev/null)
    
    echo ""
    log_success "🏦 Account ID: $account_id"
    log_success "👤 User ARN: $user_arn"
    log_success "🆔 User ID: $user_id"
    
    if [[ "$account_id" == "831926593713" ]]; then
        log_success "✅ Conta correta identificada: flood-monitor-dev"
    fi
else
    log_error "Falha na autenticação AWS. Verifique credenciais com: aws configure"
    exit 1
fi

echo ""
log_demo "=== FASE 2: AWS IoT CORE - THINGS E CERTIFICADOS ==="

# Listar Things IoT
echo ""
log_demo "3. Listando dispositivos IoT (Things)"
log_info "Comando: aws iot list-things"

things_response=$(aws iot list-things 2>/dev/null)
if [[ $? -eq 0 ]]; then
    echo "$things_response" | jq '.' 2>/dev/null || echo "$things_response"
    
    # Verificar se FloodMonitor01 existe
    thing_count=$(echo "$things_response" | jq '.things | length' 2>/dev/null || echo "0")
    flood_monitor=$(echo "$things_response" | jq -r '.things[] | select(.thingName == "FloodMonitor01") | .thingName' 2>/dev/null)
    
    echo ""
    log_success "📱 Total de Things: $thing_count"
    
    if [[ "$flood_monitor" == "FloodMonitor01" ]]; then
        log_success "🎯 FloodMonitor01 encontrado e configurado!"
        
        # Obter detalhes do Thing
        thing_details=$(aws iot describe-thing --thing-name "FloodMonitor01" 2>/dev/null)
        if [[ $? -eq 0 ]]; then
            echo ""
            log_info "Detalhes do FloodMonitor01:"
            echo "$thing_details" | jq '.' 2>/dev/null || echo "$thing_details"
        fi
    else
        log_warning "FloodMonitor01 não encontrado na lista"
    fi
else
    log_error "Falha ao listar Things IoT"
fi

# Listar certificados
echo ""
log_demo "4. Verificando certificados X.509"
log_info "Comando: aws iot list-certificates"

certificates_response=$(aws iot list-certificates 2>/dev/null)
if [[ $? -eq 0 ]]; then
    cert_count=$(echo "$certificates_response" | jq '.certificates | length' 2>/dev/null || echo "0")
    
    echo ""
    log_success "🔐 Total de certificados: $cert_count"
    
    if [[ $cert_count -gt 0 ]]; then
        echo ""
        log_info "Certificados disponíveis:"
        echo "$certificates_response" | jq '.certificates[] | {certificateId: .certificateId, status: .status, creationDate: .creationDate}' 2>/dev/null || echo "$certificates_response"
        
        # Verificar certificados ativos
        active_certs=$(echo "$certificates_response" | jq '[.certificates[] | select(.status == "ACTIVE")] | length' 2>/dev/null || echo "0")
        log_success "✅ Certificados ativos: $active_certs"
    else
        log_warning "Nenhum certificado encontrado"
    fi
else
    log_error "Falha ao listar certificados"
fi

echo ""
log_demo "=== FASE 3: POLÍTICAS E PERMISSÕES IoT ==="

# Listar políticas IoT
echo ""
log_demo "5. Verificando políticas IoT"
log_info "Comando: aws iot list-policies"

policies_response=$(aws iot list-policies 2>/dev/null)
if [[ $? -eq 0 ]]; then
    policy_count=$(echo "$policies_response" | jq '.policies | length' 2>/dev/null || echo "0")
    
    echo ""
    log_success "📋 Total de políticas: $policy_count"
    
    if [[ $policy_count -gt 0 ]]; then
        echo ""
        log_info "Políticas disponíveis:"
        echo "$policies_response" | jq '.policies[] | {policyName: .policyName, creationDate: .creationDate}' 2>/dev/null || echo "$policies_response"
        
        # Verificar se política FloodMonitor01-Policy existe
        flood_policy=$(echo "$policies_response" | jq -r '.policies[] | select(.policyName | contains("FloodMonitor")) | .policyName' 2>/dev/null)
        
        if [[ -n "$flood_policy" ]]; then
            log_success "🎯 Política FloodMonitor encontrada: $flood_policy"
            
            # Obter detalhes da política
            echo ""
            log_info "Detalhes da política $flood_policy:"
            policy_details=$(aws iot get-policy --policy-name "$flood_policy" 2>/dev/null)
            if [[ $? -eq 0 ]]; then
                echo "$policy_details" | jq '.' 2>/dev/null || echo "$policy_details"
            fi
        else
            log_warning "Política FloodMonitor não encontrada"
        fi
    fi
else
    log_error "Falha ao listar políticas IoT"
fi

echo ""
log_demo "=== FASE 4: VERIFICAÇÃO DE ARQUIVOS LOCAIS ==="

# Verificar estrutura aws/iot/
echo ""
log_demo "6. Verificando arquivos AWS locais"

if [[ -d "aws/iot" ]]; then
    log_success "📁 Diretório aws/iot/ encontrado"
    
    # Listar arquivos importantes
    echo ""
    log_info "Estrutura do projeto AWS:"
    find aws/iot -type f -name "*.pem" -o -name "*.json" -o -name "*.sh" -o -name "*Policy*" 2>/dev/null | while read file; do
        if [[ -f "$file" ]]; then
            size=$(ls -lh "$file" | awk '{print $5}')
            echo "   📄 $file ($size)"
        fi
    done
    
    # Verificar start.sh
    if [[ -f "aws/iot/start.sh" ]]; then
        echo ""
        log_success "🚀 Script start.sh encontrado"
        log_info "Execute: cd aws/iot && ./start.sh para testar MQTT"
    fi
    
    # Verificar certificados
    cert_files=$(find aws/iot -name "*.pem" 2>/dev/null | wc -l)
    if [[ $cert_files -gt 0 ]]; then
        log_success "🔐 $cert_files arquivo(s) de certificado encontrado(s)"
    else
        log_warning "Nenhum arquivo .pem encontrado"
    fi
    
else
    log_warning "Diretório aws/iot/ não encontrado"
fi

echo ""
log_demo "=== FASE 5: TESTE DE CONECTIVIDADE IoT ==="

# Verificar endpoint IoT
echo ""
log_demo "7. Obtendo endpoint IoT Core"
log_info "Comando: aws iot describe-endpoint --endpoint-type iot:Data-ATS"

endpoint_response=$(aws iot describe-endpoint --endpoint-type iot:Data-ATS 2>/dev/null)
if [[ $? -eq 0 ]]; then
    endpoint_address=$(echo "$endpoint_response" | jq -r '.endpointAddress // "N/A"' 2>/dev/null)
    
    echo ""
    log_success "🌐 IoT Endpoint: $endpoint_address"
    
    if [[ "$endpoint_address" != "N/A" && "$endpoint_address" != "null" ]]; then
        log_success "✅ Endpoint IoT Core ativo e acessível"
    fi
else
    log_error "Falha ao obter endpoint IoT"
fi

echo ""
log_demo "=== RESUMO DA CONFIGURAÇÃO AWS ==="
echo ""
echo -e "${GREEN}🎊 DEMONSTRAÇÃO AWS CLI CONCLUÍDA!${NC}"
echo ""
echo "✅ AWS CLI: Instalado e configurado"
echo "✅ Credenciais: Autenticadas (Account: $account_id)"
echo "✅ IoT Things: $thing_count configurado(s)"
echo "✅ Certificados: $cert_count disponível(is)"
echo "✅ Políticas: $policy_count configurada(s)"
echo "✅ Estrutura local: Organizada"
echo ""

if [[ "$thing_count" -gt 0 && "$cert_count" -gt 0 && "$policy_count" -gt 0 ]]; then
    log_success "🏆 AWS IoT Core 100% CONFIGURADO!"
    echo ""
    echo "🚀 Próximos passos:"
    echo "   1. Execute: cd aws/iot && ./start.sh"
    echo "   2. Teste MQTT com demo_iot_mqtt.sh"
    echo "   3. Verifique Lambda com demo_lambda_logs.sh"
else
    log_warning "⚠️  Configuração AWS incompleta"
    echo ""
    echo "🔧 Ações necessárias:"
    if [[ $thing_count -eq 0 ]]; then
        echo "   • Criar Thing: aws iot create-thing --thing-name FloodMonitor01"
    fi
    if [[ $cert_count -eq 0 ]]; then
        echo "   • Gerar certificados: aws iot create-keys-and-certificate"
    fi
    if [[ $policy_count -eq 0 ]]; then
        echo "   • Criar política: aws iot create-policy"
    fi
fi

echo ""
echo "================================================="
echo "☁️  Demonstração AWS encerrada - Pronto para IoT! ☁️"
echo "================================================="
