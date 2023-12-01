import datetime
import math
import time

import backtrader as bt
from backtrader import dataseries
from backtrader.strategy import Strategy

class CompraVentaMEP(Strategy):
    params = (
         ("ema_corta", 15),
        ("ema_larga", 28),
        ("ema_senial", 9),
        ("periodo_corto", 60),
        ("periodo_largo", 220),
        ("rsi_periodo", 25),
        ("rsi_bajo", 40),
        ("rsi_alto", 80),
    )

    def __init__(self):
        #velas
        self.martillo = False
        self.hombre_colgado = False

        self.armonica =  bt.indicators.ExponentialMovingAverage(self.data.close, period=20)
        #macd
        self.macd = bt.indicators.MACDHisto(
            period_me1=self.params.ema_corta,
            period_me2=self.params.ema_larga,
            period_signal=self.params.ema_senial
        )
        #golden cross
        self.ma_corta = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.periodo_corto)
        self.ma_larga = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.periodo_largo)
        #rsi
        self.rsi = bt.indicators.RelativeStrengthIndex(period=self.params.rsi_periodo)

    
    def next(self):
        #velas
        if self.data.close[0] < self.data.open[0] and self.data.low[0] == self.data.close[0] and self.data.open[0] == self.data.high[0]:     # Apertura igual al máximo
           self.martillo = True
        else:
           self.martillo = False
        if self.data.close[0] > self.data.open[0] and self.data.low[0] == self.data.close[0] and self.data.open[0] == self.data.high[0]:     # Apertura igual al máximo
            self.hombre_colgado = True
        else:
            self.hombre_colgado = False
        
        macd_buy = ema_buy = ma_buy = rsi_buy  = False
        total = 0
        #ema
        if self.data.close > self.armonica.lines.ema :
            ema_buy = True
        elif  self.data.close < self.armonica.lines.ema :
            total  = total + 1
        #macd
        if self.macd.lines.histo[-1] > 0 and self.macd.lines.histo[0] <= 0:
            macd_buy = True
        elif  self.macd.lines.histo[-1] < 0 and self.macd.lines.histo[0] >= 0:
            total  = total + 1
        
        # Golden Cross
        if self.ma_corta > self.ma_larga and self.ma_corta[-1] <= self.ma_larga[-1]:
        # Cruce de las medias de abajo hacia arriba, señal de compra
            ma_buy  = True
        elif self.ma_corta < self.ma_larga and self.ma_corta[-1] >= self.ma_larga[-1]:
        # Cruce de las medias de arriba hacia abajo, señal de venta
            total  = total + 1
        #rsi
        if self.rsi < self.params.rsi_bajo:
        # RSI por debajo del umbral inferior, señal de compra
            rsi_buy = True
        elif self.rsi > self.params.rsi_alto:
        # RSI por encima del umbral superior, señal de venta
            total  = total + 1

        if (macd_buy  or ema_buy or ma_buy or rsi_buy):
          if macd_buy:
            self.buy(size=100)
          if ema_buy:
            self.buy(size=100)
          if ma_buy:
            self.buy(size=100)
          if rsi_buy:
            self.buy(size=100)
          
        # estrategia de venta: si almenos dos de los indicadores da positivo para la venta o si la tecnica del martillo y 
        # ganancia/pérdida neta incluyendo comisión da positiva para una venta 
        elif (total > 1) :
        # si tengo mas de 100 vendo 100 sino vendo lo q tengo
          if(self.position.size>100):
            self.sell(size=100) 
          else: self.sell(size=self.position.size)
          
        position = self.position.size 
        total = 0
        '''print('Capital disponible: {:.2f}'.format(self.broker.cash))
        position = self.position.size 
        print('Posición actual: {}'.format(position))'''
        
if __name__ == '__main__':
    cerebro = bt.Cerebro()

    # Agregar un Data Feed 
    data = bt.feeds.GenericCSVData(
        dataname='DATASET\orcl-1995-2014.txt',
        fromdate=datetime.datetime(1995, 1, 1),
        todate=datetime.datetime(2014, 12, 31),
        dtformat=('%Y-%m-%d'),  
    )
    #data = dataseries.DataSeries(dataname='orcl-1995-2014.txt', fromdate=datetime(1995, 1, 3), todate=datetime(2014, 12, 31))
    cerebro.adddata(data)

    cerebro.addstrategy(CompraVentaMEP)

    cerebro.broker.set_cash(100000)

    cerebro.broker.setcommission(commission=0.001)

    print('Saldo inicial: %.2f' % cerebro.broker.getvalue())

    cerebro.run()

    print('Saldo final: %.2f' % cerebro.broker.getvalue())

    cerebro.plot()
