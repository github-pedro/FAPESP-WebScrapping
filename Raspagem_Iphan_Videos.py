import pandas as pd
import requests
from bs4 import BeautifulSoup

url = "http://portal.iphan.gov.br/videos?pagina="
coluna_iphan = ['Url_pagina', 'Titulo', 'Url_video']
tabela_iphan_videos = pd.DataFrame(columns=coluna_iphan)

#INTEIRANDO URL POR PAGINA DE 1 ATE 18
for i in range(1,19):
    req = requests.get(url+str(i))
    soup = BeautifulSoup(req.content, 'html.parser')
    buscas = soup.find_all('div', class_="row")

    j=1
    #INTEIRANDO BUSCA PELO HTML
    for busca in buscas:
        #VARIAS BUSCAS SÃO ENCONTRADAS NO HTML MAS SO QUERENMOS 2 PARTES ENTÃO QUANDO O CONTADOR CHEGAR NA PARTE 8 OU 9 DA BUSCA ELE BUSCA OS DADOS QUE QUEREMOS. 
        if(j==8):
            videos = busca.find_all('li', class_="lista-galeria-vertical2-titulo")
            for video in videos:
                dados = video.find_all('a')
                for dado in dados:
                    link = dado.get("href")
                    titulo = dado.next_element
                    #INSERINDO O LINK DO VIDEO E O TITULO NA TABELA
                    tabela_iphan_videos = tabela_iphan_videos.append({'Url_pagina': url+str(i),'Titulo':titulo,'Url_video':link}, ignore_index=True)
                    
        #VARIAS BUSCAS SÃO ENCONTRADAS NO HTML MAS SO QUERENMOS 2 PARTES ENTÃO QUANDO O CONTADOR CHEGAR NA PARTE 8 OU 9 DA BUSCA ELE BUSCA OS DADOS QUE QUEREMOS.           
        if(j==9):
            videos = busca.find_all('li', class_="lista-galeria-vertical2-titulo")
            for video in videos:
                dados = video.find_all('a')
                for dado in dados:
                    link = dado.get("href")
                    titulo = dado.next_element
                    #INSERINDO O LINK DO VIDEO E O TITULO NA TABELA
                    tabela_iphan_videos = tabela_iphan_videos.append({'Url_pagina': url+str(i),'Titulo':titulo,'Url_video':link}, ignore_index=True)
        #CONTADOR PARA BUSCA
        j=j+1

tabela_iphan_videos.to_excel('iphan_videos.xlsx')