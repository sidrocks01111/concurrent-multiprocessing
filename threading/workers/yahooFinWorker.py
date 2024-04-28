from queue import Empty
import time
import random
import threading
from bs4 import BeautifulSoup
import requests
from lxml import html

class YahooFinancePriceScheduler(threading.Thread):
    def __init__(self, input_queue, output_queue, **kwargs):
        # print("YahooFinancePriceScheduler initialised")
        super(YahooFinancePriceScheduler, self).__init__(**kwargs)
        self._input_queue = input_queue
        self._output_queue = output_queue
        self.start()
        
    def run(self):
        # print("YahooFinancePriceScheduler run")
        while True:
            try:
                val = self._input_queue.get(timeout=10)  #queue timeouts if it doesnt get anything for 10s
            except Empty:
                print("Timeout reached, Yahoo scheduler stopping")
                break
            # val = self._input_queue.get() # this is blocking ops. it will wait till it gets the value in queue
            # print("YahooFinVal", val)
            if val == 'DONE':
                if self._output_queue is not None:
                    self._output_queue.put('DONE')
                break
            
            yahooFinWorker = YahooFinWorker(symbol=val)
            price = yahooFinWorker.get_price()
            if self._output_queue is not None:
                output_values = (val, price, int(time.time()))
                self._output_queue.put(output_values) 
            print(price)
            

class YahooFinWorker():
    def __init__(self, symbol, **kwargs):
        # print("YahooFinWorker initialised")
        super(YahooFinWorker, self).__init__(**kwargs)
        self._symbol = symbol
        base_url = 'https://finance.yahoo.com/quote/' + self._symbol
        self._url = base_url
        
        
    def get_price(self):
        # print("YahooFinWorker get_price")
        try:
            r = requests.get(self._url)
            if r.status_code != 200:
                return
            page_contents = html.fromstring(r.text)
            raw_price = page_contents.xpath('//*[@id="quote-header-info"]/div[3]/div[1]/div[1]/fin-streamer[1]')[0].text
            price = float(raw_price.replace(',', ''))
            return price
        except Exception as err:
            print("error", err) 