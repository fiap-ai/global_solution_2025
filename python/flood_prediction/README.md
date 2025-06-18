# 🌧️ Flood Prediction - Core ML Module

## 🎯 Descrição
Módulo responsável pelo processamento de dados meteorológicos do INMET e treinamento de modelo LSTM para predição de enchentes na região serrana do Rio de Janeiro.

## 🚀 Quick Start
```bash
# Setup ambiente único
cd python/
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Processar dados INMET
pip install -r flood_prediction/requirements.txt
python flood_prediction/data_processor.py

# Treinar modelo
python flood_prediction/train.py
```

## 📋 Pré-requisitos
- **Python 3.8+** (recomendado 3.9 ou superior)
- **16GB+ RAM** (para processamento dos dados)
- **2GB+ espaço em disco** (para dados processados e modelo)
- **Dados INMET** (já incluídos em `../../data/inmet/bd/`)

## 📁 Estrutura do Módulo
```
flood_prediction/
├── requirements.txt        # Dependências TensorFlow, pandas, etc.
├── README.md              # Esta documentação
├── data_processor.py      # Processamento dados INMET das 2 cidades
├── model.py              # Arquitetura LSTM para séries temporais
├── train.py              # Pipeline completo de treinamento
└── utils.py              # Funções auxiliares (criado automaticamente)
```

## 🏛️ Dados de Entrada
### Estações Meteorológicas INMET
- **🏔️ Teresópolis** (A618): 2015-2025 - Região serrana RJ
- **🌿 Nova Friburgo** (A624): 2015-2025 - Região serrana RJ

### Features Meteorológicas
- **☔ Precipitação** - Total horário em mm/h
- **💧 Umidade** - Relativa do ar em %
- **🌡️ Temperatura** - Do ar em °C
- **🌀 Pressão** - Atmosférica em mB

## 🧠 Modelo LSTM
### Arquitetura
```
Input: (24h, 4 features) → LSTM(50) → LSTM(50) → Dense(25) → Sigmoid → Output: P(enchente)
```

### Critérios de Enchente
- Precipitação > 20mm/h por 2h+ consecutivas
- Umidade > 90% + Precipitação > 10mm/h  
- Precipitação acumulada 6h > 50mm
- Queda de pressão + precipitação simultânea

### Meta de Performance
- **Accuracy**: > 75%
- **Precision**: > 70% (poucos falsos positivos)
- **Recall**: > 70% (detectar eventos reais)

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
pip install -r flood_prediction/requirements.txt

# Verificar instalação TensorFlow
python -c "import tensorflow as tf; print(f'TensorFlow: {tf.__version__}')"
```

### 3. Verificar Dados
```bash
# Verificar se dados INMET existem
ls ../../data/inmet/bd/2024/  # Deve mostrar arquivos CSV

# Verificar dados das cidades foco
ls ../../data/inmet/bd/*/INMET_SE_RJ_A618_TERESOPOLIS*
ls ../../data/inmet/bd/*/INMET_SE_RJ_A624_NOVA*FRIBURGO*
```

## 🔧 Como Usar

### Passo 1: Processar Dados INMET
```bash
python data_processor.py
```

**O que acontece:**
- ✅ Busca arquivos CSV das 2 cidades (2015-2025)
- ✅ Limpa dados inválidos e normaliza formatos
- ✅ Cria labels de enchente baseado em condições reais
- ✅ Gera sequências de 24h para LSTM
- ✅ Salva dados processados em `../../data/processed/`

**Resultado esperado:**
```
🌧️  PROCESSANDO DADOS INMET - PREDIÇÃO DE ENCHENTES
============================================================

📍 Estação: TERESOPOLIS (A618)
   Arquivos encontrados: 10
✅ 87,600 registros processados
📊 Período: 2015-01-01 a 2025-05-31

📍 Estação: NOVA_FRIBURGO (A624)  
   Arquivos encontrados: 10
✅ 87,240 registros processados
📊 Período: 2015-01-01 a 2025-05-31

🎯 RESULTADO FINAL:
   Total de registros: 174,840
   Total de sequências: 174,816
   Risco positivo: 8,741/174,816 (5.0%)

💾 DataFrame salvo: ../../data/processed/inmet_rj_processed.csv
💾 Sequências salvas: ../../data/processed/flood_sequences.npz
📊 Estatísticas salvas: ../../data/processed/inmet_stats.json
```

### Passo 2: Treinar Modelo
```bash
python train.py
```

**O que acontece:**
- ✅ Carrega dados processados automaticamente
- ✅ Divide dados em treino/validação/teste (60/20/20)
- ✅ Balanceia dataset para melhor aprendizado
- ✅ Treina modelo LSTM por 50 épocas
- ✅ Salva modelo treinado e artefatos

**Resultado esperado:**
```
🌧️  PIPELINE COMPLETO - TREINAMENTO MODELO ENCHENTES
============================================================
⚙️  Configurações:
   LSTM Units: 64
   Epochs: 50
   Batch Size: 32
   Balance Data: True

📂 Carregando dados: ../../data/processed/flood_sequences.npz
✅ Dados carregados:
   Shape X: (174816, 24, 4)
   Shape y: (174816,)

🔄 Preparando dados para treinamento...
📊 Classes balanceadas: {0: 8741, 1: 8741}
✅ Dados preparados:
   Treino: (10489, 24, 4) - Classes: {0: 5244, 1: 5245}
   Validação: (3497, 24, 4) - Classes: {0: 1748, 1: 1749}
   Teste: (3496, 24, 4) - Classes: {0: 1749, 1: 1747}

🚀 INICIANDO TREINAMENTO DO MODELO
==================================================
Model: "sequential"
_________________________________________________________________
 Layer (type)                Output Shape              Param #   
=================================================================
 lstm_1 (LSTM)              (None, 24, 64)            17664     
 batch_normalization (BatchN (None, 24, 64)           256       
 dropout (Dropout)          (None, 24, 64)            0         
 lstm_2 (LSTM)              (None, 64)                33024     
 batch_normalization_1 (Batc (None, 64)               256       
 dropout_1 (Dropout)        (None, 64)                0         
 dense_1 (Dense)            (None, 25)                1625      
 dropout_2 (Dropout)        (None, 25)                0         
 output (Dense)             (None, 1)                 26        
=================================================================
Total params: 52,851

Epoch 1/50
328/328 [==============================] - 45s - loss: 0.5234 - accuracy: 0.7456
...
Epoch 23/50
328/328 [==============================] - 35s - loss: 0.3891 - accuracy: 0.8234

📊 AVALIAÇÃO FINAL DO MODELO
==================================================
   Loss: 0.3654
   Accuracy: 0.8421
   Precision: 0.8156
   Recall: 0.8789
   F1-Score: 0.8461

💾 SALVANDO MODELO E ARTEFATOS
==================================================
💾 Modelo salvo: ../../data/models/flood_lstm_model.h5
💾 Scaler salvo: ../../data/models/flood_scaler.pkl
📊 Resultados salvos: ../../data/models/training_results.json
📊 Gráfico salvo: ../../data/models/plots/training_history.png

🎯 TREINAMENTO CONCLUÍDO COM SUCESSO!
   Accuracy: 0.842
   Precision: 0.816  
   Recall: 0.879
   F1-Score: 0.846
```

## ✅ Como Testar

### Teste 1: Verificar Processamento
```bash
# Verificar se dados foram processados
ls ../../data/processed/
# Deve mostrar: flood_sequences.npz, inmet_rj_processed.csv, inmet_stats.json

# Verificar estatísticas
cat ../../data/processed/inmet_stats.json
```

### Teste 2: Verificar Modelo Treinado
```bash
# Verificar se modelo foi salvo
ls ../../data/models/
# Deve mostrar: flood_lstm_model.h5, flood_scaler.pkl, training_results.json

# Verificar resultados do treinamento
cat ../../data/models/training_results.json
```

### Teste 3: Testar Predição Manual
```python
# Teste simples em Python
import numpy as np
import tensorflow as tf
import joblib

# Carrega modelo e scaler
model = tf.keras.models.load_model('../../data/models/flood_lstm_model.h5')
scaler = joblib.load('../../data/models/flood_scaler.pkl')

# Dados de teste (24h normais)
test_data = np.array([[0.0, 65.0, 22.0, 1015.0]] * 24)  # sem chuva
test_scaled = scaler.transform(test_data).reshape(1, 24, 4)
prob = model.predict(test_scaled)[0][0]
print(f"Risco de enchente: {prob:.3f} ({'ALTO' if prob > 0.5 else 'BAIXO'})")

# Dados de teste (chuva intensa)
rain_data = np.array([[25.0, 95.0, 24.0, 1005.0]] * 24)  # chuva forte
rain_scaled = scaler.transform(rain_data).reshape(1, 24, 4)
prob_rain = model.predict(rain_scaled)[0][0]
print(f"Risco com chuva: {prob_rain:.3f} ({'ALTO' if prob_rain > 0.5 else 'BAIXO'})")
```

## 🐛 Troubleshooting

### Erro: "No module named 'tensorflow'"
```bash
# Reativar ambiente virtual
source venv_flood/bin/activate  # Linux/Mac
# OU venv_flood\Scripts\activate  # Windows

# Reinstalar TensorFlow
pip install --upgrade tensorflow
```

### Erro: "File not found: INMET data"
```bash
# Verificar se dados INMET estão presentes
ls ../../data/inmet/bd/
# Se vazio, os dados não foram baixados corretamente
```

### Erro: "Memory Error" durante treinamento
```bash
# Reduzir batch size no train.py
# Editar linha 'batch_size': 32 para 'batch_size': 16
```

### Erro: "Model accuracy too low"
```bash
# Aumentar épocas de treinamento
# Editar linha 'epochs': 50 para 'epochs': 100

# OU verificar balanceamento dos dados
python -c "
import numpy as np
data = np.load('../../data/processed/flood_sequences.npz')
print('Classes:', np.unique(data['y'], return_counts=True))
"
```

### Performance Baixa
- **Accuracy < 70%**: Dados insuficientes ou mal balanceados
- **Loss não converge**: Learning rate muito alto/baixo
- **Overfitting**: Aumentar dropout ou reduzir épocas

## 📊 Arquivos Gerados

### Dados Processados (`../../data/processed/`)
- `inmet_rj_processed.csv` - Dataset completo limpo
- `flood_sequences.npz` - Sequências 24h para LSTM
- `inmet_stats.json` - Estatísticas do processamento

### Modelo Treinado (`../../data/models/`)
- `flood_lstm_model.h5` - Modelo LSTM treinado
- `flood_scaler.pkl` - Normalizador MinMax ajustado
- `training_results.json` - Métricas de performance
- `plots/training_history.png` - Gráficos de treinamento

## 🔗 Próximos Passos
1. **API FastAPI**: Usar modelo para predições em tempo real
2. **Integração ESP32**: Receber dados de sensores físicos
3. **AWS Lambda**: Deploy do modelo na nuvem
4. **Dashboard**: Visualização em tempo real

## 📞 Suporte
- Verificar logs detalhados durante execução
- Cada script mostra progress e estatísticas
- Em caso de erro, verificar pré-requisitos primeiro
