import pandas as pd
import pandas_ta as ta
import MetaTrader5 as mt5
import tkinter as tk
import time


mt5.initialize()
symbol = "BOVA11"
lot = 1.0
request = {}
result = 0
position_id = 0

def enviar_email(tipo):
    pass

while True:
    data = pd.DataFrame(mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M1, 0, 90))
    data['time'] = pd.to_datetime(data['time'], unit="s")
    data['mm9'] = data.ta.sma(9)

    media = (list(data['mm9'])[-1])
    fechamento = (list(data['close'])[-1])

    print("====================================================")
    
    print("Média: ", media) 
    print("Fechamento:", fechamento)

    position = mt5.positions_total()
    print(position)

    if(fechamento < media and position == 0):
        print("Comprar")
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
        
    elif(fechamento > media and position > 0):
        print("Fechar Posição")
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

    elif(fechamento < media and position > 0):
        print("Esperar, Posição Aberta")
    else:
        print("Esperar")

    time.sleep(10)
