import time
from datetime import datetime, timedelta, date
from fastapi import FastAPI
# from flask import Flask, request
# from datetime import datetime, timedelta
# import pandas as pd

import sys, os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

app = FastAPI()


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
                element = navegador.find_element(by=By.XPATH,value='//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p')
                time.sleep(0.1)
                for var in mensagem:
                    element.send_keys(var)
                    element.send_keys(Keys.SHIFT+Keys.ENTER)
                    print(var)
                element.send_keys(Keys.ENTER)
            
            if(imagem!=0):
                print("asd")
                element = navegador.find_element(by=By.XPATH,value='//*[@id="side"]/div[1]/div/div/div[2]/div/div[1]/p')
                element.send_keys(destinatario)
                time.sleep(0.1)
                element.send_keys(Keys.ENTER)
                icone_anexo = navegador.find_element(by=By.XPATH,value='//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/div')
                icone_anexo.click()
                navegador.implicitly_wait(5)
                opcao_imagem = navegador.find_element(by=By.XPATH,value='//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')
                opcao_imagem.send_keys(imagem)
                time.sleep(5)
                element = navegador.find_element(by=By.XPATH,value='//*[@id="app"]/div/div/div[3]/div[2]/span/div/span/div/div/div[2]/div/div[1]/div[3]/div/div/div[2]/div[1]/div[1]/p')
                for var in mensagem:
                    element.send_keys(var)
                    element.send_keys(Keys.SHIFT+Keys.ENTER)
                    print(var)
                element.send_keys(Keys.ENTER)
                time.sleep(1)
                element.send_keys(Keys.ENTER)
        
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            open("errorlog.txt","a").write(f"\n{datetime.now()} - Erro ao criar pagina - {exc_type} - {e} - {fname} {exc_tb.tb_lineno}")

class mensagem():
    texto = [str]
    dest = str

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.put("/asd/{mensagem}")
def update_item(mensagem: int):
    return {"item_name": item.name, "item_id": item_id}

    # # objeto = componenteMsg
    # # navegador = objeto.criaPagWeb()

    # @app.route("/",methods=['GET','POST'])
    # def response(self):
    #     dest = request.form('dest')
    #     msg = request.form('msg')
    #     open("errorlog.txt","a").write(f"\n{datetime.now()} - NOME={dest} MSG={msg}")
    #     open("errorlog.txt","a").write(f"\n{datetime.now()} - NOME={dest} MSG={msg}")
    # # objeto.enviaMensagem(destinatario=dest, mensagem=[msg])




# objeto = componenteMsg
# navegador = objeto.criaPagWeb()

# objeto = componenteMsg
# navegador = objeto.criaPagWeb()
# time.sleep(6)
# objeto.enviaMensagem(destinatario="abne", mensagem="asdasdasdasd")

