# Data Scraper - DisastersCharter.org
## Coleta Automática de Dados de Enchentes

---

## 📋 DESCRIÇÃO

Script Python para coleta automática de dados de enchentes do site oficial **DisastersCharter.org** usando sua API interna. Desenvolvido especificamente para a Global Solution 2025.

---

## 🚀 FUNCIONALIDADES

- ✅ **Coleta Automática**: Busca eventos de enchentes em múltiplas regiões
- ✅ **API Interna**: Utiliza a API real do DisastersCharter.org
- ✅ **Dados Estruturados**: Extrai JSON com metadados completos
- ✅ **Múltiplas Regiões**: South America, Africa, Asia, Europe, North America
- ✅ **Rate Limiting**: Respeita limites do servidor (2s entre requests)
- ✅ **Deduplicação**: Remove eventos duplicados automaticamente
- ✅ **Logs Detalhados**: Acompanhamento completo da execução
- ✅ **Tratamento de Erros**: Robusto contra falhas de rede

---

## 📦 INSTALAÇÃO

### **Pré-requisitos**
- Python 3.7+
- pip3

### **Setup Ambiente Único**
```bash
# Setup ambiente único
cd python/
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalar dependências
pip install -r data_scraper/requirements.txt
```

---

## 🔧 USO

### **Execução Simples**
```bash
# Setup ambiente único
cd python/
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Executar scraper
python data_scraper/disasters_scraper.py
```

### **Outros Scripts**
```bash
# Enriquecer dados com duração
python data_scraper/enrich_duration.py

# Baixar relatórios
python data_scraper/download_reports.py

# Baixar imagens
python data_scraper/download_images.py
```

### **Como Módulo Python**
```python
from disasters_scraper import DisastersCharterScraper

# Criar instância
scraper = DisastersCharterScraper()

# Coletar dados
flood_data = scraper.get_flood_activations()

print(f"Coletados {len(flood_data)} eventos de enchentes")
```

### **Personalizar Regiões**
```python
# Buscar apenas América do Sul
data = scraper.get_flood_activations(location="south america")

# Buscar múltiplas regiões específicas
regions = ["africa", "asia"]
for region in regions:
    data = scraper.get_flood_activations(location=region)
```

### **Enriquecimento Completo com Duração**
```bash
# Executar enriquecimento completo de TODOS os eventos
python enrich_duration.py
```

**Resultados do Enriquecimento:**
- ✅ **27 eventos processados** - todos os eventos coletados
- ✅ **Informações de impacto extraídas** - mortes, deslocados, etc.
- ✅ **Duração identificada** - quando disponível (ex: México 3 dias)
- ✅ **Estrutura completa** - campo `duration` em todos os eventos

**Arquivo gerado:**
```
../../data/processed/flood_events_enriched_complete.json
```

### **Download de Relatórios Técnicos**
```bash
# Baixar 5 relatórios técnicos oficiais
python download_reports.py
```

**Resultados do Download:**
- ✅ **5 relatórios baixados** - meta atingida
- ✅ **Relatórios anuais** - Charter Annual Report 2022 e 2023
- ✅ **Documentos técnicos** - Brand Guidelines
- ✅ **Newsletters** - Issues 29 e 30
- ✅ **Metadados salvos** - reports_metadata.json

**Arquivos gerados:**
```
../../data/reports/
├── report_01_Charter_Annual_Report_23.pdf
├── report_02_Charter_Annual_Report_22.pdf
├── report_03_The_International_Charter_Brand_Guidelines.pdf
├── report_04_Charter_Newsletter_Issue_30.pdf
├── report_05_Charter_Newsletter_Issue_29.pdf
└── reports_metadata.json
```

### **Download de Imagens de Satélite**
```bash
# Baixar todas as imagens de satélite disponíveis (quickviews de enchentes)
python download_images.py
```

**Resultados do Download:**
- ✅ **12 imagens baixadas** - superou expectativas (6 quickviews × 2 imagens cada)
- ✅ **Imagens pré e pós-desastre** - comparação temporal completa
- ✅ **Cobertura global** - Espanha, Sri Lanka, Brasil, Escócia, Rússia
- ✅ **Satélites diversos** - Sentinel-1, Amazonia-1, CBERS-4, RCM, SAOCOM
- ✅ **Metadados completos** - país, satélite, dimensões, copyright

**Arquivos gerados:**
```
../../data/images/
├── satellite_01_Flooding_of_the_Albufera_National_Park_Post_disast.jpg
├── satellite_02_Flooding_of_the_Albufera_National_Park_Pre_disaste.jpg
├── satellite_03_Sentinel_1_RedCyan_composites_near_Hambatota_in_Sr.jpg
├── satellite_04_Sentinel_1_RedCyan_composites_near_Hambatota_in_Sr.jpg
├── satellite_05_Flooding_Event_in_Rio_Grande_do_Sul_Brazil_Post_di.jpg
├── satellite_06_Flooding_Event_in_Rio_Grande_do_Sul_Brazil_Pre_dis.jpg
├── satellite_07_Flooding_Event_in_Rio_Grande_do_Sul_state_Brazil_P.jpg
├── satellite_08_Flooding_Event_in_Rio_Grande_do_Sul_state_Brazil_P.jpg
├── satellite_09_Flooded_areas_in_Central_Scotland_Post_disaster.jpg
├── satellite_10_Flooded_areas_in_Central_Scotland_Pre_disaster.jpg
├── satellite_11_Floods_along_river_Reka_Ilistaya_Post_disaster.jpg
├── satellite_12_Floods_along_river_Reka_Ilistaya_Pre_disaster.jpg
└── images_metadata.json
```

---

## 📊 DADOS COLETADOS

### **Estrutura JSON**
```json
{
  "activation_id": "955",
  "title": "Flood in Bolivia",
  "date": "2025-01-18T00:00:00",
  "timestamp": 1742515200000,
  "location": {
    "country": "Bolivia",
    "region": "south america",
    "latitude": -22.277708727860684,
    "longitude": -62.614670721505604
  },
  "metadata": {
    "slug": "flood-in-bolivia-activation-955-",
    "article_id": "31235618",
    "external_reference": "ACT-1091",
    "keywords": "floods, bolivia, 2025, activation",
    "disaster_types": ["floods"]
  },
  "disaster_type": "flood",
  "severity": "medium",
  "data_source": "disasterscharter.org",
  "collected_at": "2025-06-17T01:36:00"
}
```

### **Campos Principais**
- **activation_id**: ID único do evento
- **title**: Título descritivo
- **date**: Data do evento (ISO format)
- **location**: País, região e coordenadas
- **metadata**: Dados técnicos adicionais
- **severity**: Estimativa de severidade (low/medium/high)

---

## 📁 ARQUIVOS GERADOS

### **Localização**
```
../../data/raw/flood_events_raw.json      # Dados brutos
../../data/processed/flood_events.json    # Dados processados + metadados
```

### **Dados Processados**
```json
{
  "metadata": {
    "total_events": 15,
    "collection_date": "2025-06-17T01:36:00",
    "source": "disasterscharter.org",
    "regions_covered": ["south america", "africa", "asia"],
    "date_range": {
      "earliest": "2024-01-15T00:00:00",
      "latest": "2025-01-18T00:00:00"
    }
  },
  "events": [...]
}
```

---

## 🔧 CONFIGURAÇÕES

### **Parâmetros Ajustáveis**
```python
class DisastersCharterScraper:
    def __init__(self):
        self.delay_between_requests = 2  # Segundos entre requests
        self.max_retries = 3            # Tentativas em caso de erro
```

### **Headers HTTP**
O script usa headers que simulam um browser real para evitar bloqueios:
- User-Agent: Chrome/136.0.0.0
- Accept-Language: pt-BR,pt;q=0.9,en-US;q=0.8
- Referer: https://disasterscharter.org/activations

---

## 📈 EXEMPLO DE EXECUÇÃO

```
INFO:__main__:Iniciando coleta de dados de enchentes...
INFO:__main__:Buscando enchentes em: south america
INFO:__main__:Extraídas 3 ativações
INFO:__main__:Coletadas 3 ativações de south america
INFO:__main__:Buscando enchentes em: africa
INFO:__main__:Extraídas 5 ativações
INFO:__main__:Coletadas 5 ativações de africa
INFO:__main__:Total de ativações únicas coletadas: 15
INFO:__main__:Dados salvos em: ../../data/raw/flood_events_raw.json
INFO:__main__:Coleta concluída! 15 eventos coletados.
INFO:__main__:Países com mais eventos:
INFO:__main__:  Kazakhstan: 2 eventos
INFO:__main__:  Russian Federation: 2 eventos
```

---

## 🌍 REGIÕES COBERTAS

- **South America**: Brasil, Argentina, Peru, Bolívia, etc.
- **Africa**: Nigéria, Congo, África do Sul, etc.
- **Asia**: Cazaquistão, China, Índia, etc.
- **Europe**: Alemanha, França, Itália, etc.
- **North America**: EUA, Canadá, México, etc.

---

## ⚠️ CONSIDERAÇÕES TÉCNICAS

### **Rate Limiting**
- Delay de 2 segundos entre requests
- Máximo 3 tentativas por região
- Headers que simulam browser real

### **Tratamento de Erros**
- Timeout de 30 segundos por request
- Logs detalhados de erros
- Continuação mesmo com falhas parciais

### **Qualidade dos Dados**
- Validação de campos obrigatórios
- Remoção automática de duplicatas
- Conversão de timestamps para ISO format
- Estimativa de severidade baseada no título

---

## 🔍 DEBUGGING

### **Logs Detalhados**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### **Verificar Dados**
```bash
# Verificar arquivos gerados
ls -la ../../data/raw/
ls -la ../../data/processed/

# Visualizar dados coletados
python3 -c "import json; print(json.dumps(json.load(open('../../data/processed/flood_events.json')), indent=2)[:500])"
```

---

## 🎯 INTEGRAÇÃO COM O PROJETO

Este scraper é parte do sistema completo:

1. **Data Scraper** ← Você está aqui
2. **Data Processor** → Limpa e prepara dados
3. **ML Training** → Treina rede neural LSTM
4. **FastAPI** → Serve predições
5. **ESP32** → Coleta dados de sensores
6. **AWS Integration** → Processa em tempo real

---

## 📝 NOTAS IMPORTANTES

- ✅ **Dados Reais**: Fonte oficial DisastersCharter.org
- ✅ **Conformidade**: Respeita termos de uso do site
- ✅ **Atualizado**: Baseado na API atual (2025)
- ✅ **Testado**: Funcional em macOS/Linux/Windows

---

*Script desenvolvido para Global Solution 2025 - FIAP*
