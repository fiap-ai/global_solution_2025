"""
DisastersCharter.org Data Scraper
Coleta dados estruturados de enchentes usando a API interna do site
"""

import requests
import json
import time
import re
from datetime import datetime
from typing import List, Dict, Optional
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DisastersCharterScraper:
    def __init__(self):
        self.base_url = "https://disasterscharter.org"
        self.session = requests.Session()
        
        # Headers baseados no curl fornecido
        self.headers = {
            'accept': '*/*',
            'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,it;q=0.6',
            'dnt': '1',
            'referer': 'https://disasterscharter.org/activations',
            'rsc': '1',
            'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36'
        }
        
        self.session.headers.update(self.headers)
        
        # Parâmetros de configuração
        self.delay_between_requests = 2
        self.max_retries = 3
        
    def extract_activations_from_response(self, response_text: str) -> List[Dict]:
        """
        Extrai dados de ativações da resposta da API interna
        """
        try:
            # A resposta contém dados estruturados em formato específico
            # Procurar pelo padrão de dados JSON nas linhas
            activations = []
            
            # Buscar pela linha que contém os dados de ativações
            lines = response_text.split('\n')
            for line in lines:
                if '"activations":[' in line:
                    # Extrair o JSON da linha
                    start_idx = line.find('"activations":[')
                    if start_idx != -1:
                        # Encontrar o final do array de ativações
                        bracket_count = 0
                        json_start = line.find('[', start_idx)
                        json_end = json_start
                        
                        for i, char in enumerate(line[json_start:], json_start):
                            if char == '[':
                                bracket_count += 1
                            elif char == ']':
                                bracket_count -= 1
                                if bracket_count == 0:
                                    json_end = i + 1
                                    break
                        
                        if json_end > json_start:
                            json_str = line[json_start:json_end]
                            try:
                                activations = json.loads(json_str)
                                logger.info(f"Extraídas {len(activations)} ativações")
                                return activations
                            except json.JSONDecodeError as e:
                                logger.error(f"Erro ao decodificar JSON: {e}")
                                
            return activations
            
        except Exception as e:
            logger.error(f"Erro ao extrair ativações: {e}")
            return []
    
    def get_flood_activations(self, location: str = "", limit_years: int = 5) -> List[Dict]:
        """
        Busca ativações de enchentes globalmente
        """
        all_activations = []
        
        # Buscar globalmente primeiro (sem filtro de região)
        search_configs = [
            {"name": "Global (sem filtro)", "params": {'disaster': 'flood', '_rsc': 'ryiee'}},
            {"name": "South America", "params": {'disaster': 'flood', 'location': 'south america', '_rsc': 'ryiee'}},
            {"name": "Africa", "params": {'disaster': 'flood', 'location': 'africa', '_rsc': 'ryiee'}},
            {"name": "Asia", "params": {'disaster': 'flood', 'location': 'asia', '_rsc': 'ryiee'}},
            {"name": "Europe", "params": {'disaster': 'flood', 'location': 'europe', '_rsc': 'ryiee'}},
            {"name": "North America", "params": {'disaster': 'flood', 'location': 'north america', '_rsc': 'ryiee'}},
            {"name": "Oceania", "params": {'disaster': 'flood', 'location': 'oceania', '_rsc': 'ryiee'}},
            {"name": "Caribbean", "params": {'disaster': 'flood', 'location': 'caribbean', '_rsc': 'ryiee'}},
            {"name": "Central America", "params": {'disaster': 'flood', 'location': 'central america', '_rsc': 'ryiee'}},
            {"name": "Middle East", "params": {'disaster': 'flood', 'location': 'middle east', '_rsc': 'ryiee'}}
        ]
        
        # Se location específica for fornecida, usar apenas ela
        if location:
            search_configs = [{"name": f"Específico: {location}", "params": {'disaster': 'flood', 'location': location, '_rsc': 'ryiee'}}]
        
        for config in search_configs:
            logger.info(f"Buscando enchentes em: {config['name']}")
            
            # URL baseada no curl fornecido
            url = f"{self.base_url}/activations"
            params = config['params']
            
            try:
                response = self.session.get(url, params=params, timeout=30)
                response.raise_for_status()
                
                # Extrair ativações da resposta
                activations = self.extract_activations_from_response(response.text)
                
                # Processar e limpar dados
                for activation in activations:
                    processed = self.process_activation(activation, config['name'])
                    if processed:
                        all_activations.append(processed)
                
                logger.info(f"Coletadas {len(activations)} ativações de {config['name']}")
                
                # Delay entre requests
                time.sleep(self.delay_between_requests)
                
            except requests.RequestException as e:
                logger.error(f"Erro ao buscar dados de {config['name']}: {e}")
                continue
        
        # Remover duplicatas baseado no activationId
        unique_activations = {}
        for activation in all_activations:
            activation_id = activation.get('activation_id')
            if activation_id and activation_id not in unique_activations:
                unique_activations[activation_id] = activation
        
        result = list(unique_activations.values())
        logger.info(f"Total de ativações únicas coletadas: {len(result)}")
        
        return result
    
    def process_activation(self, raw_activation: Dict, region: str) -> Optional[Dict]:
        """
        Processa e estrutura dados de uma ativação
        """
        try:
            # Converter timestamp para data legível
            timestamp = raw_activation.get('dateAsTimestamp', 0)
            date = datetime.fromtimestamp(timestamp / 1000) if timestamp else None
            
            processed = {
                'activation_id': raw_activation.get('activationId'),
                'title': raw_activation.get('title', ''),
                'date': date.isoformat() if date else None,
                'timestamp': timestamp,
                'location': {
                    'country': raw_activation.get('country', ''),
                    'region': region,
                    'latitude': float(raw_activation.get('centerPointLatitude', 0)),
                    'longitude': float(raw_activation.get('centerPointLongitude', 0))
                },
                'metadata': {
                    'slug': raw_activation.get('slug', ''),
                    'article_id': raw_activation.get('articleId', ''),
                    'external_reference': raw_activation.get('externalReferenceCode', ''),
                    'keywords': raw_activation.get('keywords', ''),
                    'disaster_types': raw_activation.get('disasterTypes', [])
                },
                'data_source': 'disasterscharter.org',
                'collected_at': datetime.now().isoformat()
            }
            
            # Extrair informações adicionais do título se possível
            title = processed['title'].lower()
            if 'flood' in title:
                processed['disaster_type'] = 'flood'
                processed['severity'] = self.estimate_severity_from_title(title)
            
            return processed
            
        except Exception as e:
            logger.error(f"Erro ao processar ativação: {e}")
            return None
    
    def estimate_severity_from_title(self, title: str) -> str:
        """
        Estima severidade baseada no título
        """
        title_lower = title.lower()
        
        if any(word in title_lower for word in ['devastating', 'major', 'severe', 'catastrophic']):
            return 'high'
        elif any(word in title_lower for word in ['flooding', 'flood']):
            return 'medium'
        else:
            return 'low'
    
    def get_activation_details(self, slug: str, article_id: str) -> Optional[Dict]:
        """
        Busca detalhes específicos de uma ativação incluindo duração
        """
        try:
            # URL da página individual do evento
            detail_url = f"{self.base_url}/activations/{slug}"
            
            logger.info(f"Buscando detalhes de: {slug}")
            
            response = self.session.get(detail_url, timeout=30)
            response.raise_for_status()
            
            # Extrair informações da página HTML
            details = self.extract_duration_from_html(response.text)
            
            return details
            
        except requests.RequestException as e:
            logger.error(f"Erro ao buscar detalhes de {slug}: {e}")
            return None
    
    def extract_duration_from_html(self, html_content: str) -> Dict:
        """
        Extrai duração e outros detalhes do HTML da página
        """
        details = {
            'duration_days': None,
            'start_date': None,
            'end_date': None,
            'description': None,
            'impact_details': None
        }
        
        try:
            # Buscar padrões comuns de duração no texto
            import re
            
            # Padrões para encontrar duração
            duration_patterns = [
                r'(\d+)\s*days?',
                r'(\d+)\s*weeks?',
                r'lasted\s+(\d+)\s*days?',
                r'duration[:\s]+(\d+)\s*days?',
                r'over\s+(\d+)\s*days?',
                r'for\s+(\d+)\s*days?'
            ]
            
            # Padrões para datas
            date_patterns = [
                r'from\s+(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{4})\s+to\s+(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{4})',
                r'between\s+(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{4})\s+and\s+(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{4})',
                r'(\d{1,2}\s+\w+\s+\d{4})\s+to\s+(\d{1,2}\s+\w+\s+\d{4})'
            ]
            
            text = html_content.lower()
            
            # Buscar duração em dias
            for pattern in duration_patterns:
                match = re.search(pattern, text)
                if match:
                    duration = int(match.group(1))
                    # Converter semanas para dias se necessário
                    if 'week' in pattern:
                        duration *= 7
                    details['duration_days'] = duration
                    logger.info(f"Duração encontrada: {duration} dias")
                    break
            
            # Buscar datas de início e fim
            for pattern in date_patterns:
                match = re.search(pattern, text)
                if match:
                    details['start_date'] = match.group(1)
                    details['end_date'] = match.group(2)
                    logger.info(f"Período encontrado: {match.group(1)} até {match.group(2)}")
                    break
            
            # Extrair descrição básica (primeiros parágrafos)
            desc_match = re.search(r'<p[^>]*>(.*?)</p>', html_content, re.DOTALL)
            if desc_match:
                # Limpar HTML tags
                description = re.sub(r'<[^>]+>', '', desc_match.group(1))
                details['description'] = description.strip()[:500]  # Limitar a 500 chars
            
            # Buscar informações de impacto
            impact_keywords = ['deaths?', 'casualties', 'missing', 'displaced', 'evacuated', 'affected']
            impact_info = []
            
            for keyword in impact_keywords:
                pattern = rf'(\d+[,\d]*)\s+(?:people\s+)?{keyword}'
                matches = re.findall(pattern, text)
                if matches:
                    for match in matches:
                        impact_info.append(f"{match} {keyword}")
            
            if impact_info:
                details['impact_details'] = '; '.join(impact_info[:3])  # Máximo 3 itens
            
        except Exception as e:
            logger.error(f"Erro ao extrair detalhes do HTML: {e}")
        
        return details
    
    def enrich_events_with_duration(self, events: List[Dict]) -> List[Dict]:
        """
        Enriquece eventos existentes com informações de duração
        """
        enriched_events = []
        
        for i, event in enumerate(events):
            logger.info(f"Enriquecendo evento {i+1}/{len(events)}: {event['title']}")
            
            # Buscar detalhes adicionais
            slug = event['metadata']['slug']
            article_id = event['metadata']['article_id']
            
            details = self.get_activation_details(slug, article_id)
            
            if details:
                # Adicionar informações de duração ao evento
                event['duration'] = details
            else:
                # Adicionar estrutura vazia se não conseguir obter detalhes
                event['duration'] = {
                    'duration_days': None,
                    'start_date': None,
                    'end_date': None,
                    'description': None,
                    'impact_details': None
                }
            
            enriched_events.append(event)
            
            # Delay entre requests para não sobrecarregar o servidor
            time.sleep(self.delay_between_requests)
        
        return enriched_events
    
    def save_to_json(self, data: List[Dict], filename: str) -> None:
        """
        Salva dados em arquivo JSON
        """
        try:
            # Garantir que o diretório existe
            import os
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Dados salvos em: {filename}")
            
        except Exception as e:
            logger.error(f"Erro ao salvar arquivo: {e}")

def main():
    """
    Função principal para executar o scraper
    """
    scraper = DisastersCharterScraper()
    
    logger.info("Iniciando coleta de dados de enchentes...")
    
    # Coletar dados de enchentes
    flood_data = scraper.get_flood_activations()
    
    if flood_data:
        # Salvar dados brutos
        raw_filename = "../../data/raw/flood_events_raw.json"
        scraper.save_to_json(flood_data, raw_filename)
        
        # Criar versão processada
        processed_data = {
            'metadata': {
                'total_events': len(flood_data),
                'collection_date': datetime.now().isoformat(),
                'source': 'disasterscharter.org',
                'regions_covered': list(set([event['location']['region'] for event in flood_data])),
                'date_range': {
                    'earliest': min([event['date'] for event in flood_data if event['date']]),
                    'latest': max([event['date'] for event in flood_data if event['date']])
                }
            },
            'events': flood_data
        }
        
        processed_filename = "../../data/processed/flood_events.json"
        scraper.save_to_json(processed_data, processed_filename)
        
        logger.info(f"Coleta concluída! {len(flood_data)} eventos coletados.")
        
        # Estatísticas básicas
        countries = [event['location']['country'] for event in flood_data]
        country_counts = {}
        for country in countries:
            country_counts[country] = country_counts.get(country, 0) + 1
        
        logger.info("Países com mais eventos:")
        for country, count in sorted(country_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
            logger.info(f"  {country}: {count} eventos")
    
    else:
        logger.warning("Nenhum dado coletado!")

if __name__ == "__main__":
    main()
