# -*- coding: utf-8 -*-
# https://www.linkedin.com/in/chenghao1990/

import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import datetime
import pandas as pd
import matplotlib.dates as mdates
from ticker_request import *
from mpl_finance import candlestick_ohlc

class MyMplCanvas(FigureCanvas, QObject):
    """FigureCanvas的最终的父类其实是QWidget。"""
    send_fig = pyqtSignal(str)

    def __init__(self, crypto, timeframe, conn, parent=None, width=16, height=9, dpi=100):

        # 配置中文显示
        plt.rcParams['font.family'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

        #时差
        self.conn = conn
        self.timeframe = timeframe
        self.crypto = crypto
        self.fig = Figure(figsize=(width, height), dpi=dpi, tight_layout=True)

        FigureCanvas.__init__(self, self.fig)
         # 新建一个figure
        self.ax = self.fig.add_subplot(111)
        self.ax.cla()  # 每次绘图的时候不保留上一次绘图的结果
        self.setParent(parent)

        '''定义FigureCanvas的尺寸策略，这部分的意思是设置FigureCanvas，使之尽可能的向外填充空间。'''
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.fig.subplots_adjust(bottom=0.2)
        self.ax.xaxis_date()
        self.ax.autoscale_view()
        self.ax.grid()


    def update(self):
        bitfinex = BitFinex(conn=None, use_proxy=True)
        ohlc = bitfinex.ohlc(self.timeframe, self.crypto)
        print(1)
        candlestick_ohlc(self.ax, zip(mdates.date2num(pd.to_datetime(ohlc.time, unit='ms')),
                                      ohlc['Open'], ohlc['High'],
                                      ohlc['Low'], ohlc['Close']),
                         width=0.6 / (24 * 60))

        print(2)
        plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')




