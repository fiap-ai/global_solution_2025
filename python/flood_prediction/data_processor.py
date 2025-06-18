#!/usr/bin/env python3
"""
INMET Data Processor - Flood Prediction
Processa dados meteorológicos de Teresópolis e Nova Friburgo para predição de enchentes.
"""

import pandas as pd
import numpy as np
import os
import glob
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class InmetDataProcessor:
    """Processador de dados INMET para predição de enchentes"""
    
    def __init__(self, base_path="../data/inmet/bd"):
        self.base_path = base_path
        self.stations = ['TERESOPOLIS', 'FRIBURGO']
        self.required_columns = [
            'Data;Hora UTC',
            'PRECIPITACAO TOTAL, HORARIO (mm)',
            'UMIDADE RELATIVA DO AR, HORARIA (%)',
            'TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)',
            'PRESSAO ATMOSFERICA AO NIVEL DA ESTACAO, HORARIA (mB)'
        ]
        
    def find_station_files(self, station_name):
        """Encontra todos os arquivos CSV de uma estação específica pelo nome"""
        pattern = f"{self.base_path}/**/*{station_name}*.CSV"
        print(f"   🔍 Buscando padrão: {pattern}")
        files = glob.glob(pattern, recursive=True)
        print(f"   📁 Arquivos encontrados com nome {station_name}: {len(files)}")
        
        for file in files:
            print(f"   📄 Encontrado: {os.path.basename(file)}")
                
        return sorted(files)
    
    def clean_numeric_column(self, series, column_name):
        """Limpa e converte coluna numérica"""
        # Substitui valores inválidos
        series = series.replace(['-9999', '-9999.0', '', ' ', 'nan', 'NaN'], np.nan)
        series = series.replace(',', '.', regex=True)  # Decimal brasileiro -> inglês
        
        try:
            series = pd.to_numeric(series, errors='coerce')
        except:
            print(f"Erro ao converter coluna {column_name}")
            
        return series
    
    def process_single_file(self, file_path):
        """Processa um único arquivo CSV do INMET"""
        try:
            print(f"Processando: {os.path.basename(file_path)}")
            
            # Lê CSV com encoding adequado
            df = pd.read_csv(file_path, sep=';', encoding='latin-1', skiprows=8)
            
            # DEBUG: Mostra apenas se necessário
            # print(f"   🔍 Colunas: {len(df.columns)} encontradas")
            
            # Busca flexível por colunas (parcial)
            col_mapping = {}
            date_col = None
            hour_col = None
            
            # Procura colunas de data e hora (podem estar separadas)
            for col in df.columns:
                col_lower = col.lower()
                if 'data' in col_lower and 'hora' in col_lower:
                    col_mapping['datetime'] = col
                    break
                elif col_lower == 'data' or col_lower == 'data (yyyy-mm-dd)':
                    date_col = col
                elif col_lower == 'hora utc' or col_lower == 'hora (utc)':
                    hour_col = col
            
            # Se data e hora estão separadas, combina
            if 'datetime' not in col_mapping and date_col and hour_col:
                col_mapping['date_col'] = date_col  
                col_mapping['hour_col'] = hour_col
                print(f"   📅 Data/Hora separadas: {date_col} + {hour_col}")
            
            # Procura coluna de precipitação
            for col in df.columns:
                if 'precipitacao' in col.lower() or 'precipitação' in col.lower():
                    col_mapping['precipitation'] = col
                    break
                    
            # Procura coluna de umidade - busca padrão específico
            for col in df.columns:
                if 'umidade relativa do ar, horaria' in col.lower():
                    col_mapping['humidity'] = col
                    break
                    
            # Procura coluna de temperatura - busca padrão específico
            for col in df.columns:
                if 'temperatura do ar - bulbo seco, horaria' in col.lower():
                    col_mapping['temperature'] = col
                    break
                    
            # Procura coluna de pressão - busca padrão específico
            for col in df.columns:
                if 'pressao atmosferica ao nivel da estacao, horaria' in col.lower():
                    col_mapping['pressure'] = col
                    break
            
            print(f"   ✅ Colunas mapeadas: {list(col_mapping.keys())}")
            
            if len(col_mapping) < 4:  # Pelo menos precipitation + 3 outras
                print(f"   ❌ Poucas colunas essenciais encontradas")
                return None
            
            # Cria dataframe limpo
            df_clean = pd.DataFrame()
            
            # Processa datetime primeiro
            if 'date_col' in col_mapping and 'hour_col' in col_mapping:
                # Combina data e hora
                df_clean['datetime'] = pd.to_datetime(
                    df[col_mapping['date_col']].astype(str) + ' ' + 
                    df[col_mapping['hour_col']].astype(str), 
                    errors='coerce'
                )
            elif 'datetime' in col_mapping:
                df_clean['datetime'] = pd.to_datetime(df[col_mapping['datetime']], errors='coerce')
            else:
                print(f"   ❌ Nenhuma coluna de datetime encontrada")
                return None
            
            # Copia outras colunas
            for field in ['precipitation', 'humidity', 'temperature', 'pressure']:
                if field in col_mapping:
                    df_clean[field] = df[col_mapping[field]].copy()
                else:
                    df_clean[field] = np.nan
                    print(f"   ⚠️  Campo {field} não encontrado, preenchido com NaN")
            
            # Limpa dados numéricos
            for col in ['precipitation', 'humidity', 'temperature', 'pressure']:
                df_clean[col] = self.clean_numeric_column(df_clean[col], col)
            
            # Remove linhas com datetime inválido e normaliza timezone
            df_clean = df_clean.dropna(subset=['datetime'])
            
            # Remove timezone para evitar conflitos
            if df_clean['datetime'].dt.tz is not None:
                df_clean['datetime'] = df_clean['datetime'].dt.tz_localize(None)
            
            # Adiciona metadados
            if 'TERESOPOLIS' in file_path.upper():
                df_clean['station'] = 'TERESOPOLIS'
                df_clean['station_code'] = 'A618'
            elif 'FRIBURGO' in file_path.upper():
                df_clean['station'] = 'NOVA_FRIBURGO'
                df_clean['station_code'] = 'A624'
            else:
                df_clean['station'] = 'UNKNOWN'
                df_clean['station_code'] = 'UNKNOWN'
            
            # Extrai ano do arquivo usando regex
            import re
            year_match = re.search(r'(\d{4})', os.path.basename(file_path))
            if year_match:
                year = int(year_match.group(1))
                # Verifica se é um ano válido (entre 2000-2030)
                if 2000 <= year <= 2030:
                    df_clean['year'] = year
                else:
                    df_clean['year'] = 2024  # Default
            else:
                df_clean['year'] = 2024  # Default
            
            print(f"  ✅ {len(df_clean)} registros processados")
            return df_clean
            
        except Exception as e:
            print(f"  ❌ Erro ao processar {file_path}: {str(e)}")
            return None
    
    def create_flood_labels(self, df):
        """Cria labels de risco de enchente baseado em condições meteorológicas"""
        
        # Condições para risco de enchente (baseado em literatura)
        conditions = []
        
        # Condição 1: Precipitação intensa (>20mm/h por 2h consecutivas)
        df['precip_2h'] = df['precipitation'].rolling(window=2, min_periods=2).sum()
        conditions.append(df['precip_2h'] >= 40)  # 20mm/h * 2h
        
        # Condição 2: Precipitação moderada + Umidade muito alta
        conditions.append((df['precipitation'] >= 10) & (df['humidity'] >= 90))
        
        # Condição 3: Precipitação acumulada 6h > 50mm
        df['precip_6h'] = df['precipitation'].rolling(window=6, min_periods=4).sum()
        conditions.append(df['precip_6h'] >= 50)
        
        # Condição 4: Precipitação + Queda de pressão (instabilidade)
        df['pressure_drop'] = df['pressure'].rolling(window=3).min() - df['pressure']
        conditions.append((df['precipitation'] >= 5) & (df['pressure_drop'] >= 3))
        
        # Combinação OR das condições
        flood_risk = np.zeros(len(df))
        for condition in conditions:
            flood_risk = flood_risk | condition.fillna(False)
        
        df['flood_risk'] = flood_risk.astype(int)
        
        # Estatísticas
        total_hours = len(df)
        flood_hours = flood_risk.sum()
        print(f"  📊 Risco de enchente: {flood_hours}/{total_hours} horas ({flood_hours/total_hours*100:.1f}%)")
        
        return df
    
    def create_sequences(self, df, sequence_length=24):
        """Cria sequências de 24h para entrada do LSTM"""
        
        features = ['precipitation', 'humidity', 'temperature', 'pressure']
        
        # Remove NaN
        df_clean = df.dropna(subset=features + ['flood_risk'])
        
        if len(df_clean) < sequence_length:
            print(f"  ⚠️  Dados insuficientes: {len(df_clean)} < {sequence_length}")
            return [], []
        
        X, y = [], []
        
        for i in range(len(df_clean) - sequence_length + 1):
            # Sequência de 24h de features
            sequence = df_clean[features].iloc[i:i+sequence_length].values
            
            # Verifica se não há NaN na sequência
            if not np.isnan(sequence).any():
                X.append(sequence)
                # Label é o risco da última hora da sequência
                y.append(df_clean['flood_risk'].iloc[i+sequence_length-1])
        
        print(f"  📈 {len(X)} sequências de {sequence_length}h criadas")
        return np.array(X), np.array(y)
    
    def process_all_data(self, limit_years=5):
        """Processa dados das duas estações com limite de memória"""
        
        print("🌧️  PROCESSANDO DADOS INMET - PREDIÇÃO DE ENCHENTES")
        print("=" * 60)
        
        all_data = []
        all_sequences_X = []
        all_sequences_y = []
        
        for station_name in self.stations:
            print(f"\n📍 Estação: {station_name}")
            
            # Encontra arquivos da estação pelo nome
            files = self.find_station_files(station_name)
            print(f"   Arquivos encontrados: {len(files)}")
            
            if not files:
                print(f"   ⚠️  Nenhum arquivo encontrado para {station_name}")
                continue
            
            # Limita anos para evitar problemas de memória
            files = files[-limit_years:] if len(files) > limit_years else files
            print(f"   🔄 Processando últimos {len(files)} anos para economia de memória")
            
            station_data = []
            
            # Processa cada arquivo
            for file_path in files:
                df = self.process_single_file(file_path)
                if df is not None:
                    station_data.append(df)
            
            if station_data:
                # Combina todos os anos da estação
                station_df = pd.concat(station_data, ignore_index=True)
                del station_data  # Libera memória
                
                station_df = station_df.sort_values('datetime')
                
                # Cria labels de enchente
                station_df = self.create_flood_labels(station_df)
                
                # Cria sequências
                X, y = self.create_sequences(station_df)
                
                if len(X) > 0:
                    all_sequences_X.append(X)
                    all_sequences_y.append(y)
                    
                    # Mantém apenas sample dos dados para estatísticas
                    station_sample = station_df.sample(min(1000, len(station_df))).copy()
                    all_data.append(station_sample)
                    del station_df  # Libera memória
                    
                    print(f"   ✅ {len(X)} sequências processadas")
                    print(f"   📊 Período: {station_sample['datetime'].min()} a {station_sample['datetime'].max()}")
        
        # Combina dados de todas as estações
        if all_data:
            combined_df = pd.concat(all_data, ignore_index=True)
            combined_X = np.vstack(all_sequences_X)
            combined_y = np.hstack(all_sequences_y)
            
            print(f"\n🎯 RESULTADO FINAL:")
            print(f"   Total de registros: {len(combined_df)}")
            print(f"   Total de sequências: {len(combined_X)}")
            print(f"   Risco positivo: {combined_y.sum()}/{len(combined_y)} ({combined_y.sum()/len(combined_y)*100:.1f}%)")
            
            return combined_df, combined_X, combined_y
        
        else:
            print("\n❌ Nenhum dado processado com sucesso!")
            return None, None, None
    
    def save_processed_data(self, df, X, y, output_dir="../data/processed"):
        """Salva dados processados"""
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Salva dataframe completo
        df_path = os.path.join(output_dir, 'inmet_rj_processed.csv')
        df.to_csv(df_path, index=False)
        print(f"💾 DataFrame salvo: {df_path}")
        
        # Salva sequências para ML
        sequences_path = os.path.join(output_dir, 'flood_sequences')
        np.savez(sequences_path, X=X, y=y)
        print(f"💾 Sequências salvas: {sequences_path}.npz")
        
        # Salva estatísticas
        stats = {
            'total_records': len(df),
            'total_sequences': len(X),
            'flood_percentage': float(y.sum() / len(y) * 100),
            'stations': df['station'].unique().tolist(),
            'date_range': [str(df['datetime'].min()), str(df['datetime'].max())],
            'features': ['precipitation', 'humidity', 'temperature', 'pressure']
        }
        
        import json
        stats_path = os.path.join(output_dir, 'inmet_stats.json')
        with open(stats_path, 'w') as f:
            json.dump(stats, f, indent=2)
        print(f"📊 Estatísticas salvas: {stats_path}")

def main():
    """Função principal"""
    processor = InmetDataProcessor()
    
    # Processa todos os dados
    df, X, y = processor.process_all_data()
    
    if df is not None:
        # Salva dados processados
        processor.save_processed_data(df, X, y)
        print(f"\n✅ Processamento concluído com sucesso!")
    else:
        print(f"\n❌ Falha no processamento!")

if __name__ == "__main__":
    main()
