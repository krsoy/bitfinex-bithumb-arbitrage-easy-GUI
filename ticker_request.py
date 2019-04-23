# -*- coding: utf-8 -*-
# https://www.linkedin.com/in/chenghao1990/

import requests
from multiprocessing import Process
from threading import Thread
import time
import pandas as pd


class BitFinex(Process):

    # it's a rest api
    # set proxy in the first place if you want to use it
    #  example = BitfinexTicker(proxy = 123, 23, 24, 25:1111, use_proxy=True)
    def __init__(self, conn, proxy='127.0.0.1:1080', use_proxy=False):
        Process.__init__(self)
        self.proxy = proxy
        self.use_proxy = use_proxy
        self.proxies = {'https': f'http://{self.proxy}',
                   'http': f'http://{self.proxy}'}

        # conn should be multiprocess pipe object
        self.conn = conn

    # Process auto run when instant the class
    def run(self):
        print('Bitfinex start...')
        self.upload_ticker()
        # thread = Thread(target=self.upload_ticker, daemon=True)
        # thread.start()

    def upload_ticker(self):
        while True:
            data = self.ticker()
            self.conn.send(data)
            time.sleep(10)

    def ohlc(self, TimeFrame, Symbol):
        url = f'https://api-pub.bitfinex.com/v2/candles/trade:{TimeFrame}:{Symbol}/hist?limit=100&sort=-1'
        if self.use_proxy:
            hist = requests.get(url, proxies=self.proxies).json()
        else:
            hist = requests.get(url).json()

        data = pd.DataFrame(data=hist, columns=['time', 'Open', 'Close', 'High', 'Low', 'volumes'])
        return data



    # get all ticker from bitfinex
    # check https://docs.bitfinex.com/v2/reference#rest-public-tickers for response details
    def ticker(self):
        url = 'https://api-pub.bitfinex.com/v2/tickers?symbols=ALL'
        if self.use_proxy:
            ticker_all = requests.get(url, proxies=self.proxies).json()
        else:
            ticker_all = requests.get(url).json()
        return ticker_all


class BitHumb(Process):
    # it's a rest api
    # set proxy in the first place if you want to use it
    #  example = BitfinexTicker(proxy = 123, 23, 24, 25:1111, use_proxy=True)
    def __init__(self, conn, proxy='127.0.0.1:1080', use_proxy=False):
        Process.__init__(self)

        self.proxy = proxy
        self.use_proxy = use_proxy
        self.rest_url = 'https://api-pub.bitfinex.com/v2/'
        self.proxies = {'https': f'http://{self.proxy}',
                   'http': f'http://{self.proxy}'}

        self.conn = conn
        print('bithumb start')

    # Process auto run when instant the class
    def run(self):
        self.upload_ticker()

    def upload_ticker(self):
        while True:
            data = self.ticker()
            self.conn.send(data)
            time.sleep(10)

    # get all ticker from bithumb
    # check https://apidocs.bithumb.com/docs/ticker for response detials
    def ticker(self):
        url = 'https://api.bithumb.com/public/ticker/ALL'
        if self.use_proxy:
            ticker_all = requests.get(url, proxies=self.proxies).json()
        else:
            ticker_all = requests.get(url).json()
        return ticker_all['data']


class ExchangeRate:
    # getting currency exchange rate, here is using USDKRW pair
    def __init__(self, proxy='127.0.0.1:1080', base='USD', target='KRW', use_proxy=False):
        self.pair = base +target
        self.proxy = proxy
        self.use_proxy = use_proxy
        self.rest_url = 'https://api-pub.bitfinex.com/v2/'
        self.proxies = {'https': f'http://{self.proxy}',
                   'http': f'http://{self.proxy}'}

    def rate(self):
        key = 'f898c58dbddd24135db2a45bd2066231'
        url = 'http://apilayer.net/api/live?access_key={}&currencies=KRW&source=USD&format=1'.format(key)
        if self.use_proxy:
            ticker_all = requests.get(url, proxies=self.proxies).json()
        else:
            ticker_all = requests.get(url).json()

        return ticker_all['quotes'][self.pair]





