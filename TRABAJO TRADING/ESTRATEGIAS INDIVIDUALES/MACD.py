import datetime
import math
import time

import backtrader as bt
from backtrader import dataseries
from backtrader.strategy import Strategy

class MACD(Strategy):
    params = (
        ("macd_short", 15),
        ("macd_long", 28),
        ("macd_signal", 9),
    )

    def __init__(self):
        # Agrega el indicador de Media Armónica Simple
        self.macd = bt.indicators.MACDHisto(
            period_me1=self.params.macd_short,
            period_me2=self.params.macd_long,
            period_signal=self.params.macd_signal
        )
    
    def next(self):
        position = self.position.size
        # Verifica si se detecta un Doji

        bol_buy =  bol_sell =  macd_buy = macd_sell = sma_buy = sma_sell =  ma_buy = ma_sell = rsi_buy = rsi_sell = False
        total = 0

        if self.macd.lines.histo[-1] > 0 and self.macd.lines.histo[0] <= 0:
            macd_buy = True
        elif  self.macd.lines.histo[-1] < 0 and self.macd.lines.histo[0] >= 0:
            macd_sell = True
            total  = total + 1

        if macd_buy:
            self.buy(size=100)
        elif (macd_sell) :
          self.sell(size=position) 
        position = self.position.size 
        total = 0
        
if __name__ == '__main__':
    cerebro = bt.Cerebro()

    # Agregar un Data Feed (puedes ajustar esto según tu configuración)
    data = bt.feeds.GenericCSVData(
        dataname='DATASET\orcl-1995-2014.txt',
        fromdate=datetime.datetime(1995, 1, 1),
        todate=datetime.datetime(2014, 12, 31),
        dtformat=('%Y-%m-%d'),  
    )
    #data = dataseries.DataSeries(dataname='orcl-1995-2014.txt', fromdate=datetime(1995, 1, 3), todate=datetime(2014, 12, 31))
    cerebro.adddata(data)

    # Agregar la estrategia
    cerebro.addstrategy(MACD)

    # Configurar el capital inicial
    cerebro.broker.set_cash(100000)

    # Configurar la comisión (puedes ajustar esto según tus necesidades)
    cerebro.broker.setcommission(commission=0.001)

    # Imprimir el saldo inicial
    print('Saldo inicial: %.2f' % cerebro.broker.getvalue())

    # Ejecutar la simulación
    cerebro.run()

    # Imprimir el saldo final
    print('Saldo final: %.2f' % cerebro.broker.getvalue())