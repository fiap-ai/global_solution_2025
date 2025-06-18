"""
Script para baixar imagens de satélite dos eventos de enchentes
Baseado na API de imagens do DisastersCharter.org
"""

import json
import sys
import os
import requests
from urllib.parse import urljoin, urlparse
import re
from pathlib import Path
import time

# Adicionar o diretório pai ao path para importar o scraper
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from disasters_scraper import DisastersCharterScraper
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ImagesDownloader:
    def __init__(self):
        self.scraper = DisastersCharterScraper()
        self.base_url = "https://disasterscharter.org"
        self.images_dir = Path("../../data/images")
        self.images_dir.mkdir(parents=True, exist_ok=True)
        
    def get_images_from_api(self) -> list:
        """
        Busca imagens de satélite da API oficial do DisastersCharter (Quickviews de enchentes)
        """
        try:
            # Primeiro tentar usar a resposta salva dos quickviews
            quickviews_response_path = "../../data/disasters_charter/quickviews_flood_api_response.json"
            if os.path.exists(quickviews_response_path):
                logger.info("Usando resposta salva da API de quickviews...")
                with open(quickviews_response_path, 'r', encoding='utf-8') as f:
                    response_text = f.read()
                
                images = self.parse_quickviews_response(response_text)
                if images:
                    logger.info(f"Encontradas {len(images)} imagens de satélite nos quickviews")
                    return images
            
            # Se não funcionou, tentar API diretamente
            url = f"{self.base_url}/library/quickviews"
            params = {'disaster': 'flood', '_rsc': 'dzz1n'}
            
            # Headers baseados no curl fornecido
            headers = {
                'accept': '*/*',
                'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,it;q=0.6',
                'dnt': '1',
                'next-url': '/en/library/quickviews',
                'priority': 'u=1, i',
                'referer': 'https://disasterscharter.org/library/quickviews',
                'rsc': '1',
                'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"macOS"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36'
            }
            
            logger.info("Buscando quickviews de enchentes da API oficial...")
            
            response = self.scraper.session.get(url, params=params, headers=headers, timeout=30)
            response.raise_for_status()
            
            # Extrair dados da resposta (formato específico da API)
            images = self.parse_quickviews_response(response.text)
            
            logger.info(f"Encontradas {len(images)} imagens de satélite nos quickviews")
            return images
            
        except Exception as e:
            logger.error(f"Erro ao buscar quickviews da API: {e}")
            return []
    
    def parse_images_response(self, response_text: str) -> list:
        """
        Extrai imagens da resposta da API
        """
        images = []
        
        try:
            # Buscar pelo padrão específico da resposta da API
            # A resposta contém dados no formato: 2:["$","$L1e",null,{"items":[...]
            
            # Procurar pela linha que contém os dados das imagens
            for line in response_text.split('\n'):
                if '"items":[' in line and '"title":' in line and '"imageUrl":' in line:
                    logger.info("Encontrada linha com dados de imagens")
                    
                    # Extrair a parte JSON dos items
                    start_marker = '"items":['
                    start_idx = line.find(start_marker)
                    
                    if start_idx != -1:
                        # Encontrar o início do array
                        json_start = start_idx + len('"items":')
                        
                        # Encontrar o final do array contando brackets
                        bracket_count = 0
                        json_end = json_start
                        in_string = False
                        escape_next = False
                        
                        for i, char in enumerate(line[json_start:], json_start):
                            if escape_next:
                                escape_next = False
                                continue
                            
                            if char == '\\':
                                escape_next = True
                                continue
                                
                            if char == '"' and not escape_next:
                                in_string = not in_string
                                continue
                                
                            if not in_string:
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
                                images_array = json.loads(json_str)
                                if isinstance(images_array, list):
                                    # Processar cada imagem
                                    for img_data in images_array:
                                        if isinstance(img_data, dict):
                                            # Extrair URL da imagem principal
                                            image_url = None
                                            if 'image' in img_data and isinstance(img_data['image'], dict):
                                                image_url = img_data['image'].get('url')
                                            
                                            # Se não tem imagem principal, usar thumbnail
                                            if not image_url and 'thumbnail' in img_data and isinstance(img_data['thumbnail'], dict):
                                                image_url = img_data['thumbnail'].get('url')
                                            
                                            if image_url:
                                                processed_img = {
                                                    'title': img_data.get('title', 'Unknown'),
                                                    'description': img_data.get('description', ''),
                                                    'imageUrl': image_url,
                                                    'keywords': img_data.get('keywords', 'satellites'),
                                                    'copyright': img_data.get('copyright', ''),
                                                    'dateAsTimestamp': img_data.get('dateAsTimestamp', 0)
                                                }
                                                
                                                # Adicionar thumbnail se disponível
                                                if 'thumbnail' in img_data and isinstance(img_data['thumbnail'], dict):
                                                    processed_img['thumbnailUrl'] = img_data['thumbnail'].get('url')
                                                
                                                # Adicionar dimensões se disponíveis
                                                if 'image' in img_data and isinstance(img_data['image'], dict):
                                                    processed_img['width'] = img_data['image'].get('width', 0)
                                                    processed_img['height'] = img_data['image'].get('height', 0)
                                                
                                                images.append(processed_img)
                                    
                                    logger.info(f"Extraídas {len(images)} imagens da API")
                                    break
                                    
                            except json.JSONDecodeError as e:
                                logger.error(f"Erro ao decodificar JSON: {e}")
                                continue
            
            # Se não encontrou nenhuma imagem, usar fallback
            if not images:
                logger.warning("Nenhuma imagem encontrada na resposta da API")
                images = self.get_hardcoded_images()
                
        except Exception as e:
            logger.error(f"Erro ao analisar resposta: {e}")
            images = self.get_hardcoded_images()
        
        return images
    
    def parse_quickviews_response(self, response_text: str) -> list:
        """
        Extrai imagens dos quickviews de enchentes da resposta da API
        """
        images = []
        
        try:
            # Procurar pela linha que contém os dados dos quickviews
            for line in response_text.split('\n'):
                if '"items":[' in line and '"quickviewId":' in line and '"image1Url":' in line:
                    logger.info("Encontrada linha com dados de quickviews")
                    
                    # Extrair a parte JSON dos items
                    start_marker = '"items":['
                    start_idx = line.find(start_marker)
                    
                    if start_idx != -1:
                        # Encontrar o início do array
                        json_start = start_idx + len('"items":')
                        
                        # Encontrar o final do array contando brackets
                        bracket_count = 0
                        json_end = json_start
                        in_string = False
                        escape_next = False
                        
                        for i, char in enumerate(line[json_start:], json_start):
                            if escape_next:
                                escape_next = False
                                continue
                            
                            if char == '\\':
                                escape_next = True
                                continue
                                
                            if char == '"' and not escape_next:
                                in_string = not in_string
                                continue
                                
                            if not in_string:
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
                                quickviews_array = json.loads(json_str)
                                if isinstance(quickviews_array, list):
                                    # Processar cada quickview
                                    for qv_data in quickviews_array:
                                        if isinstance(qv_data, dict):
                                            # Extrair imagem 1 (pós-desastre)
                                            image1_url = qv_data.get('image1Url')
                                            if image1_url:
                                                processed_img1 = {
                                                    'title': f"{qv_data.get('title', 'Unknown')} - Post-disaster",
                                                    'description': qv_data.get('description', ''),
                                                    'imageUrl': image1_url,
                                                    'keywords': 'satellite, flood, quickview, post-disaster',
                                                    'copyright': qv_data.get('copyrights', ''),
                                                    'country': qv_data.get('country', ''),
                                                    'satellite': qv_data.get('image1Satellite', ''),
                                                    'width': qv_data.get('image1Width', 0),
                                                    'height': qv_data.get('image1Height', 0),
                                                    'quickview_id': qv_data.get('quickviewId', 0)
                                                }
                                                images.append(processed_img1)
                                            
                                            # Extrair imagem 2 (pré-desastre) se disponível
                                            image2_url = qv_data.get('image2Url')
                                            if image2_url:
                                                processed_img2 = {
                                                    'title': f"{qv_data.get('title', 'Unknown')} - Pre-disaster",
                                                    'description': qv_data.get('description', ''),
                                                    'imageUrl': image2_url,
                                                    'keywords': 'satellite, flood, quickview, pre-disaster',
                                                    'copyright': qv_data.get('copyrights', ''),
                                                    'country': qv_data.get('country', ''),
                                                    'satellite': qv_data.get('image2Satellite', ''),
                                                    'width': qv_data.get('image2Width', 0),
                                                    'height': qv_data.get('image2Height', 0),
                                                    'quickview_id': qv_data.get('quickviewId', 0)
                                                }
                                                images.append(processed_img2)
                                    
                                    logger.info(f"Extraídas {len(images)} imagens dos quickviews")
                                    break
                                    
                            except json.JSONDecodeError as e:
                                logger.error(f"Erro ao decodificar JSON dos quickviews: {e}")
                                continue
            
            # Se não encontrou nenhuma imagem, usar fallback
            if not images:
                logger.warning("Nenhuma imagem encontrada nos quickviews")
                images = self.get_hardcoded_images()
                
        except Exception as e:
            logger.error(f"Erro ao analisar resposta dos quickviews: {e}")
            images = self.get_hardcoded_images()
        
        return images
    
    def get_hardcoded_images(self) -> list:
        """
        Imagens baseadas na análise da API (fallback)
        """
        logger.info("Usando dados de fallback - imagens típicas de satélite do Charter")
        return [
            {
                "title": "Satellite Image - Flood Monitoring",
                "description": "Satellite imagery for flood monitoring and assessment",
                "imageUrl": "https://disasterscharter.org/cos-api/api/file/public/article-image/sample1",
                "keywords": "satellite, flood, monitoring"
            },
            {
                "title": "Satellite Image - Disaster Assessment",
                "description": "Satellite imagery for disaster impact assessment",
                "imageUrl": "https://disasterscharter.org/cos-api/api/file/public/article-image/sample2",
                "keywords": "satellite, disaster, assessment"
            }
        ]
    
    def download_image(self, url: str, filename: str) -> bool:
        """
        Baixa uma imagem da URL especificada
        """
        try:
            logger.info(f"Baixando imagem: {filename}")
            
            response = self.scraper.session.get(url, timeout=60, stream=True)
            response.raise_for_status()
            
            # Verificar se é realmente uma imagem
            content_type = response.headers.get('content-type', '').lower()
            if not any(img_type in content_type for img_type in ['image/', 'jpeg', 'jpg', 'png', 'gif']):
                # Tentar pela extensão da URL
                if not any(ext in url.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif', '.tiff', '.tif']):
                    logger.warning(f"URL pode não ser uma imagem: {url}")
                    # Continuar mesmo assim, pois pode ser uma imagem sem content-type correto
            
            filepath = self.images_dir / filename
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            # Verificar se o arquivo foi baixado corretamente
            if filepath.exists() and filepath.stat().st_size > 1024:  # Pelo menos 1KB
                logger.info(f"Imagem baixada com sucesso: {filename} ({filepath.stat().st_size} bytes)")
                return True
            else:
                logger.error(f"Arquivo baixado está vazio ou muito pequeno: {filename}")
                if filepath.exists():
                    filepath.unlink()
                return False
                
        except Exception as e:
            logger.error(f"Erro ao baixar imagem {filename}: {e}")
            return False
    
    def download_images(self) -> list:
        """
        Baixa todas as imagens de satélite disponíveis
        """
        images = self.get_images_from_api()
        
        if not images:
            logger.warning("Nenhuma imagem encontrada na API")
            return []
        
        downloaded_images = []
        images_downloaded = 0
        
        logger.info(f"Iniciando download de imagens de satélite...")
        logger.info(f"Total de imagens encontradas: {len(images)}")
        
        for img in images:
            title = img.get('title', 'Unknown')
            img_url = img.get('imageUrl', '')
            
            if not img_url:
                logger.warning(f"Imagem sem URL: {title}")
                continue
            
            # Determinar extensão da imagem
            parsed_url = urlparse(img_url)
            path_lower = parsed_url.path.lower()
            
            if '.jpg' in path_lower or '.jpeg' in path_lower:
                ext = '.jpg'
            elif '.png' in path_lower:
                ext = '.png'
            elif '.gif' in path_lower:
                ext = '.gif'
            elif '.tiff' in path_lower or '.tif' in path_lower:
                ext = '.tiff'
            else:
                ext = '.jpg'  # Default
            
            # Criar nome do arquivo
            safe_title = re.sub(r'[^\w\s-]', '', title)
            safe_title = re.sub(r'[-\s]+', '_', safe_title)
            filename = f"satellite_{images_downloaded + 1:02d}_{safe_title[:50]}{ext}"
            
            # Baixar a imagem
            if self.download_image(img_url, filename):
                downloaded_images.append({
                    'title': title,
                    'description': img.get('description', ''),
                    'url': img_url,
                    'filename': filename,
                    'filepath': str(self.images_dir / filename),
                    'keywords': img.get('keywords', ''),
                    'file_size': (self.images_dir / filename).stat().st_size
                })
                images_downloaded += 1
                logger.info(f"Imagem {images_downloaded}: {filename}")
            
            # Delay entre downloads
            time.sleep(2)
        
        return downloaded_images
    
    def save_images_metadata(self, images: list):
        """
        Salva metadados das imagens baixadas
        """
        metadata = {
            'total_images': len(images),
            'download_date': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'images_directory': str(self.images_dir),
            'source': 'disasterscharter.org/library/images?type=satellites',
            'total_size_bytes': sum(img['file_size'] for img in images),
            'images': images
        }
        
        metadata_file = self.images_dir / 'images_metadata.json'
        
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Metadados salvos em: {metadata_file}")

def main():
    """
    Função principal para baixar imagens de satélite
    """
    downloader = ImagesDownloader()
    
    # Baixar todas as imagens disponíveis
    images = downloader.download_images()
    
    # Salvar metadados
    downloader.save_images_metadata(images)
    
    # Estatísticas finais
    logger.info(f"\n=== RESUMO DO DOWNLOAD ===")
    logger.info(f"Total de imagens baixadas: {len(images)}")
    logger.info(f"Diretório: {downloader.images_dir}")
    
    if images:
        total_size = sum(img['file_size'] for img in images)
        logger.info(f"Tamanho total: {total_size / (1024*1024):.2f} MB")
        logger.info(f"\nImagens baixadas:")
        for img in images:
            size_mb = img['file_size'] / (1024*1024)
            logger.info(f"  - {img['filename']} ({size_mb:.2f} MB)")
            logger.info(f"    Título: {img['title']}")
    else:
        logger.warning("Nenhuma imagem foi baixada com sucesso.")
    
    logger.info(f"\nDownload de imagens concluído!")

if __name__ == "__main__":
    main()
