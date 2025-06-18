#!/usr/bin/env python3
"""
LSTM Model - Flood Prediction
Arquitetura de rede neural para predição de enchentes baseada em séries temporais.
"""

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

class FloodLSTMModel:
    """Modelo LSTM para predição de enchentes"""
    
    def __init__(self, sequence_length=24, n_features=4):
        self.sequence_length = sequence_length
        self.n_features = n_features
        self.model = None
        self.history = None
        
    def create_model(self, lstm_units=50, dropout_rate=0.2, learning_rate=0.001):
        """Cria arquitetura LSTM"""
        
        model = Sequential([
            # Primeira camada LSTM
            LSTM(lstm_units, 
                 return_sequences=True, 
                 input_shape=(self.sequence_length, self.n_features),
                 name='lstm_1'),
            BatchNormalization(),
            Dropout(dropout_rate),
            
            # Segunda camada LSTM
            LSTM(lstm_units, 
                 return_sequences=False,
                 name='lstm_2'),
            BatchNormalization(),
            Dropout(dropout_rate),
            
            # Camadas densas
            Dense(25, activation='relu', name='dense_1'),
            Dropout(dropout_rate),
            
            # Saída - probabilidade de enchente
            Dense(1, activation='sigmoid', name='output')
        ])
        
        # Compilação
        optimizer = Adam(learning_rate=learning_rate)
        model.compile(
            optimizer=optimizer,
            loss='binary_crossentropy',
            metrics=['accuracy', 'precision', 'recall']
        )
        
        self.model = model
        return model
    
    def get_callbacks(self, patience=10):
        """Configura callbacks de treinamento"""
        
        callbacks = [
            EarlyStopping(
                monitor='val_loss',
                patience=patience,
                restore_best_weights=True,
                verbose=1
            ),
            ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=5,
                min_lr=0.0001,
                verbose=1
            )
        ]
        
        return callbacks
    
    def train_model(self, X_train, y_train, X_val, y_val, 
                   epochs=100, batch_size=32, verbose=1):
        """Treina o modelo"""
        
        if self.model is None:
            self.create_model()
            
        print("🚀 Iniciando treinamento do modelo LSTM...")
        print(f"   Dados treino: {X_train.shape}")
        print(f"   Dados validação: {X_val.shape}")
        print(f"   Épocas: {epochs}, Batch size: {batch_size}")
        
        # Callbacks
        callbacks = self.get_callbacks()
        
        # Treinamento
        self.history = self.model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=epochs,
            batch_size=batch_size,
            callbacks=callbacks,
            verbose=verbose
        )
        
        print("✅ Treinamento concluído!")
        return self.history
    
    def evaluate_model(self, X_test, y_test):
        """Avalia performance do modelo"""
        
        if self.model is None:
            print("❌ Modelo não foi treinado ainda!")
            return None
            
        print("📊 Avaliando modelo...")
        
        # Predições
        y_pred_prob = self.model.predict(X_test)
        y_pred = (y_pred_prob > 0.5).astype(int).flatten()
        
        # Métricas básicas
        loss, accuracy, precision, recall = self.model.evaluate(X_test, y_test, verbose=0)
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        print(f"   Loss: {loss:.4f}")
        print(f"   Accuracy: {accuracy:.4f}")
        print(f"   Precision: {precision:.4f}")
        print(f"   Recall: {recall:.4f}")
        print(f"   F1-Score: {f1_score:.4f}")
        
        # Relatório detalhado
        print("\n📋 Classification Report:")
        print(classification_report(y_test, y_pred, 
                                   target_names=['Normal', 'Flood Risk']))
        
        # Matriz de confusão
        cm = confusion_matrix(y_test, y_pred)
        print(f"\n🔍 Confusion Matrix:")
        print(f"   TN: {cm[0,0]}, FP: {cm[0,1]}")
        print(f"   FN: {cm[1,0]}, TP: {cm[1,1]}")
        
        results = {
            'loss': loss,
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1_score,
            'confusion_matrix': cm.tolist(),
            'predictions': y_pred.tolist(),
            'probabilities': y_pred_prob.flatten().tolist()
        }
        
        return results
    
    def predict(self, X):
        """Faz predições"""
        if self.model is None:
            print("❌ Modelo não foi treinado ainda!")
            return None
            
        probabilities = self.model.predict(X)
        predictions = (probabilities > 0.5).astype(int)
        
        return predictions.flatten(), probabilities.flatten()
    
    def plot_training_history(self, save_path=None):
        """Plota histórico de treinamento"""
        
        if self.history is None:
            print("❌ Modelo não foi treinado ainda!")
            return
            
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Loss
        axes[0,0].plot(self.history.history['loss'], label='Train Loss')
        axes[0,0].plot(self.history.history['val_loss'], label='Val Loss')
        axes[0,0].set_title('Model Loss')
        axes[0,0].set_xlabel('Epoch')
        axes[0,0].set_ylabel('Loss')
        axes[0,0].legend()
        axes[0,0].grid(True)
        
        # Accuracy
        axes[0,1].plot(self.history.history['accuracy'], label='Train Acc')
        axes[0,1].plot(self.history.history['val_accuracy'], label='Val Acc')
        axes[0,1].set_title('Model Accuracy')
        axes[0,1].set_xlabel('Epoch')
        axes[0,1].set_ylabel('Accuracy')
        axes[0,1].legend()
        axes[0,1].grid(True)
        
        # Precision
        axes[1,0].plot(self.history.history['precision'], label='Train Precision')
        axes[1,0].plot(self.history.history['val_precision'], label='Val Precision')
        axes[1,0].set_title('Model Precision')
        axes[1,0].set_xlabel('Epoch')
        axes[1,0].set_ylabel('Precision')
        axes[1,0].legend()
        axes[1,0].grid(True)
        
        # Recall
        axes[1,1].plot(self.history.history['recall'], label='Train Recall')
        axes[1,1].plot(self.history.history['val_recall'], label='Val Recall')
        axes[1,1].set_title('Model Recall')
        axes[1,1].set_xlabel('Epoch')
        axes[1,1].set_ylabel('Recall')
        axes[1,1].legend()
        axes[1,1].grid(True)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"📊 Gráfico salvo: {save_path}")
        
        plt.show()
    
    def plot_confusion_matrix(self, y_true, y_pred, save_path=None):
        """Plota matriz de confusão"""
        
        cm = confusion_matrix(y_true, y_pred)
        
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                   xticklabels=['Normal', 'Flood Risk'],
                   yticklabels=['Normal', 'Flood Risk'])
        plt.title('Confusion Matrix - Flood Prediction')
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"📊 Matriz de confusão salva: {save_path}")
        
        plt.show()
    
    def save_model(self, model_path):
        """Salva modelo treinado"""
        if self.model is None:
            print("❌ Modelo não foi treinado ainda!")
            return
            
        self.model.save(model_path)
        print(f"💾 Modelo salvo: {model_path}")
    
    def load_model(self, model_path):
        """Carrega modelo salvo"""
        self.model = tf.keras.models.load_model(model_path)
        print(f"📂 Modelo carregado: {model_path}")
        return self.model
    
    def get_model_summary(self):
        """Mostra resumo do modelo"""
        if self.model is None:
            print("❌ Modelo não foi criado ainda!")
            return
            
        print("🏗️  ARQUITETURA DO MODELO:")
        print("=" * 50)
        self.model.summary()
        
        # Conta parâmetros
        total_params = self.model.count_params()
        print(f"\n📊 Total de parâmetros: {total_params:,}")

def create_balanced_dataset(X, y, balance_ratio=0.5):
    """Balanceia dataset para melhor treinamento"""
    
    # Conta classes
    unique, counts = np.unique(y, return_counts=True)
    class_counts = dict(zip(unique, counts))
    
    print(f"📊 Classes originais: {class_counts}")
    
    # Se já está balanceado, retorna original
    minority_class = min(class_counts.values())
    majority_class = max(class_counts.values())
    
    if minority_class / majority_class >= balance_ratio:
        print("✅ Dataset já está balanceado")
        return X, y
    
    # Balanceamento por undersampling da classe majoritária
    normal_indices = np.where(y == 0)[0]
    flood_indices = np.where(y == 1)[0]
    
    # Calcula quantos exemplos manter da classe majoritária
    n_flood = len(flood_indices)
    n_normal_target = int(n_flood / balance_ratio)
    
    if n_normal_target < len(normal_indices):
        # Undersampling da classe normal
        normal_selected = np.random.choice(normal_indices, n_normal_target, replace=False)
        selected_indices = np.concatenate([normal_selected, flood_indices])
    else:
        selected_indices = np.concatenate([normal_indices, flood_indices])
    
    # Embaralha índices
    np.random.shuffle(selected_indices)
    
    X_balanced = X[selected_indices]
    y_balanced = y[selected_indices]
    
    # Estatísticas finais
    unique_bal, counts_bal = np.unique(y_balanced, return_counts=True)
    class_counts_bal = dict(zip(unique_bal, counts_bal))
    
    print(f"✅ Classes balanceadas: {class_counts_bal}")
    print(f"   Redução: {len(y)} → {len(y_balanced)} exemplos")
    
    return X_balanced, y_balanced
