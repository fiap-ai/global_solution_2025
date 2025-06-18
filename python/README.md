# Python - Sistema de Monitoramento de Enchentes
## Global Solution 2025

---

## 📁 ESTRUTURA DO PROJETO

```
python/
├── README.md                    # Este arquivo
├── data_scraper/               # Coleta automática de dados
│   ├── disasters_scraper.py    # Script principal de scraping
│   └── requirements.txt        # Dependências do scraper
├── flood_prediction/           # Rede Neural e ML (a ser criado)
├── api/                       # FastAPI endpoints (a ser criado)
└── data_collector/            # Processamento de dados (a ser criado)
```

---

## 🔧 DATA SCRAPER

### **Descrição**
Script automatizado para coleta de dados de enchentes do site oficial DisastersCharter.org usando sua API interna.

### **Funcionalidades**
- ✅ Coleta automática de eventos de enchentes
- ✅ Busca por múltiplas regiões geográficas
- ✅ Extração de dados estruturados (JSON)
- ✅ Remoção de duplicatas
- ✅ Logs detalhados de execução
- ✅ Rate limiting respeitoso
- ✅ Tratamento de erros robusto

### **Como Usar**

#### **1. Instalação**
```bash
cd python/data_scraper
pip install -r requirements.txt
```

#### **2. Execução**
```bash
# Executar coleta completa
python disasters_scraper.py

# Ou importar como módulo
python -c "from disasters_scraper import DisastersCharterScraper; scraper = DisastersCharterScraper(); data = scraper.get_flood_activations(); print(f'Coletados {len(data)} eventos')"
```

### **Dados Coletados**

#### **Estrutura JSON de Saída**
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
  "collected_at": "2025-06-17T01:27:00"
}
```

#### **Arquivos Gerados**
- `../../data/raw/flood_events_raw.json` - Dados brutos coletados
- `../../data/processed/flood_events.json` - Dados processados com metadados

### **Configurações**

#### **Regiões Cobertas**
- South America
- Africa  
- Asia
- Europe
- North America

#### **Parâmetros Ajustáveis**
```python
# No código disasters_scraper.py
self.delay_between_requests = 2  # Segundos entre requests
self.max_retries = 3            # Tentativas em caso de erro
```

### **Logs de Exemplo**
```
INFO:__main__:Iniciando coleta de dados de enchentes...
INFO:__main__:Buscando enchentes em: south america
INFO:__main__:Extraídas 3 ativações
INFO:__main__:Coletadas 3 ativações de south america
INFO:__main__:Total de ativações únicas coletadas: 15
INFO:__main__:Dados salvos em: ../../data/raw/flood_events_raw.json
INFO:__main__:Coleta concluída! 15 eventos coletados.
INFO:__main__:Países com mais eventos:
INFO:__main__:  Bolivia: 3 eventos
INFO:__main__:  Argentina: 2 eventos
```

---

## 🧠 FLOOD PREDICTION (A SER IMPLEMENTADO)

### **Planejado**
- Rede Neural LSTM para predição de enchentes
- Processamento de séries temporais
- Treinamento com dados coletados
- Modelo salvo em formato .h5

---

## 🚀 API (A SER IMPLEMENTADO)

### **Planejado**
- FastAPI para endpoints de predição
- Endpoint `/predict` para análise em tempo real
- Endpoint `/health` para status
- Documentação automática em `/docs`

---

## 📊 DATA COLLECTOR (A SER IMPLEMENTADO)

### **Planejado**
- Processamento de dados coletados
- Normalização e limpeza
- Preparação para Machine Learning
- Integração com APIs climáticas

---

## 🔄 WORKFLOW COMPLETO

### **1. Coleta de Dados**
```bash
cd python/data_scraper
python disasters_scraper.py
```

### **2. Processamento (Futuro)**
```bash
cd python/data_collector  
python process_data.py
```

### **3. Treinamento ML (Futuro)**
```bash
cd python/flood_prediction
python train_model.py
```

### **4. API Local (Futuro)**
```bash
cd python/api
uvicorn main:app --reload
```

---

## 📋 DEPENDÊNCIAS

### **Data Scraper**
- `requests>=2.25.0` - HTTP requests

### **Futuras Dependências**
- `tensorflow>=2.10.0` - Rede Neural
- `fastapi>=0.68.0` - API endpoints
- `pandas>=1.3.0` - Manipulação de dados
- `numpy>=1.21.0` - Computação numérica
- `scikit-learn>=1.0.0` - ML utilities

---

## ⚠️ CONSIDERAÇÕES IMPORTANTES

### **Rate Limiting**
- Delay de 2 segundos entre requests
- Headers que simulam browser real
- Respeito aos termos de uso do site

### **Dados Reais**
- ✅ Fonte oficial: DisastersCharter.org
- ✅ Dados estruturados e validados
- ✅ Coordenadas geográficas precisas
- ✅ Timestamps e metadados completos

### **Qualidade dos Dados**
- Remoção automática de duplicatas
- Validação de campos obrigatórios
- Logs detalhados para debugging
- Tratamento de erros robusto

---

## 🎯 PRÓXIMOS PASSOS

1. **Executar data_scraper** para coletar dados iniciais
2. **Implementar flood_prediction** com LSTM
3. **Criar API FastAPI** para predições
4. **Integrar com ESP32** via AWS
5. **Documentar resultados** no PDF final

---

*Este módulo Python é parte integral do sistema de monitoramento de enchentes para a Global Solution 2025.*
