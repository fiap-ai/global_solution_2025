"""
Script para enriquecer eventos existentes com informações de duração
"""

import json
import sys
import os

# Adicionar o diretório pai ao path para importar o scraper
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from disasters_scraper import DisastersCharterScraper
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """
    Enriquece eventos existentes com informações de duração
    """
    scraper = DisastersCharterScraper()
    
    # Carregar eventos existentes
    try:
        with open("../../data/processed/flood_events.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        events = data['events']
        logger.info(f"Carregados {len(events)} eventos para enriquecimento")
        
    except FileNotFoundError:
        logger.error("Arquivo de eventos não encontrado. Execute primeiro o disasters_scraper.py")
        return
    
    # Enriquecer eventos com duração (TODOS os eventos)
    logger.info("Iniciando enriquecimento com informações de duração...")
    logger.info(f"Processando TODOS os {len(events)} eventos coletados")
    
    enriched_events = scraper.enrich_events_with_duration(events)
    
    # Mostrar resultados
    logger.info("\n=== RESULTADOS DO ENRIQUECIMENTO ===")
    for i, event in enumerate(enriched_events):
        duration_info = event.get('duration', {})
        logger.info(f"\nEvento {i+1}: {event['title']}")
        logger.info(f"  País: {event['location']['country']}")
        logger.info(f"  Data: {event['date'][:10] if event['date'] else 'N/A'}")
        logger.info(f"  Duração: {duration_info.get('duration_days', 'N/A')} dias")
        logger.info(f"  Período: {duration_info.get('start_date', 'N/A')} até {duration_info.get('end_date', 'N/A')}")
        logger.info(f"  Impacto: {duration_info.get('impact_details', 'N/A')}")
        if duration_info.get('description'):
            logger.info(f"  Descrição: {duration_info['description'][:100]}...")
    
    # Salvar eventos enriquecidos (TODOS os eventos)
    enriched_filename = "../../data/processed/flood_events_enriched_complete.json"
    
    enriched_data = {
        'metadata': {
            'total_events': len(enriched_events),
            'enrichment_date': scraper.session.headers.get('user-agent', 'unknown'),
            'source': 'disasterscharter.org',
            'note': f'Complete enrichment of all {len(enriched_events)} events with duration information'
        },
        'events': enriched_events
    }
    
    scraper.save_to_json(enriched_data, enriched_filename)
    
    # Estatísticas de duração
    durations = [e['duration']['duration_days'] for e in enriched_events if e['duration']['duration_days']]
    if durations:
        logger.info(f"\nEstatísticas de duração:")
        logger.info(f"  Eventos com duração identificada: {len(durations)}/{len(enriched_events)}")
        logger.info(f"  Duração média: {sum(durations)/len(durations):.1f} dias")
        logger.info(f"  Duração mínima: {min(durations)} dias")
        logger.info(f"  Duração máxima: {max(durations)} dias")
    else:
        logger.warning("Nenhuma duração foi identificada nos eventos testados")
    
    logger.info(f"\nEnriquecimento concluído! Dados salvos em: {enriched_filename}")

if __name__ == "__main__":
    main()
