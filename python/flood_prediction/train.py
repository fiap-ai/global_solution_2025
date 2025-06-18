#!/usr/bin/env python3
"""
Train Script - Flood Prediction
Script principal para treinar modelo LSTM de predição de enchentes.
"""

import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import joblib
import json
from datetime import datetime

from data_processor import InmetDataProcessor
from model import FloodLSTMModel, create_balanced_dataset

class FloodTrainer:
    """Classe principal para treinamento do modelo"""
    
    def __init__(self, output_dir="../data/models"):
        self.output_dir = output_dir
        self.scaler = MinMaxScaler()
        self.model = None
        self.results = {}
        
        # Cria diretório de saída
        os.makedirs(output_dir, exist_ok=True)
        
    def load_processed_data(self, data_path="../data/processed/flood_sequences.npz"):
        """Carrega dados processados"""
        
        if not os.path.exists(data_path):
            print(f"❌ Arquivo não encontrado: {data_path}")
            print("   Execute primeiro: python data_processor.py")
            return None, None
            
        print(f"📂 Carregando dados: {data_path}")
        
        data = np.load(data_path)
        X = data['X']
        y = data['y']
        
        print(f"✅ Dados carregados:")
        print(f"   Shape X: {X.shape}")
        print(f"   Shape y: {y.shape}")
        print(f"   Classes: {np.unique(y, return_counts=True)}")
        
        return X, y
    
    def prepare_data(self, X, y, test_size=0.2, val_size=0.2, balance_data=True):
        """Prepara dados para treinamento"""
        
        print("\n🔄 Preparando dados para treinamento...")
        
        # Balanceamento (opcional)
        if balance_data:
            X, y = create_balanced_dataset(X, y, balance_ratio=0.3)
        
        # Primeiro split: treino+val vs teste
        X_temp, X_test, y_temp, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        
        # Segundo split: treino vs validação
        val_size_adjusted = val_size / (1 - test_size)
        X_train, X_val, y_train, y_val = train_test_split(
            X_temp, y_temp, test_size=val_size_adjusted, random_state=42, stratify=y_temp
        )
        
        # Normalização das features
        # Reshape para 2D para o scaler
        n_samples, n_timesteps, n_features = X_train.shape
        X_train_2d = X_train.reshape(-1, n_features)
        X_val_2d = X_val.reshape(-1, n_features)
        X_test_2d = X_test.reshape(-1, n_features)
        
        # Fit scaler apenas no treino
        self.scaler.fit(X_train_2d)
        
        # Transform todos os conjuntos
        X_train_scaled = self.scaler.transform(X_train_2d).reshape(n_samples, n_timesteps, n_features)
        X_val_scaled = self.scaler.transform(X_val_2d).reshape(X_val.shape[0], n_timesteps, n_features)
        X_test_scaled = self.scaler.transform(X_test_2d).reshape(X_test.shape[0], n_timesteps, n_features)
        
        print(f"✅ Dados preparados:")
        print(f"   Treino: {X_train_scaled.shape} - {np.unique(y_train, return_counts=True)}")
        print(f"   Validação: {X_val_scaled.shape} - {np.unique(y_val, return_counts=True)}")
        print(f"   Teste: {X_test_scaled.shape} - {np.unique(y_test, return_counts=True)}")
        
        return (X_train_scaled, X_val_scaled, X_test_scaled, 
                y_train, y_val, y_test)
    
    def train_model(self, X_train, X_val, y_train, y_val, 
                   lstm_units=50, epochs=100, batch_size=32):
        """Treina o modelo LSTM"""
        
        print("\n🚀 INICIANDO TREINAMENTO DO MODELO")
        print("=" * 50)
        
        # Cria modelo
        self.model = FloodLSTMModel(
            sequence_length=X_train.shape[1],
            n_features=X_train.shape[2]
        )
        
        # Cria arquitetura
        self.model.create_model(lstm_units=lstm_units)
        self.model.get_model_summary()
        
        # Treinamento
        history = self.model.train_model(
            X_train, y_train, X_val, y_val,
            epochs=epochs, batch_size=batch_size
        )
        
        return history
    
    def evaluate_model(self, X_test, y_test):
        """Avalia modelo final"""
        
        print("\n📊 AVALIAÇÃO FINAL DO MODELO")
        print("=" * 50)
        
        results = self.model.evaluate_model(X_test, y_test)
        self.results = results
        
        return results
    
    def save_model_and_artifacts(self):
        """Salva modelo e artefatos"""
        
        print("\n💾 SALVANDO MODELO E ARTEFATOS")
        print("=" * 50)
        
        # Salva modelo
        model_path = os.path.join(self.output_dir, 'flood_lstm_model.h5')
        self.model.save_model(model_path)
        
        # Salva scaler
        scaler_path = os.path.join(self.output_dir, 'flood_scaler.pkl')
        joblib.dump(self.scaler, scaler_path)
        print(f"💾 Scaler salvo: {scaler_path}")
        
        # Salva resultados
        results_path = os.path.join(self.output_dir, 'training_results.json')
        results_to_save = {
            'timestamp': datetime.now().isoformat(),
            'model_architecture': {
                'type': 'LSTM',
                'sequence_length': self.model.sequence_length,
                'n_features': self.model.n_features,
                'lstm_units': 50,  # Default value
            },
            'performance': self.results,
            'files': {
                'model': model_path,
                'scaler': scaler_path,
                'results': results_path
            }
        }
        
        with open(results_path, 'w') as f:
            json.dump(results_to_save, f, indent=2)
        print(f"📊 Resultados salvos: {results_path}")
        
        # Salva gráficos
        plots_dir = os.path.join(self.output_dir, 'plots')
        os.makedirs(plots_dir, exist_ok=True)
        
        history_plot = os.path.join(plots_dir, 'training_history.png')
        self.model.plot_training_history(save_path=history_plot)
        
        print(f"✅ Artefatos salvos em: {self.output_dir}")
    
    def run_full_training(self, lstm_units=50, epochs=100, batch_size=32, balance_data=True):
        """Executa pipeline completo de treinamento"""
        
        print("🌧️  PIPELINE COMPLETO - TREINAMENTO MODELO ENCHENTES")
        print("=" * 60)
        print(f"⚙️  Configurações:")
        print(f"   LSTM Units: {lstm_units}")
        print(f"   Epochs: {epochs}")
        print(f"   Batch Size: {batch_size}")
        print(f"   Balance Data: {balance_data}")
        print("=" * 60)
        
        # 1. Carrega dados processados
        X, y = self.load_processed_data()
        if X is None:
            return False
        
        # 2. Prepara dados
        data_splits = self.prepare_data(X, y, balance_data=balance_data)
        X_train, X_val, X_test, y_train, y_val, y_test = data_splits
        
        # 3. Treina modelo
        history = self.train_model(X_train, X_val, y_train, y_val,
                                 lstm_units=lstm_units, epochs=epochs, batch_size=batch_size)
        
        # 4. Avalia modelo
        results = self.evaluate_model(X_test, y_test)
        
        # 5. Salva tudo
        self.save_model_and_artifacts()
        
        print(f"\n🎯 TREINAMENTO CONCLUÍDO COM SUCESSO!")
        print(f"   Accuracy: {results['accuracy']:.3f}")
        print(f"   Precision: {results['precision']:.3f}")
        print(f"   Recall: {results['recall']:.3f}")
        print(f"   F1-Score: {results['f1_score']:.3f}")
        
        return True

def main():
    """Função principal"""
    
    # Verifica se dados foram processados
    data_path = "../data/processed/flood_sequences.npz"
    if not os.path.exists(data_path):
        print("❌ Dados não processados ainda!")
        print("   Executando processamento primeiro...")
        
        # Processa dados automaticamente
        processor = InmetDataProcessor()
        df, X, y = processor.process_all_data()
        
        if df is not None:
            processor.save_processed_data(df, X, y)
            print("✅ Dados processados com sucesso!")
        else:
            print("❌ Falha no processamento dos dados!")
            return
    
    # Inicia treinamento
    trainer = FloodTrainer()
    
    # Configurações do treinamento
    config = {
        'lstm_units': 64,      # Aumentado para melhor capacidade
        'epochs': 50,          # Reduzido para teste mais rápido
        'batch_size': 32,
        'balance_data': True
    }
    
    success = trainer.run_full_training(**config)
    
    if success:
        print("\n🚀 Modelo pronto para produção!")
        print("   Próximo passo: Criar API FastAPI")
    else:
        print("\n❌ Falha no treinamento!")

if __name__ == "__main__":
    main()
