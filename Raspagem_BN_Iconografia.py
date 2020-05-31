import pandas as pd
import requests
from bs4 import BeautifulSoup

url = "http://acervo.bn.gov.br/sophia_web/acervo/detalhe/"

coluna_Iconografia = ['Titulo', 'Chave', 'Valor']
tabelaIconografia = pd.DataFrame(columns=coluna_Iconografia)
coluna_troca = ['Chave']
tabelaChave = pd.DataFrame(columns=coluna_troca)
j=0

#FOR PARA CADA PAGINA
for i in range(1,4):
    #REQUEST PARA CADA PAGINA
    req = requests.get(url + str(i))
    soup = BeautifulSoup(req.content, 'html.parser')
    #BUSCANDO TITULO DO REGISTRO
    titulo = soup.find('h1', class_='titulo').next_element
    #ADICIONANDO A URL A TABELA
    tabelaIconografia = tabelaIconografia.append({'Titulo': titulo,'Chave': "Url", 'Valor': url+str(i)}, ignore_index=True)
    #INTERANDO PARA CADA CHAVE DO REGISTRO
    registro = soup.find_all('label', class_='control-label')
    for registros in registro:
        chave = registros.next_element
        #ADICIONANDO CHAVES A COLUNA CHAVE PARA DEPOIS PASSAR ESSE DICIONARIO PARA O DICIONARIO ICONOGRAFIA PASSANDO O VALOR PARA A COLUNA 'CHAVE' DA ICONOGRAFIA
        tabelaChave = tabelaChave.append({'Chave': chave}, ignore_index=True)
    
    #INTERANDO PARA CADA VALOR DA CHAVE DO REGISTRO
    registro = soup.find_all('p')
    for registros in registro:
        valor = registros.next_element
        #USANDO ESSE IF POR QUE O FOR ESTAVA BUSCANDO NO HTML ESSA STRING QUE NÃO CONTÉM NO REGISTRO
        if(valor!="Você não tem acesso a este arquivo."):
            #ADICIONANDO OS VALORES DAS CHAVES DO REGISTRO
            tabelaIconografia = tabelaIconografia.append({'Titulo': titulo, 'Chave': tabelaChave['Chave'][j], 'Valor': valor}, ignore_index=True)
            j = j+1
    
    #INTEIRANDO PARA CADA ASSUNTO NA CHAVE ASSUNTOS NO REGISTRO   
    buscarAssunto = soup.find_all('div', class_='box-conteudo')
    for busca in buscarAssunto:
        busca2 = busca.find_all('a')
        for assuntos in busca2:
            assunto = assuntos.get("title")
            tabelaIconografia = tabelaIconografia.append({'Titulo': titulo, 'Chave': "Assuntos", 'Valor': assunto}, ignore_index=True)
    
    #INTEIRANDO PARA CADA AUTOR NA CHAVE AUTORIA NO REGISTRO  
    buscarAutoria = soup.find_all('div', class_='box-duplo autoria-sem-funcao')
    for busca in buscarAutoria:
        busca2 = busca.find_all('a')
        for assuntos in busca2:
            assunto = assuntos.get("title")
            tabelaIconografia = tabelaIconografia.append({'Titulo': titulo, 'Chave': "Autoria", 'Valor': assunto}, ignore_index=True)

#EXPORTANDO TABELA PARA O EXCEL    
tabelaIconografia.to_excel('iconografia.xlsx')