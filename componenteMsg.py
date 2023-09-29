import time
from datetime import datetime, timedelta, date
# from datetime import datetime, timedelta
# import pandas as pd

import sys, os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class componenteMsg:

    navegador = webdriver

    def __init__(self):
        objeto= self
        # self.navegador = self.criaPagWeb()
        navegador = self.criaPagWeb()

    def criaPagWeb():
        
        try:
            # navegador = webdriver.Chrome(ChromeDriverManager().install())
            navegador = webdriver.Chrome(r'C:\Users\GabrielReis\Desktop\abne\wppSend\chromedriver.exe')
            navegador.get(r'https://web.whatsapp.com/')
            time.sleep(1)
            os.system('cls')
            print("Aguarda ler qrcode com o celular")
            while len(navegador.find_elements(by=By.ID, value="side")) < 1:
                time.sleep(3) #Aguarda ler qrcode do WhattsApp com o celular
                print(".")
                time.sleep(1)       
            return navegador

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            open("errorlog.txt","a").write(f"\n{datetime.now()} - Erro ao criar pagina - {exc_type} - {fname} {exc_tb.tb_lineno}")
        
    def enviaMensagem(destinatario, mensagem, imagem=0):

        try:
            
            if(imagem==0):
                element = navegador.find_element(by=By.XPATH,value='//*[@id="side"]/div[1]/div/div/div[2]/div/div[1]/p')
                element.send_keys(destinatario)
                time.sleep(0.1)
                element.send_keys(Keys.ENTER)
                print(mensagem)





            # print(componenteMsg.navegador.find)
        
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            open("errorlog.txt","a").write(f"\n{datetime.now()} - Erro ao criar pagina - {exc_type} - {e} - {fname} {exc_tb.tb_lineno}")
        





objeto = componenteMsg
navegador = objeto.criaPagWeb()
time.sleep(6)
objeto.enviaMensagem(destinatario="abne", mensagem="asdasdasdasd")