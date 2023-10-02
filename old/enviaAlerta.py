from operator import contains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from pylogix import PLC
from datetime import datetime, timedelta
# from webdriver_manager.chrome import ChromeDriverManager
import mysql.connector
import time
from datetime import datetime, timedelta, date
from datetime import datetime, timedelta
import pandas as pd
global con
global cursor
import simon
from simon.accounts.pages import LoginPage
from simon.chat.pages import ChatPage
from simon.chats.pages import PanePage
from simon.header.pages import HeaderPage

def criaSql():

    global con, cursor
    con = mysql.connector.connect(host='172.20.233.63', user='asd', password='asd@1234',database='chatbot')
    if con.is_connected():
        db_info = con.get_server_info()
        cursor = con.cursor()

def removeSql():

    global con, cursor
    # FIM SQL
    if con.is_connected():
        cursor.close()
        con.close()
        # print("Conexão ao MySQL foi encerrada")

def fazQuery(query):
        return cursor.execute(query)

def setup():
    global navegador
    # navegador = webdriver.Chrome(ChromeDriverManager().install())
    navegador = webdriver.Chrome(r'F:\Alerta\chromedriver.exe')
    navegador.get(r'https://web.whatsapp.com/')
    time.sleep(1)
    print("Aguarda ler qrcode com o celular")
    while len(navegador.find_elements(by=By.ID, value="side")) < 1:
        time.sleep(3) #Aguarda ler qrcode do WhattsApp com o celular
        print(".")
    time.sleep(1)

def enviaMensagemWpp(sensor, funcionario):
    mensagem = []
    mensagem.append(f'Olá {funcionario[1]}!')
    mensagem.append(f'Houve um alerta no sensor {sensor[1]} localizado em {sensor[3]}')
    mensagem.append(f'')
    # mensagem.append(f'As dicas para resolver o problema são:')
    # mensagem.append(f'')
    # mensagem.append(f'1-{sensor[4]}')
    # mensagem.append(f'2-{sensor[5]}')
    # mensagem.append(f'3-{sensor[6]}')

    element = navegador.find_element(by=By.XPATH,value='//*[@id="side"]/div[1]/div/div/div[2]/div/div[1]/p')

    element.send_keys(funcionario[5])
    time.sleep(0.1)
    element.send_keys(Keys.ENTER)

    icone_anexo = navegador.find_element(by=By.XPATH,value='//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/div')
    icone_anexo.click()
    navegador.implicitly_wait(5)
    opcao_imagem = navegador.find_element(by=By.XPATH,value='//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')
    # opcao_imagem.send_keys(sensor[7])
    opcao_imagem.send_keys(sensor[8])
    time.sleep(10)
    element = navegador.find_element(by=By.XPATH,value='//*[@id="app"]/div/div/div[3]/div[2]/span/div/span/div/div/div[2]/div/div[1]/div[3]/div/div/div[2]/div[1]/div[1]/p')
    
    for linha in mensagem:
        element.send_keys(linha)
        element.send_keys(Keys.SHIFT+Keys.ENTER)
    time.sleep(1)
    # botao_enviar = navegador.find_element(by=By.XPATH,value='//*[@id="app"]/div/div/div[3]/div[2]/span/div/span/div/div/div[2]/div/div[2]/div[2]/div/div/span')
    # botao_enviar.click()
    element.send_keys(Keys.ENTER)

    fazQuery(f'select * from correcoes where fk_codigoSensor = {sensor[0]} order by ultimoOcorrido desc LIMIT 1')
    ultimo = cursor.fetchone()
    fazQuery('Select Max( quantidadeOcorridos ) As Valor From correcoes')
    maior = cursor.fetchone()
    fazQuery(f'select * from correcoes where fk_codigoSensor = {sensor[0]} and quantidadeOcorridos = {maior[0]} and id != {ultimo[0]} ')
    maiores = cursor.fetchall()
    exclusoes = (f' id != {ultimo[0]}')
    for var in maiores:
        exclusoes = (f'{exclusoes} and id != {var[0]} ')
    fazQuery(f'SELECT * FROM `correcoes` where {exclusoes}')
    restante = cursor.fetchall()

    element = navegador.find_element(by=By.XPATH,value='//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]')

    element.send_keys("A ultima falha foi resolvida da seguinte forma:")
    element.send_keys(Keys.SHIFT+Keys.ENTER)
    time.sleep(0.1)
    element.send_keys(ultimo[2])
    element.send_keys(Keys.ENTER)

    element = navegador.find_element(by=By.XPATH,value='//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]')
    element.send_keys("A resolução funcionou?")
    element.send_keys(Keys.ENTER)
    resposta = ultima_msg(navegador)
    print(resposta)
    print(type(resposta))
    if ((resposta == 'sim') or
        (resposta == 'SIM') or
        (resposta == 'Sim')
        ):
            print ('sim recente')
            agora = datetime.now()
            element = navegador.find_element(by=By.XPATH,value='//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]')
            element.send_keys("Otimo!")
            element.send_keys(Keys.ENTER)
            fazQuery(f'UPDATE correcoes SET quantidadeOcorridos = quantidadeOcorridos +1 and ultimoOcorrido = "{agora}" WHERE id = {ultimo[0]};')
            return

    elif((resposta == 'nao') or
          (resposta == 'NAO') or
          (resposta == 'Nao') or
          (resposta == 'NÃO') or
          (resposta == 'não') or
          (resposta == 'Não')) :
    
    
            print ('Não recente')
            
            for lista in maiores:

                element = navegador.find_element(by=By.XPATH,value='//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]')
                element.send_keys(Keys.SHIFT+Keys.ENTER)
                time.sleep(0.1)
                element.send_keys(lista[2])
                element.send_keys(Keys.ENTER)

                element = navegador.find_element(by=By.XPATH,value='//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]')
                element.send_keys("A resolução funcionou?")
                element.send_keys(Keys.ENTER)
                resposta = ultima_msg(navegador)

                if ((resposta == 'sim') or
                    (resposta == 'SIM') or
                    (resposta == 'Sim')
                ):
                        print ('sim maior')
                        agora = datetime.now()
                        element = navegador.find_element(by=By.XPATH,value='//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]')
                        element.send_keys("Otimo!")
                        element.send_keys(Keys.ENTER)
                        fazQuery(f'UPDATE correcoes SET quantidadeOcorridos = quantidadeOcorridos +1 and ultimoOcorrido = "{agora}" WHERE id = {lista[0]};')
                        return

                elif((resposta == 'nao') or
                    (resposta == 'NAO') or
                    (resposta == 'Nao') or
                    (resposta == 'NÃO') or
                    (resposta == 'não') or
                    (resposta == 'Não')) :
                        print ('Não maior')

                        for item in restante:

                            element = navegador.find_element(by=By.XPATH,value='//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]')
                            element.send_keys(Keys.SHIFT+Keys.ENTER)
                            time.sleep(0.1)
                            element.send_keys(lista[2])
                            element.send_keys(Keys.ENTER)

                            element = navegador.find_element(by=By.XPATH,value='//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]')
                            element.send_keys("A resolução funcionou?")
                            element.send_keys(Keys.ENTER)
                            resposta = ultima_msg(navegador)

                            if ((resposta == 'sim') or
                                (resposta == 'SIM') or
                                (resposta == 'Sim')
                            ):
                                    print ('sim resto')
                                    agora = datetime.now()
                                    element = navegador.find_element(by=By.XPATH,value='//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]')
                                    element.send_keys("Otimo!")
                                    element.send_keys(Keys.ENTER)
                                    fazQuery(f'UPDATE correcoes SET quantidadeOcorridos = quantidadeOcorridos +1 and ultimoOcorrido = "{agora}" WHERE id = {item[0]};')
                                    return

                            elif((resposta == 'nao') or
                                (resposta == 'NAO') or
                                (resposta == 'Nao') or
                                (resposta == 'NÃO') or
                                (resposta == 'não') or
                                (resposta == 'Não')) :
                                    print ('Não resto')

                                    element = navegador.find_element(by=By.XPATH,value='//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]')
                                    element.send_keys("Então Como foi feita a resolução?")
                                    element.send_keys(Keys.ENTER)
                                    resposta = ultima_msg(navegador)

                                    
                                    element = navegador.find_element(by=By.XPATH,value='//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]')
                                    element.send_keys("Obrigado pela cooperação!")
                                    element.send_keys(Keys.ENTER)
                                    agora = datetime.now()
                                    fazQuery(f'insert into correcoes (fk_codigoSensor, correcao, ultimoOcorrido, quantidadeOcorridos) values({sensor[0]}, "{resposta}" ,"{agora}",1);')



def turnoAtual():
    dataHora= datetime.now()
    if(dataHora.hour>=1 and dataHora.hour<6):
        return 3
    elif(dataHora.hour>=6 and dataHora.hour<=15):
        return 1
    else:
        return 2

def ultima_msg(navegador):
        
        """ Captura a ultima mensagem da conversa """
        try:
            post = navegador.find_elements(by = By.CLASS_NAME , value="_21Ahp")
            ultimo = len(post) - 1
            print(f'id ultimo {ultimo}')
            mensagemParametro = post[ultimo].find_element_by_css_selector("span.selectable-text").text
            mensagemFinal = post[ultimo].find_element_by_css_selector("span.selectable-text").text
            while(mensagemParametro == mensagemFinal):
                # print(f'parametro: {mensagemParametro}')
                # print(f'Final : {mensagemFinal}')
                post = navegador.find_elements(by = By.CLASS_NAME , value="_21Ahp")
                ultimo = len(post) - 1
                mensagemFinal = post[ultimo].find_element_by_css_selector("span.selectable-text").text             
            return mensagemFinal
        except Exception as e:
            print("Erro ao ler msg, tentando novamente!")

def buscaSensoresPlc():
        
        fazQuery("select estado from alerta where id = 1")
        estadoDoAlerta = cursor.fetchone()
        # if estadoDoAlerta[0] == 1:
        fazQuery("update alerta set estado = 0 where id = 1")
        fazQuery("select * from sensores where bitValidacao = 1")
        sensores = cursor.fetchall()
        for sensor in sensores:
            cursor.execute(f"select * from funcionarios where UTE = {sensor[2]} and turno = {turnoAtual()}") 
            funcionarios = cursor.fetchall()
            for func in funcionarios:
                enviaMensagemWpp(sensor = sensor, funcionario=func)
            # fazQuery(f"update sensores set bitValidacao = 0 where codigo = {sensor[0]}")
            time.sleep(60)  
    


setup()
while 1:

    criaSql()
    for i in range(100):
        buscaSensoresPlc()
        print(i)
    removeSql()
    time.sleep(3)



