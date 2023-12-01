import datetime
import math
import time

import backtrader as bt
from backtrader import dataseries
from backtrader.strategy import Strategy

class CompraVentaMEP(Strategy):
    params = (
        ("rsi_period", 25),
        ("rsi_low", 40),
        ("rsi_high", 80),
    )

    def __init__(self):

        self.rsi = bt.indicators.RelativeStrengthIndex(period=self.params.rsi_period)

    def next(self):
        position = self.position.size
        # Verifica si se detecta un Doji
        bol_buy =  bol_sell =  macd_buy = macd_sell = sma_buy = sma_sell =  ma_buy = ma_sell = rsi_buy = rsi_sell = False
        total = 0
        
        if self.rsi < self.params.rsi_low:
            # RSI por debajo del umbral inferior, señal de compra
            rsi_buy = True
        elif self.rsi > self.params.rsi_high:
            # RSI por encima del umbral superior, señal de venta
            rsi_sell = True
            
        order_book = self.data.volume[0]
        
        if rsi_buy:
            self.buy(size=100)
        elif rsi_sell :
          self.sell(size=position) 
        position = self.position.size 
        total = 0
        '''print('Capital disponible: {:.2f}'.format(self.broker.cash))
        position = self.position.size 
        print('Posición actual: {}'.format(position))'''
        
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
    cerebro.addstrategy(CompraVentaMEP)

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
    #cerebro.plot()
