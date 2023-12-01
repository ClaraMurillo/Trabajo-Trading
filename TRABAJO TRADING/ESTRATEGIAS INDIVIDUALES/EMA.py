import datetime
import math
import time

import backtrader as bt
from backtrader import dataseries
from backtrader.strategy import Strategy

class estrategiaHMS(Strategy):

    def __init__(self):
        self.harmonic =  bt.indicators.ExponentialMovingAverage(self.data.close, period=20)
        
    def should_sell(self):
        # Lógica para determinar si se debe realizar una venta
        if self.position:
            pnl = self.data.close[0] - self.position.price
            pnlcomm =  pnl - pnl * 0.1  # Ganancia/pérdida neta incluyendo comisión
            return pnlcomm > 0.1
        else:
            return False
    
    def next(self):
        if self.data.close > self.harmonic.lines.ema and self.position.size == 0:
             self.buy(size=100)  # Implement dynamic position sizing
        elif self.data.close < self.harmonic.lines.ema and self.position.size > 0:
             self.sell(size=self.position.size)
      
        
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
    cerebro.addstrategy(estrategiaHMS)

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
    