(venv) MacBook-Pro-de-Gabriel-Mule:python gabmule$ python flood_prediction/train.py
🌧️  PIPELINE COMPLETO - TREINAMENTO MODELO ENCHENTES
============================================================
⚙️  Configurações:
   LSTM Units: 64
   Epochs: 50
   Batch Size: 32
   Balance Data: True
============================================================
📂 Carregando dados: ../data/processed/flood_sequences.npz
✅ Dados carregados:
   Shape X: (72651, 24, 4)
   Shape y: (72651,)
   Classes: (array([0, 1]), array([72244,   407]))

🔄 Preparando dados para treinamento...
📊 Classes originais: {np.int64(0): np.int64(72244), np.int64(1): np.int64(407)}
✅ Classes balanceadas: {np.int64(0): np.int64(1356), np.int64(1): np.int64(407)}
   Redução: 72651 → 1763 exemplos
✅ Dados preparados:
   Treino: (1057, 24, 4) - (array([0, 1]), array([813, 244]))
   Validação: (353, 24, 4) - (array([0, 1]), array([271,  82]))
   Teste: (353, 24, 4) - (array([0, 1]), array([272,  81]))

🚀 INICIANDO TREINAMENTO DO MODELO
==================================================
🏗️  ARQUITETURA DO MODELO:
==================================================
Model: "sequential"
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓
┃ Layer (type)                         ┃ Output Shape                ┃         Param # ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩
│ lstm_1 (LSTM)                        │ (None, 24, 64)              │          17,664 │
├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤
│ batch_normalization                  │ (None, 24, 64)              │             256 │
│ (BatchNormalization)                 │                             │                 │
├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤
│ dropout (Dropout)                    │ (None, 24, 64)              │               0 │
├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤
│ lstm_2 (LSTM)                        │ (None, 64)                  │          33,024 │
├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤
│ batch_normalization_1                │ (None, 64)                  │             256 │
│ (BatchNormalization)                 │                             │                 │
├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤
│ dropout_1 (Dropout)                  │ (None, 64)                  │               0 │
├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤
│ dense_1 (Dense)                      │ (None, 25)                  │           1,625 │
├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤
│ dropout_2 (Dropout)                  │ (None, 25)                  │               0 │
├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤
│ output (Dense)                       │ (None, 1)                   │              26 │
└──────────────────────────────────────┴─────────────────────────────┴─────────────────┘
 Total params: 52,851 (206.45 KB)
 Trainable params: 52,595 (205.45 KB)
 Non-trainable params: 256 (1.00 KB)

📊 Total de parâmetros: 52,851
🚀 Iniciando treinamento do modelo LSTM...
   Dados treino: (1057, 24, 4)
   Dados validação: (353, 24, 4)
   Épocas: 50, Batch size: 32
Epoch 1/50
34/34 ━━━━━━━━━━━━━━━━━━━━ 2s 13ms/step - accuracy: 0.7698 - loss: 0.4850 - precision: 0.5347 - recall: 0.4887 - val_accuracy: 0.7705 - val_loss: 0.6576 - val_precision: 1.0000 - val_recall: 0.0122 - learning_rate: 0.0010
Epoch 2/50
34/34 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - accuracy: 0.9120 - loss: 0.2655 - precision: 0.8710 - recall: 0.7205 - val_accuracy: 0.7734 - val_loss: 0.6256 - val_precision: 1.0000 - val_recall: 0.0244 - learning_rate: 0.0010
Epoch 3/50
34/34 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - accuracy: 0.9433 - loss: 0.1724 - precision: 0.9389 - recall: 0.8184 - val_accuracy: 0.7677 - val_loss: 0.5583 - val_precision: 0.0000e+00 - val_recall: 0.0000e+00 - learning_rate: 0.0010
Epoch 4/50
34/34 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - accuracy: 0.9568 - loss: 0.1284 - precision: 0.9223 - recall: 0.8866 - val_accuracy: 0.7677 - val_loss: 0.5077 - val_precision: 0.0000e+00 - val_recall: 0.0000e+00 - learning_rate: 0.0010
Epoch 5/50
34/34 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - accuracy: 0.9656 - loss: 0.1051 - precision: 0.9277 - recall: 0.9230 - val_accuracy: 0.7677 - val_loss: 0.4817 - val_precision: 0.0000e+00 - val_recall: 0.0000e+00 - learning_rate: 0.0010
Epoch 6/50
34/34 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - accuracy: 0.9670 - loss: 0.0870 - precision: 0.9408 - recall: 0.9114 - val_accuracy: 0.7734 - val_loss: 0.4545 - val_precision: 1.0000 - val_recall: 0.0244 - learning_rate: 0.0010
Epoch 7/50
34/34 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - accuracy: 0.9758 - loss: 0.0692 - precision: 0.9486 - recall: 0.9496 - val_accuracy: 0.7734 - val_loss: 0.4269 - val_precision: 1.0000 - val_recall: 0.0244 - learning_rate: 0.0010
Epoch 8/50
34/34 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - accuracy: 0.9739 - loss: 0.0676 - precision: 0.9202 - recall: 0.9615 - val_accuracy: 0.8697 - val_loss: 0.3290 - val_precision: 1.0000 - val_recall: 0.4390 - learning_rate: 0.0010
Epoch 9/50
34/34 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - accuracy: 0.9796 - loss: 0.0641 - precision: 0.9577 - recall: 0.9666 - val_accuracy: 0.8102 - val_loss: 0.3583 - val_precision: 1.0000 - val_recall: 0.1829 - learning_rate: 0.0010
Epoch 10/50
34/34 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - accuracy: 0.9866 - loss: 0.0441 - precision: 0.9597 - recall: 0.9844 - val_accuracy: 0.8782 - val_loss: 0.2603 - val_precision: 1.0000 - val_recall: 0.4756 - learning_rate: 0.0010
Epoch 11/50
34/34 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - accuracy: 0.9841 - loss: 0.0433 - precision: 0.9534 - recall: 0.9759 - val_accuracy: 0.9122 - val_loss: 0.1855 - val_precision: 0.9811 - val_recall: 0.6341 - learning_rate: 0.0010
Epoch 12/50
34/34 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - accuracy: 0.9910 - loss: 0.0344 - precision: 0.9684 - recall: 0.9936 - val_accuracy: 0.9093 - val_loss: 0.1886 - val_precision: 1.0000 - val_recall: 0.6098 - learning_rate: 0.0010
Epoch 13/50
34/34 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - accuracy: 0.9875 - loss: 0.0375 - precision: 0.9626 - recall: 0.9784 - val_accuracy: 0.9263 - val_loss: 0.1571 - val_precision: 1.0000 - val_recall: 0.6829 - learning_rate: 0.0010
Epoch 14/50
34/34 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - accuracy: 0.9804 - loss: 0.0397 - precision: 0.9481 - recall: 0.9707 - val_accuracy: 0.9207 - val_loss: 0.1828 - val_precision: 0.9821 - val_recall: 0.6707 - learning_rate: 0.0010
Epoch 15/50
34/34 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - accuracy: 0.9936 - loss: 0.0255 - precision: 0.9794 - recall: 0.9934 - val_accuracy: 0.9122 - val_loss: 0.2574 - val_precision: 1.0000 - val_recall: 0.6220 - learning_rate: 0.0010
Epoch 16/50
34/34 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - accuracy: 0.9929 - loss: 0.0274 - precision: 0.9899 - recall: 0.9822 - val_accuracy: 0.9603 - val_loss: 0.0763 - val_precision: 0.9722 - val_recall: 0.8537 - learning_rate: 0.0010
Epoch 17/50
34/34 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - accuracy: 0.9954 - loss: 0.0290 - precision: 0.9825 - recall: 0.9977 - val_accuracy: 0.9433 - val_loss: 0.1368 - val_precision: 1.0000 - val_recall: 0.7561 - learning_rate: 0.0010
Epoch 18/50
34/34 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - accuracy: 0.9945 - loss: 0.0297 - precision: 0.9877 - recall: 0.9897 - val_accuracy: 0.9830 - val_loss: 0.0497 - val_precision: 0.9318 - val_recall: 1.0000 - learning_rate: 0.0010
Epoch 19/50
34/34 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - accuracy: 0.9908 - loss: 0.0273 - precision: 0.9732 - recall: 0.9870 - val_accuracy: 0.9858 - val_loss: 0.0426 - val_precision: 0.9529 - val_recall: 0.9878 - learning_rate: 0.0010
Epoch 20/50
34/34 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - accuracy: 0.9871 - loss: 0.0378 - precision: 0.9824 - recall: 0.9657 - val_accuracy: 0.9773 - val_loss: 0.0602 - val_precision: 0.9111 - val_recall: 1.0000 - learning_rate: 0.0010
Epoch 21/50
34/34 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - accuracy: 0.9789 - loss: 0.0554 - precision: 0.9081 - recall: 0.9892 - val_accuracy: 0.9858 - val_loss: 0.0359 - val_precision: 0.9425 - val_recall: 1.0000 - learning_rate: 0.0010
Epoch 22/50
34/34 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - accuracy: 0.9925 - loss: 0.0222 - precision: 0.9788 - recall: 0.9927 - val_accuracy: 0.9887 - val_loss: 0.0252 - val_precision: 0.9756 - val_recall: 0.9756 - learning_rate: 0.0010
Epoch 23/50
34/34 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - accuracy: 0.9938 - loss: 0.0262 - precision: 0.9735 - recall: 0.9998 - val_accuracy: 0.9830 - val_loss: 0.0478 - val_precision: 1.0000 - val_recall: 0.9268 - learning_rate: 0.0010
Epoch 24/50
34/34 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - accuracy: 0.9862 - loss: 0.0313 - precision: 0.9759 - recall: 0.9649 - val_accuracy: 0.9858 - val_loss: 0.0202 - val_precision: 0.9529 - val_recall: 0.9878 - learning_rate: 0.0010
Epoch 25/50
34/34 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - accuracy: 0.9939 - loss: 0.0209 - precision: 0.9756 - recall: 1.0000 - val_accuracy: 0.9858 - val_loss: 0.0263 - val_precision: 0.9753 - val_recall: 0.9634 - learning_rate: 0.0010
Epoch 26/50
34/34 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - accuracy: 0.9964 - loss: 0.0151 - precision: 0.9913 - recall: 0.9930 - val_accuracy: 0.9943 - val_loss: 0.0188 - val_precision: 0.9762 - val_recall: 1.0000 - learning_rate: 0.0010
Epoch 27/50
34/34 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - accuracy: 0.9916 - loss: 0.0160 - precision: 0.9692 - recall: 0.9965 - val_accuracy: 0.9830 - val_loss: 0.0649 - val_precision: 0.9318 - val_recall: 1.0000 - learning_rate: 0.0010
Epoch 28/50
34/34 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - accuracy: 0.9964 - loss: 0.0126 - precision: 0.9859 - recall: 0.9990 - val_accuracy: 0.9858 - val_loss: 0.0247 - val_precision: 0.9753 - val_recall: 0.9634 - learning_rate: 0.0010
Epoch 29/50
34/34 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - accuracy: 0.9927 - loss: 0.0213 - precision: 0.9725 - recall: 0.9995 - val_accuracy: 0.9887 - val_loss: 0.0351 - val_precision: 0.9535 - val_recall: 1.0000 - learning_rate: 0.0010
Epoch 30/50
34/34 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - accuracy: 0.9913 - loss: 0.0168 - precision: 0.9693 - recall: 0.9955 - val_accuracy: 0.9915 - val_loss: 0.0310 - val_precision: 0.9647 - val_recall: 1.0000 - learning_rate: 0.0010
Epoch 31/50
29/34 ━━━━━━━━━━━━━━━━━━━━ 0s 6ms/step - accuracy: 0.9988 - loss: 0.0085 - precision: 0.9991 - recall: 0.9956 
Epoch 31: ReduceLROnPlateau reducing learning rate to 0.0005000000237487257.
34/34 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - accuracy: 0.9983 - loss: 0.0090 - precision: 0.9978 - recall: 0.9949 - val_accuracy: 0.9887 - val_loss: 0.0483 - val_precision: 0.9643 - val_recall: 0.9878 - learning_rate: 0.0010
Epoch 32/50
34/34 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - accuracy: 0.9961 - loss: 0.0107 - precision: 0.9927 - recall: 0.9900 - val_accuracy: 0.9858 - val_loss: 0.0358 - val_precision: 0.9639 - val_recall: 0.9756 - learning_rate: 5.0000e-04
Epoch 33/50
34/34 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - accuracy: 0.9953 - loss: 0.0160 - precision: 0.9829 - recall: 0.9968 - val_accuracy: 0.9887 - val_loss: 0.0463 - val_precision: 0.9535 - val_recall: 1.0000 - learning_rate: 5.0000e-04
Epoch 34/50
34/34 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - accuracy: 0.9946 - loss: 0.0122 - precision: 0.9863 - recall: 0.9908 - val_accuracy: 0.9887 - val_loss: 0.0589 - val_precision: 0.9535 - val_recall: 1.0000 - learning_rate: 5.0000e-04
Epoch 35/50
34/34 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - accuracy: 0.9947 - loss: 0.0107 - precision: 0.9911 - recall: 0.9865 - val_accuracy: 0.9830 - val_loss: 0.0732 - val_precision: 0.9419 - val_recall: 0.9878 - learning_rate: 5.0000e-04
Epoch 36/50
29/34 ━━━━━━━━━━━━━━━━━━━━ 0s 6ms/step - accuracy: 0.9967 - loss: 0.0122 - precision: 0.9924 - recall: 0.9933 
Epoch 36: ReduceLROnPlateau reducing learning rate to 0.0002500000118743628.
34/34 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - accuracy: 0.9966 - loss: 0.0125 - precision: 0.9922 - recall: 0.9930 - val_accuracy: 0.9887 - val_loss: 0.0426 - val_precision: 0.9643 - val_recall: 0.9878 - learning_rate: 5.0000e-04
Epoch 36: early stopping
Restoring model weights from the end of the best epoch: 26.
✅ Treinamento concluído!

📊 AVALIAÇÃO FINAL DO MODELO
==================================================
📊 Avaliando modelo...
12/12 ━━━━━━━━━━━━━━━━━━━━ 0s 11ms/step
   Loss: 0.0283
   Accuracy: 0.9915
   Precision: 1.0000
   Recall: 0.9630
   F1-Score: 0.9811

📋 Classification Report:
              precision    recall  f1-score   support

      Normal       0.99      1.00      0.99       272
  Flood Risk       1.00      0.96      0.98        81

    accuracy                           0.99       353
   macro avg       0.99      0.98      0.99       353
weighted avg       0.99      0.99      0.99       353


🔍 Confusion Matrix:
   TN: 272, FP: 0
   FN: 3, TP: 78

💾 SALVANDO MODELO E ARTEFATOS
==================================================
WARNING:absl:You are saving your model as an HDF5 file via `model.save()` or `keras.saving.save_model(model)`. This file format is considered legacy. We recommend using instead the native Keras format, e.g. `model.save('my_model.keras')` or `keras.saving.save_model(model, 'my_model.keras')`. 
💾 Modelo salvo: ../data/models/flood_lstm_model.h5
💾 Scaler salvo: ../data/models/flood_scaler.pkl
📊 Resultados salvos: ../data/models/training_results.json
📊 Gráfico salvo: ../data/models/plots/training_history.png
✅ Artefatos salvos em: ../data/models

🎯 TREINAMENTO CONCLUÍDO COM SUCESSO!
   Accuracy: 0.992
   Precision: 1.000
   Recall: 0.963
   F1-Score: 0.981

🚀 Modelo pronto para produção!
(venv) MacBook-Pro-de-Gabriel-Mule:python gabmule$ 