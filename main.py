# -*- coding: utf-8 -*-
# https://www.linkedin.com/in/chenghao1990/

from GravityUi3 import *
from multiprocessing import Pipe
from ticker_request import *
from PyQt5.QtWidgets import QApplication, QMainWindow, qApp
from threading import Thread
from ohlc_canvas import *

class MyMainWindow(QMainWindow,Ui_MainWindow):

    # The crypto I choose to show, you can change it, once you change it
    # you should change all 3 list, same order in each list

    crypto_list = ['Bitcoin', 'Litecoin', 'Ethereum', 'Bitcoin ABC', 'Bitcoin SV',
                   'Monero', 'Zcash', 'Ripple', 'Eos', 'Bitcoin Gold', 'Dash']
    bitfinex_pair = ['tBTCUSD', 'tLTCUSD', 'tETHUSD', 'tBABUSD', 'tBSVUSD', 'tXMRUSD',
                     'tZECUSD',  'tXRPUSD', 'tEOSUSD', 'tBTGUSD', 'tDSHUSD']
    bithumb_pair = ['BTC', 'LTC', 'ETH', 'BCH', 'BSV', 'XMR', 'ZEC', 'XRP', 'EOS', 'BTG', 'DASH']

    # Pipe obeject to exchange item between Process
    bitfinex_send, bitfinex_recv = Pipe()
    bithumb_send, bithumb_recv = Pipe()
    mpl_send, mpl_recv = Pipe()

    def __init__(self,parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.bitfinex = BitFinex(self.bitfinex_send, use_proxy=True)
        self.bithumb = BitHumb(self.bithumb_send, use_proxy=True)
        self.bitfinex.daemon = True
        self.bithumb.daemon = True
        self.bitfinex.start()
        self.bithumb.start()
        self.dynamic_thread = Thread(target=self.dynamic_text, daemon=True)
        self.dynamic_thread.start()

        self.mpl = MyMplCanvas(self.mpl_send, '1h', 'tBTCUSD')
        self.horizontalLayout_3.addWidget(self.mpl)
        print('init finish')



    def dynamic_text(self):
        self.crypto_name.setText('')
        self.bitfinex_crypto.setText('Bitfinex')

        rate = ExchangeRate(use_proxy=True).rate()

        for num, crypto in zip(range(1, 12), self.crypto_list):
            getattr(self, f'crypto_name{num}').setText(crypto)
        for num, crypto in zip(range(1, 12), self.crypto_list):
            getattr(self, f'arbit_name{num}').setText(crypto)


        while True:
            bitfinex_data = self.bitfinex_recv.recv()
            bithumb_data = self.bithumb_recv.recv()

            list_keys = [x[0] for x in bitfinex_data]
            list_values = [round(x[1], 3) for x in bitfinex_data]
            dict_pair = {key: value for (key, value) in zip(list_keys, list_values)}

            for num, pair in zip(range(1, 12), self.bitfinex_pair):
                getattr(self, f'crypto_name2_{num}').setText(f'{dict_pair[pair]}')
            for num, pair in zip(range(1, 12), self.bithumb_pair):
                price = float(bithumb_data[pair]['buy_price']) / rate
                getattr(self, f'crypto_name3_{num}').setText(f'{round(price, 3)}')

            for num, pair1 , pair2 in zip(range(1, 12), self.bitfinex_pair, self.bithumb_pair):
                bitfinex_price = float(dict_pair[pair1])
                bithumb_price = float(bithumb_data[pair2]['buy_price']) / rate
                compare_price = round(bitfinex_price/bithumb_price, 4)

                getattr(self, f'arbit_price{num}').setText(f'{compare_price}')
                getattr(self, f'crypto_name2_{num}').setText(f'{bitfinex_price}')
                getattr(self, f'crypto_name3_{num}').setText(f'{bithumb_price}')




            time.sleep(10)


if __name__ == '__main__':
    import sys
    import multiprocessing
    multiprocessing.freeze_support()
    app = QApplication(sys.argv)
    win = MyMainWindow()
    win.show()
    try:
        app.exec_()
    except:
        print('Exiting')
