import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup as bs
import re
import locale
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')


class Crawler:
    def __init__(self, data_inicial, data_final):
        self.data_inicial = data_inicial
        self.data_final = data_final

    @staticmethod
    def format_data(data):
        data_formatada = datetime.strptime(data, '%d/%m/%Y').strftime('%Y-%m-%d')
        return data_formatada

    def get_html(self):
        html_soup = None
        try:
            data_inicial = self.format_data(self.data_inicial)
            data_final = self.format_data(self.data_final)
            url = f"https://portal.trt3.jus.br/internet/conheca-o-trt/comunicacao/noticias-juridicas?form.widgets.texto=&form.widgets.data_inicio={data_inicial}&form.widgets.data_fim={data_final}&form.buttons.buscar=Buscar"
            

            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'}
            dados = requests.get(url, headers= headers)
            html_soup = bs(dados.text, 'html.parser')
            #print(html_soup)

        except Exception as e:
            print(e)
            
        return html_soup

    def extract_data(self, html):
        if html is None:
            return None 
        noticias_all = []
        def __format_data_publicacao(data_publicacao):
            data_pub = re.search(r'\d{1,2} de \w+ de \d{4}', data_publicacao).group()
            data_obj = datetime.strptime(data_pub, '%d de %B de %Y')
            return data_obj.strftime('%d/%m/%Y')

        try:
            noticias = html.select('dl.trt3-list-noticias div.trt3-row-noticia')
            for noticia in noticias:
                titulo = noticia.select_one('a').text
                data_publicacao = noticia.select_one('span').text
                link = noticia.select_one('a')['href']
                noticias_all.append({
                    'titulo': titulo.replace('\n', '').strip(),
                    'data_publicacao': __format_data_publicacao(data_publicacao),
                    'link': link.replace('\n', '').strip()
                })
            return noticias_all
        except Exception as e:
            print(e)
    
 
    def __main__(self):
        html = self.get_html()
        noticias = self.extract_data(html)
        return noticias