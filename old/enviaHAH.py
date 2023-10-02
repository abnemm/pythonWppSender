from operator import contains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from pylogix import PLC
import requests
from datetime import datetime, timedelta
import pyperclip
import os
import telebot
import mysql.connector
import time
import pandas as pd
import random
# from webdriver_manager.chrome import ChromeDriverManager

global con
global cursor
bot = telebot.TeleBot('6371886975:AAFPWV0a25zlMo7RPAeiRP4hb7sP1JTMOG0')

def criaSql():

    global con, cursor
    con = mysql.connector.connect(host='localhost', user='asd', password='asd@1234',database='chatbot')
    if con.is_connected():
        db_info = con.get_server_info()
        cursor = con.cursor()
        cursor.execute("select database();")
        linha = cursor.fetchone()

def fazQuery(query):
        return cursor.execute(query)

def removeSql():

    global con, cursor
    if con.is_connected():
        cursor.close()
        con.close()
        print("Conexão ao MySQL foi encerrada")

def retornaStatus(dif):
    if dif < 0:
        return '❌'
    else:
        return '✅'

def enviaHoraAHora():
    
    dataAgora = datetime.now()
    fazQuery("select * from linhas")
    linhas = cursor.fetchall()

    for linha in linhas:
        mensagem = []
        mensagem.append(f'Linha: {linha[1]}')
        mensagem.append(f'Carros: {linha[2]}')
        mensagem.append(f'Modelos: {linha[5]}')
        mensagem.append(f' ')
        dados = []
        print(linha[0])
        fazQuery(f"select * from variaveishoraahora where fk_idLinha = {linha[0]}")
        horarios = cursor.fetchall()
        for horario in horarios:

            horaServidor = datetime.strptime((f"{dataAgora.day}/{dataAgora.month}/{dataAgora.year} {horario[1]}"), "%d/%m/%Y %H:%M:%S")
            if dataAgora>horaServidor :
                tempo = horario[1].total_seconds()
                hours, remainder = divmod(tempo, 3600)
                minutes, seconds = divmod(remainder, 60)
                tempo = '{:02}:{:02}'.format(int(hours), int(minutes))
                dados.append([tempo,horario[5],horario[6],horario[6]-horario[5],horario[7], 'X' ]) 
            else:
                tempo = horario[1].total_seconds()
                hours, remainder = divmod(tempo, 3600)
                minutes, seconds = divmod(remainder, 60)
                tempo = '{:02}:{:02}'.format(int(hours), int(minutes))
                dados.append([tempo, horario[5],0])         
        dadosDF = pd.DataFrame(dados, columns = ['HORA','PED','REAL','DIF','HOR','STATUS'])
        mensagem.append(f'HORA  PED  REAL   DIF   HOR   STATUS')
        for var in dadosDF.index:
            if((dadosDF['REAL'][var]) != 0):
                mensagem.append(f"{dadosDF['HORA'][var]}   {dadosDF['PED'][var]:3}     {int(dadosDF['REAL'][var]):3}      {int(dadosDF['DIF'][var]):3}       {int(dadosDF['HOR'][var]):3}        {retornaStatus(dadosDF['DIF'][var]):3}")
            else:
                mensagem.append(f"{dadosDF['HORA'][var]}   {dadosDF['PED'][var]:3}                                        {'⚪':3}")
        mensagem.append("")
        mensagem.append("Lorem")

        for var in mensagem:
            print(var)
        enviaMensagemWpp(TextoBot=mensagem ,nome=linha[6])

def enviaHoraAHoraTelegram():
    
    dataAgora = datetime.now()
    fazQuery("select * from linhas")
    linhas = cursor.fetchall()

    for linha in linhas:
        mensagem = (f'Linha: {linha[1]} \nCarros: {linha[2]}\n\nModelos: lorem\n\n')      
        for linha in linhas:
            dados = []
            fazQuery(f"select * from variaveishoraahora where fk_idLinha = {linha[0]}")
            horarios = cursor.fetchall()
            for horario in horarios:
                horaServidor = datetime.strptime((f"{dataAgora.day}/{dataAgora.month}/{dataAgora.year} {horario[1]}"), "%d/%m/%Y %H:%M:%S")
                if dataAgora>horaServidor :
                    tempo = horario[1].total_seconds()
                    hours, remainder = divmod(tempo, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    tempo = '{:02}:{:02}'.format(int(hours), int(minutes))
                    dados.append([tempo,horario[5],horario[6],horario[5]-horario[6],horario[7], 'Lorem' ])          
        dadosDF = pd.DataFrame(dados, columns = ['HORA','PED','REAL','DIF','HOR','STATUS'])
        mensagem = f'{mensagem} {dadosDF.to_string(index=False)}'
        print(mensagem)
        
    cursor.execute("select whatsapp from funcionarios where nome = 'Abne'") 
    funcionarios= cursor.fetchall()
    for var in funcionarios:
        bot.send_message(var[0],mensagem)

def setup():
    global navegador
    # navegador = webdriver.Chrome(ChromeDriverManager().install())
    navegador = webdriver.Chrome(r'C:\Users\F54569C\Desktop\Abne\chromedriver.exe')
    navegador.get(r'https://web.whatsapp.com/')
    time.sleep(1)
    print("Aguarda ler qrcode com o celular")
    while len(navegador.find_elements(by=By.ID, value="side")) < 1:
        time.sleep(3) #Aguarda ler qrcode do WhattsApp com o celular
        print(".")
    time.sleep(1)

def enviaMensagemWpp(TextoBot,nome):
    element = navegador.find_element(by=By.XPATH,value='//*[@id="side"]/div[1]/div/div/div[2]/div/div[1]/p')
    element.send_keys(nome)
    element.send_keys(Keys.ENTER)
    element = navegador.find_element(by=By.XPATH,value='//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p')
    for var in TextoBot:
        element.send_keys(var)
        element.send_keys(Keys.SHIFT+Keys.ENTER)
        print(var)
    element.send_keys(Keys.ENTER)
    time.sleep(0.1)

def Main():
    setup()
    while 1:

        hora = datetime.now().hour
        minuto = datetime.now().minute
        segundo = datetime.now().second
        horario = (f'{hora}:{minuto}:{segundo}')
        print (horario)
        if(
            (hora == 7 and minuto == 3 ) or
            (hora == 8 and minuto == 3 ) or
            (hora == 9 and minuto == 3 ) or
            (hora == 10 and minuto == 3 ) or
            (hora == 11 and minuto == 3 ) or
            (hora == 12 and minuto == 3 ) or
            (hora == 13 and minuto == 3 ) or
            (hora == 14 and minuto == 3 ) or
            (hora == 15 and minuto == 3 ) or
            (hora == 15 and minuto == 51 )
        ):
            criaSql()
            enviaHoraAHora()
            removeSql()
        time.sleep(58)


Main()