# -*- coding: utf-8 -*-

Original file is located at
    https://colab.research.google.com/drive/1MdPXiV39_rgS9hG1VOFCtgeQNI3SRaS8

Import bibliotecas
"""

!pip install influxdb

import csv 
from influxdb import InfluxDBClient
from datetime import datetime
import pandas as pd
#from pandas.io.parsers.readers import read_csv
from pandas import read_csv
import random
import time
import numpy as np 
import random
import math

"""Conexão com o banco"""

import json
client = InfluxDBClient(host='bitsaas-dns-vm-iot.eastus2.cloudapp.azure.com', port=8086, ssl=True, verify_ssl=True)
client.switch_database('db_dados_sensores')
results = client.query('SELECT * FROM "bit_leaf_teste"')
lista = []
total = 0 #tempo total monitorado, em ms
ligado = 0 #tempo total ligado, em ms
inicio = 0 #instante de início, em ms
termino = 0 #instante de término, em ms
consumo = 0 #spent
for i in results:
    for result in i:
          if result['time']:
            total += (result['updtimestart'] - result['updtimeend']) #soma o tempo total monitorado
            t = datetime.fromtimestamp(result['updtimestart']/1000) #transforma o updtimestart de ms para s, divide por mil e transforma em timestamp
            result['on-off']= not result['on-off']
            if result['on-off']: #verificar se a bomba está ligada
              ligado+= 1000 #add 1000 ms ao tempo da bomba ligada
            if inicio ==0: #verifica se não tem registro do início de monitoramento
              inicio = result['updtimestart'] #registra o início do monitoramento
            if termino < result['updtimestart']: #verifica se o término atual é menor que o registro atual
              termino = result['updtimestart'] #registra a última verificação
            result['spent'] = random.random()
            consumo += result['spent'] #registra o consumo 
            blueprint = {
                #"device": result['device'],
                "on-off": result['on-off'],
                "sensor": result['sensor'],
                "updtimeend" : result['updtimeend'],
                "updtimestart" : result['updtimestart'],
                "spent" : result ['spent'],
                "subtotal": (result['updtimestart'] - result['updtimeend']),
                #Total": total,
                "Tempo ligado (ms)": ligado,
                "Data": datetime.strftime(t, "%d/%m/%Y"),
                #"Data": datetime.strftime(t, "%d/%m/%Y %H:%M:%S"),#exibe o timestamp em formato datetime (data completa legível)
                "Dia": datetime.strftime(t,"%a"),
                "Hora": datetime.strftime(t, "%H:%M:%S")
                }
            lista.append(blueprint)        
#print(blueprint)
print(termino)
print(inicio)
print(ligado)
print(consumo)

"""####          Transforma dados extraídos em um DataFrame. """

df =pd.DataFrame(lista)
df.head(100)

df.groupby('spent') # agrupa os campos selecionados nos df.

df.groupby('spent').count() # total em que o device ficou ligado consumindo energia.

print(df)

print(lista)

strdate= 1646470800

#df = pd.DataFrame(strdate)
#df['updtimeend'] = pd.to_datetime(df['updtimeend'], format='%Y%m%d%H%M%S')

#datetimeobj=datetime.strptime(strdate,"%Y-%m-%d %H:%M:%S")

tempo = datetime.fromtimestamp(strdate)
print(tempo)

#adc coluna nova

"""#### Formula que calcula os dados para previsão de consumo: """

'''consumo = 9.43 * (Kw_boia+Kw_bb2) # consumo da semana convertido em R$ tarifa Enell 1.05
print('kw',consumo)
custo = consumo *( Kw_boia + Kw_bb2)*tarifa
print (f'R$:',custo) # consumo médio diário. Quando o device esp32 e acionado sua boia para controle de nível de água do reservatório também e acionada.
