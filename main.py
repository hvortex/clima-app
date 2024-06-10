import tkinter
from tkinter import *
from tkinter import ttk

# importando bilbiotecas
from PIL import ImageTk, Image
import requests
import datetime
import time

from datetime import datetime
import pytz
import pycountry_convert as pc


##### sobre dados ##
import json

################# cores ###############
co0 = "#444466"  # Preta
co1 = "#feffff"  # branca
co2 = "#6f9fbd"  # azul


fundo_dia = "#6cc4cc"
fundo_noite = "#333366"
fundo_tarde = "#cc6633"

fundo = fundo_dia


janela = Tk()
janela.iconbitmap("ClimaApp.ico")
janela.title('Clima APP')
janela.geometry('370x350')
janela.configure(bg=fundo)

################# Frames ####################

ttk.Separator(janela, orient=HORIZONTAL).grid(row=0, columnspan=1, ipadx=157)

frame_principal = Frame(janela, width=370, height=50, bg=co1, pady=0, padx=0, relief="flat",)
frame_principal.grid(row=1, column=0)

frame_quadros = Frame(janela, width=370, height=300, bg=fundo, pady=12, padx=0, relief="flat",)
frame_quadros.grid(row=2, column=0, sticky=NW)

style = ttk.Style(frame_principal)
style.theme_use("clam")

global imagem

def info():
    api_key = '3683d233a6d7569f4e1d04c9509cb823'
    cidade = e_local.get()
    api_link = "https://api.openweathermap.org/data/2.5/weather?q=" + cidade + "&appid=" + api_key + "&lang=pt" + "&metric"

    # HTTP request
    r = requests.get(api_link)
    # convert the data in 'r' into dictionary
    data = r.json()

    # zona , pais, horas 
    pais_codigo = data['sys']['country']

    zona_fuso = pytz.country_timezones[pais_codigo]

    # --- pais ---
    pais = pytz.country_names[pais_codigo]

    # --- data ---
    zona = pytz.timezone(zona_fuso[0])
    zona_horas = datetime.now(zona)
    zona_horas = zona_horas.strftime("%d %m %Y | %H:%M:%S %p")

    # --- 
    tempo = data["main"]["temp"]
    temperatura = data["main"]["temp"] - 273.15
    umidade = data["main"]["humidity"]
    velocidade = data["wind"]["speed"]
    descrcao = data["weather"][0]["description"]

    # Mudando informaoes
    def country_to_continent(country_name):
        country_alpha2 = pc.country_name_to_country_alpha2(country_name)
        country_continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
        country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)
        return country_continent_name

    continente = country_to_continent(pais)

    l_cidade['text'] = cidade + " - " + pais + " / " + continente

    l_data['text'] = zona_horas

    l_umidade['text'] = "Humidade : " + str(umidade) + "%"

    l_temp['text'] = round(temperatura, 1)
    l_temp_simbol['text'] = "°C"
    l_temp_nome['text'] = "Celsius"

    l_velocidade['text'] = "velocidade do vento : " + str(velocidade)

    l_descricao['text'] = descrcao

    # apresentado sol e lua
    zona_periodo = datetime.now(zona)
    zona_periodo = zona_periodo.strftime("%H")

    global imagem
    global fundo

    zona_periodo = int(zona_periodo)
    if zona_periodo <= 5:
        imagem = Image.open('img/lua.png')
        fundo = fundo_noite
    elif zona_periodo <= 11:
        imagem = Image.open('img/sol_dia.png')
        fundo = fundo_dia
    elif zona_periodo <= 16:
        imagem = Image.open('img/sol_tarde.png')
        fundo = fundo_tarde
    elif zona_periodo <= 19:
        imagem = Image.open('img/lua.png')
        fundo = fundo_noite
    else:
        imagem = Image.open('img/lua.png')
        fundo = fundo_noite

    imagem = imagem.resize((130, 130), Image.LANCZOS)
    imagem = ImageTk.PhotoImage(imagem)
    l_icon1 = Label(frame_quadros, image=imagem, compound=LEFT, bg=fundo, fg="white", font=('Ivy 10 bold'), anchor="nw", relief=FLAT)
    l_icon1.place(x=190, y=50)

    # -- Mudando cor do fundo
    janela.configure(bg=fundo)
    frame_quadros.configure(bg=fundo)
    frame_principal.configure(bg=fundo)

    l_cidade['bg'] = fundo
    l_data['bg'] = fundo
    l_umidade['bg'] = fundo
    l_temp['bg'] = fundo
    l_temp_simbol['bg'] = fundo
    l_temp_nome['bg'] = fundo
    l_velocidade['bg'] = fundo
    l_descricao['bg'] = fundo

e_local = Entry(frame_principal, width=20, justify='left', font=("arial", 14), highlightthickness=1, relief="solid")
e_local.place(x=15, y=10)

b_ver = Button(frame_principal, command=info, text="Ver clima", height=1, bg=co1, fg=co0, font=('Ivy 9 bold'), relief=RAISED, overrelief=RIDGE)
b_ver.place(x=250, y=10)

l_cidade = Label(frame_quadros, text="", height=1, padx=0, relief="flat", anchor="center", font=('Arial 14 '), bg=fundo, fg=co1)
l_cidade.place(x=10, y=4)

l_data = Label(frame_quadros, text="", height=1, padx=0, relief="flat", anchor="center", font=('Arial 10 '), bg=fundo, fg=co1)
l_data.place(x=10, y=54)

l_temp = Label(frame_quadros, text="", height=1, padx=0, relief="flat", anchor="center", font=('Arial 45 '), bg=fundo, fg=co1)
l_temp.place(x=10, y=100)

l_temp_simbol = Label(frame_quadros, text="", height=1, padx=0, relief="flat", anchor="center", font=('Arial 10 bold '), bg=fundo, fg=co1)
l_temp_simbol.place(x=130, y=110)

l_temp_nome = Label(frame_quadros, text="", height=1, padx=0, relief="flat", anchor="center", font=('Arial 8 '), bg=fundo, fg=co1)
l_temp_nome.place(x=130, y=140)

l_umidade = Label(frame_quadros, text="", height=1, padx=0, relief="flat", anchor="center", font=('Arial 10 '), bg=fundo, fg=co1)
l_umidade.place(x=10, y=184)

l_velocidade = Label(frame_quadros, text="", height=1, padx=0, relief="flat", anchor="center", font=('Arial 10 '), bg=fundo, fg=co1)
l_velocidade.place(x=10, y=212)

l_descricao = Label(frame_quadros, text="", height=1, padx=0, relief="flat", anchor="center", font=('Arial 10 '), bg=fundo, fg=co1)
l_descricao.place(x=170, y=190)

janela.mainloop()