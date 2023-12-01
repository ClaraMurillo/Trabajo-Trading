import datetime
import math
import time

import backtrader as bt
from backtrader import dataseries
from backtrader.strategy import Strategy

class SMA(Strategy):
    params = (
        ("short_period", 60),
        ("long_period", 220),
    )

    def __init__(self):

        # Agrega el indicador de Media Armónica Simple
        self.short_ma = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.short_period)
        self.long_ma = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.long_period)
    
    def next(self):
        position = self.position.size
        # Verifica si se detecta un Doji
    
        # Lógica de Bandas de Bollinger
        bol_buy =  bol_sell =  macd_buy = macd_sell = sma_buy = sma_sell =  ma_buy = ma_sell = rsi_buy = rsi_sell = False
        total = 0

        # Lógica de la estrategia Golden Cross
        if self.short_ma > self.long_ma and self.short_ma[-1] <= self.long_ma[-1]:
        # Cruce de las medias de abajo hacia arriba, señal de compra
            ma_buy  = True
        elif self.short_ma < self.long_ma and self.short_ma[-1] >= self.long_ma[-1]:
        # Cruce de las medias de arriba hacia abajo, señal de venta
            ma_sell = True

        order_book = self.data.volume[0]

        if ma_buy:
            self.buy(size=100)
        elif ma_sell :
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
    cerebro.addstrategy(SMA)

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