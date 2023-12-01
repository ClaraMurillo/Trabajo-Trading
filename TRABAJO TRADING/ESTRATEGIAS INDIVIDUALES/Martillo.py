import datetime
import math
import time

import backtrader as bt
from backtrader import dataseries
from backtrader.strategy import Strategy

class CompraVentaMEP(Strategy):

    def __init__(self):
        self.martillo = False
        self.hombre_colgado = False
    
    def next(self):
        position = self.position.size
        # Verifica si se detecta un Doji
        if self.data.close[0] < self.data.open[0] and self.data.low[0] == self.data.close[0] and self.data.open[0] == self.data.high[0]:     # Apertura igual al máximo
           self.martillo = True
        else:
           self.martillo = False

        if self.data.close[0] > self.data.open[0] and self.data.low[0] == self.data.close[0] and self.data.open[0] == self.data.high[0]:     # Apertura igual al máximo
            self.hombre = True
        else:
            self.hombre = False
        
      
        if self.martillo:
            self.buy(size=100)
        elif self.hombre_colgado:
          if(self.position.size>100):
            self.sell(size=100) 
          else: 
             self.sell(size=self.position.size)
        position = self.position.size 

        print('Capital disponible: {:.2f}'.format(self.broker.cash))
        position = self.position.size 
        print('Posición actual: {}'.format(position))
        
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
