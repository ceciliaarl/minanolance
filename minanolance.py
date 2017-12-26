import requests
from bs4 import BeautifulSoup
from datetime import datetime
hoje = datetime.now().date()
remetente = ' ' # Digite seu endereço de e-mail (ex: 'email@email.com)
senha = ' ' # Digite a senha do seu e-mail (ex: '12345')
destinatarios = [' ')] # ex: email@email.com, email2@email.com

msg = '\nOlá! \n\nPrepare sua torcida, porque hoje tem jogo da Superliga Feminina de Vôlei. Se liga no que vai rolar:\n\n'
superliga = []
volei = False

# Consulta à tabela de jogos

url = 'http://superliga.cbv.com.br/tabela-jogos/Feminino'
resposta = requests.get(url)
sopa = BeautifulSoup(resposta.content, 'html.parser')
bloco = sopa.find_all("div", "jogos-da-rodada")


for linha in bloco:
    canal = linha.find("div", {"class": "col-sm-2 ranking-item data"})
    canal = canal.find("img")
    if 'redetv' in str(canal):
        televisionado = True
        RedeTV = True
    elif 'sportvcom' in str(canal):
        televisionado = True
        Sportvcom = True
    elif 'sportv.png' in str(canal):
        televisionado = True
        Sportv = True
    elif canal == None:
        televisionado = False
        
    horario = linha.find("div", {"class": "col-sm-2 ranking-item data"}).text.strip()
    if horario.endswith("TV"):
        break
    data = horario.split(' | ')[0]
    hora = horario.split(' | ')[1]
    data = datetime.strptime(data, "%d/%m/%Y").date()
    
    equipes = linha.find("div", {"class": "col-sm-7 ranking-item equipes"}).text.strip()
    time1 = equipes.split(' X ')[0]
    time1 = time1.strip().title()
    time2 = equipes.split(' X ')[1]
    time2 = time2.strip().title()
    
    partida = {"Data": data, "Horário": hora, "Equipe 1": time1, "Equipe 2": time2}
    superliga.append(partida)
    
    if data == hoje and televisionado == False:
        msg += f'- {hora} - {time1} x {time2}, mas não vai ser transmitido.\n'
        volei = True
    elif data == hoje and televisionado == True and RedeTV == True:
        msg += f'- {hora} - {time1} x {time2}, com transmissão pela RedeTV. Não deixe de assistir!\n'
        volei = True
    elif data == hoje and televisionado == True and Sportv == True:
        msg += f'- {hora} - {time1} x {time2}, com transmissão pelo SporTV. Não deixe de assistir!\n'
        volei = True
    elif data == hoje and televisionado == True and Sportvcom == True:
        msg += f'- {hora} - {time1} x {time2}, com transmissão pelo SporTV.COM. Não deixe de assistir!\n'
        volei = True

msg += f'\nVamos prestigiar os jogos dessa rodada e continuar cobrando cada vez mais visibilidade do vôlei feminino na televisão.\n\n Bons jogos!\n\nminanolance'

# Envio de e-mails

import smtplib
from email.mime.text import MIMEText
msg = MIMEText(msg)
server = smtplib.SMTP('', 587) # Digite seu servidor SMTP de e-mail (ex: 'smtp-mail.outlook.com')
server.ehlo()
server.starttls()
server.login(remetente, senha)

if volei == True:
    msg['Subject'] = "Hoje tem jogo!"
    msg['From'] = remetente
    msg['To'] = ", ".join(destinatarios)
    server.sendmail(remetente, destinatarios, msg.as_string())
    server.quit()
    
if volei == False:
    naovai = input('Não vai ter jogo. Quer enviar um e-mail de alerta mesmo assim? (sim/não) ')
    if naovai.lower() == sim:        
        naotemjogo = MIMEText("""Hoje não tem jogo na SuperLiga de vôlei, vamos esperar a próxima partida ;)\n\nminanolance""")
        naotemjogo['Subject'] = "Hoje não tem jogo :("
        naotemjogo['From'] = remetente
        naotemjogo['To'] = ", ".join(destinatarios)
        server.sendmail(remetente, destinatarios, naotemjogo.as_string())
        server.quit()
    elif naovai.lower() == não:
        print('Então até a próxima checagem!')
