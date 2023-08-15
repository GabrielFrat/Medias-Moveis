import pandas as pd
import pandas_ta as ta
import MetaTrader5 as mt5
import tkinter as tk
import time
import yfinance as yf
import matplotlib as mp
import matplotlib.pyplot as plt
from time import sleep
from datetime import date


def enviar_email():
    pass

mt5.initialize()
def cruzamentoMediasMoveis():
    while True:
        diaAtual = date.today()
        
        strDia = str(diaAtual)
        print(strDia)
        symbol = "BOVA11"
        lot = 1.0
        position = mt5.positions_total()
        data = yf.download('VALE3.SA', '2020-01-01', strDia)
        print(data)
        # Pegar o momento de compra e venda
        data['SMA09'] = data['Close'].rolling(9).mean()
        data['SMA21'] = data['Close'].rolling(21).mean()

        data['Anterior'] = data['SMA09'].shift(1) - data['SMA21'].shift(1)
        data['Atual'] = data['SMA09'] - data['SMA21']
        data.loc[(data['Anterior'] < 0) & (data['Atual'] > 0), 'Compra'] = data['Close']
        data.loc[(data['Anterior'] > 0) & (data['Atual'] < 0), 'Vender'] = data['Close']
        
        action = ""

        anterior = data['Anterior'].iloc[-1]
        atual = data['Atual'].iloc[-1]

        anterior = anterior.astype(float)
        atual = atual.astype(float)
        if anterior > 0.0 and atual < 0.0:
            action = "Vender"
        elif anterior < 0.0 and atual > 0.0:
            action = "Comprar"
        elif anterior < 0.0 and atual < 0.0:
            action = "Vender"
        elif anterior > 0.0 and atual > 0.0:
            action = "Comprar"

        print(action)
        if action == "Comprar" and position == 0:
            point = mt5.symbol_info(symbol).point
            price = mt5.symbol_info_tick(symbol).ask
            deviation = 200
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": lot,
                "type": mt5.ORDER_TYPE_BUY,
                "price": price,
                # "sl": price - 150 * point,
                # "tp": price + 150 * point,
                "sl": 0.0,
                "tp": 0.0,
                "deviation": deviation,
                "magic": 234000,
                "comment": "python script open",
                "type_time": mt5.ORDER_TIME_GTC,
            }
            result = mt5.order_send(request)
            # verificamos o resultado da execução
            print("1. order_send(): by {} {} lots at {} with deviation={} points".format(symbol,lot,price,deviation));
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                print("2. order_send failed, retcode={}".format(result.retcode))
        elif action == "Vender" and position > 0:
            position_id=result.order
            price=mt5.symbol_info_tick(symbol).bid
            deviation=200
            request={
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": lot,
                "type": mt5.ORDER_TYPE_SELL,
                "position": position_id,
                "price": price,
                "deviation": deviation,
                "magic": 234000,
                "comment": "python script close",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_RETURN,
            }
            # enviamos a solicitação de negociação
            result=mt5.order_send(request)
            # verificamos o resultado da execução
            print("3. close position #{}: sell {} {} lots at {} with deviation={} points".format(position_id,symbol,lot,price,deviation));

        elif position > 0:
            print("Esperar")
        else:
            print("Esperar")

        print(anterior)
        print(atual)
        sleep(10)





cruzamentoMediasMoveis()