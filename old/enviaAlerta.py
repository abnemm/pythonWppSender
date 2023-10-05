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

def criaSql():

    global con, cursor
    con = mysql.connector.connect(host='localhost', user='asd', password='asd@1234',database='chatbot')
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
    navegador = webdriver.Chrome(r'C:\Users\GabrielReis\Desktop\abne\wppSend\chromedriver.exe')
    navegador.get(r'https://web.whatsapp.com/')
    time.sleep(1)
    print("Aguarda ler qrcode com o celular")
    while len(navegador.find_elements(by=By.ID, value="side")) < 1:
        time.sleep(3) #Aguarda ler qrcode do WhattsApp com o celular
        print(".")
    time.sleep(1)

def enviaMensagemWpp(sensor, funcionario):
    mensagem = []
    mensagem.append(f'Ola {funcionario[1]}!')
    mensagem.append(f'Houve um alerta no sensor {sensor[1]} localizado em {sensor[3]}')
    mensagem.append(f'')
    mensagem.append(f'As dicas para resolver o problema são:')
    mensagem.append(f'')
    mensagem.append(f'1-{sensor[4]}')
    mensagem.append(f'2-{sensor[5]}')
    mensagem.append(f'3-{sensor[6]}')


    element = navegador.find_element(by=By.XPATH,value='//*[@id="side"]/div[1]/div/div/div[2]/div/div[1]/p')

    element.send_keys(funcionario[5])
    time.sleep(0.1)
    element.send_keys(Keys.ENTER)

    icone_anexo = navegador.find_element(by=By.XPATH,value='//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/div')
    icone_anexo.click()
    navegador.implicitly_wait(5)
    opcao_imagem = navegador.find_element(by=By.XPATH,value='//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')
    opcao_imagem.send_keys(sensor[7])
    time.sleep(10)
    element = navegador.find_element(by=By.XPATH,value='//*[@id="app"]/div/div/div[3]/div[2]/span/div/span/div/div/div[2]/div/div[1]/div[3]/div/div/div[2]/div[1]/div[1]/p')
    for linha in mensagem:
        element.send_keys(linha)
        element.send_keys(Keys.SHIFT+Keys.ENTER)
    time.sleep(1)
    # botao_enviar = navegador.find_element(by=By.XPATH,value='//*[@id="app"]/div/div/div[3]/div[2]/span/div/span/div/div/div[2]/div/div[2]/div[2]/div/div/span')
    # botao_enviar.click()
    element.send_keys(Keys.ENTER)

def turnoAtual():
    dataHora= datetime.now()
    if(dataHora.hour>=1 and dataHora.hour<6):
        return 3
    elif(dataHora.hour>=6 and dataHora.hour<=15):
        return 1
    else:
        return 2


def buscaSensoresPlc():
        
        fazQuery("select estado from alerta where id = 1")
        estadoDoAlerta = cursor.fetchone()
        if estadoDoAlerta[0] == 1:
            fazQuery("update alerta set estado = 0 where id = 1")
            fazQuery("select * from sensores where bitValidacao = 1")
            sensores = cursor.fetchall()
            for sensor in sensores:
                cursor.execute(f"select * from funcionarios where UTE = {sensor[2]} and turno = {turnoAtual()}") 
                funcionarios = cursor.fetchall()
                for func in funcionarios:
                    enviaMensagemWpp(sensor = sensor, funcionario=func)
                fazQuery(f"update sensores set bitValidacao = 0 where codigo = {sensor[0]}")
                time.sleep(60)  
    


setup()
while 1:

    criaSql()
    for i in range(100):
        buscaSensoresPlc()
        print(i)
    removeSql()
    time.sleep(3)



