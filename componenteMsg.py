import time
from datetime import datetime, timedelta, date
# from datetime import datetime, timedelta
# import pandas as pd

from pydantic import BaseModel
import sys, os
from fastapi import  Request, FastAPI
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

app= FastAPI()
listaMsg= []
# listaMsg.append( {"nome": "abne" , "msg" : ["sdafd","asdfaf","adsfasfd"] } )
# listaMsg.append( {"nome": "julio", "msg" : ["aaaaaaa","asdddas","adsfasfd"], "img" : "imggggg"})
# listaMsg.append( {"nome": "carlo", "msg" : ["asdsadsdsa","fffffffff","apppppp"]})


class componenteMsg:

    navegador = webdriver

    def __init__(self):
        objeto= self
        # self.navegador = self.criaPagWeb()
        navegador = self.criaPagWeb()

    @app.get('/')
    async def aa():
        return {"message": "Hello World"}

    @app.post('/post/')
    async def criaMsg(msg:str, dest:str):
        listaMsg.append({"nome": dest, "msg": msg})
    # open("errorlog.txt","a").write(f"\n{datetime.now()}  -  - {dest} ")

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
                for var in mensagem:
                    element.send_keys(var)
                    element.send_keys(Keys.SHIFT+Keys.ENTER)
                element.send_keys(Keys.ENTER)
                time.sleep(0.1)

        
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            open("errorlog.txt","a").write(f"\n{datetime.now()} - Erro ao criar pagina - {exc_type} - {e} - {fname} {exc_tb.tb_lineno}")

objeto = componenteMsg
navegador = objeto.criaPagWeb()






while(1):
    try:
        if(len(listaMsg) != 0): 
            for var in listaMsg:
                if "img" in var:
                    objeto.enviaMensagem(destinatario=var['nome'],mensagem=var['msg'],imagem=var['img'])

                else:
                    objeto.enviaMensagem(destinatario=var['nome'], mensagem=var['msg'] )

            listaMsg.clear()

    except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            open("errorlog.txt","a").write(f"\n{datetime.now()} - Erro no envio  - {exc_type} - {e} - {fname} {exc_tb.tb_lineno}")
        

