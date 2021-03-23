import requests
import os
import shutil
import getpass
from bs4 import BeautifulSoup

# Funções que precisam ser criadas:
'''
1 - Verificar quais arquivos estão em uma pasta do sistema X
2 - limpar o caminho e pegar apenas o nome das pastas X
3 - enviar uma requests para o site com os dados obtidos X
4 - limpar o request e puxar o username X
5 - copiar a cfg do usuario selecionado para a pasta determinada
'''

def BuscarSteamid():
    path = "C:/Program Files (x86)/Steam/userdata"
    pastas = []

    for raiz, diretorios, arquivos in os.walk(path):
        if len(diretorios) != 0:
                pastas.append(diretorios)

    pastas = pastas[0]
    
    for pospasta, pasta in enumerate(pastas):
        if pasta.isnumeric():
            pass
        else:
            pastas.pop(pospasta)
    
    return pastas



def BuscaNomePorId(steamids=[]):

    NomesContas = []    
    
    for steamid in steamids:

        link = f'https://steamidfinder.com/lookup/[U%3A1%3A{steamid}]/'

        site = requests.get(link).content

        limpo = BeautifulSoup(site,'html.parser')

        nome = limpo.find('div',{'class':'panel-body'})
        
        nome_limpo = nome.find_all('code')

        if len(nome_limpo) == 11:
            NomesContas.append(nome_limpo[8].text)
        else:
            NomesContas.append(nome_limpo[7].text)
    
    return NomesContas

def EscolhaUsuario(usernames=[],steamids=[],escolha=''):
    escolha = str(escolha)
    if escolha.isnumeric:
        escolha = int(escolha)-1

    UserEscolha = usernames[escolha]
    SteamEscolha = steamids[escolha]

    return UserEscolha, SteamEscolha

def CopiarArquivo(origem='',destino=''):
    try:
        shutil.copyfile(origem,destino)
    except EOFError as erro:
        print(f'Erro em copir arquivo: {erro}')
        

def CriarCfg(steamid='',NomeCfg='',CopiaDesktop=True,CopiaCs=True,CopiaPersonalizada='X',path='C:/Program Files (x86)/Steam'):
    username = str(getpass.getuser())
    cfg = f'{path}/userdata/{steamid}/730/local/cfg/config.cfg'
    if CopiaDesktop:
        CopiarArquivo(cfg,f'C:/Users/{username}/Desktop/{NomeCfg}.cfg')
    if CopiaCs:
        CopiarArquivo(cfg,path+f'/steamapps/common/Counter-Strike Global Offensive/csgo/cfg/{NomeCfg}.cfg')
    if len(CopiaPersonalizada) > 1:
        CopiarArquivo(cfg,CopiaPersonalizada+f'/{NomeCfg}.cfg')

nomes = BuscaNomePorId(BuscarSteamid())
ids = BuscarSteamid()
ask = int(input('Digite qual Usuario escolha: '))

nome, steam = EscolhaUsuario(nomes,ids,ask)

print(nome, steam)

cfg = input('Digite o nome que deseja para cfg: ')

CriarCfg(steam,cfg,True,True)

