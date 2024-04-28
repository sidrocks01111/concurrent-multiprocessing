"""MongoDB connector"""
import pymongo
import threading

from queue import Empty

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
mp_db = mongo_client["marketPeerDB"]


class MongoMasterScheduler(threading.Thread):
    def __init__(self, input_queue, **kwargs):
        if 'output_queue' in kwargs:
            kwargs.pop('output_queue')
        # print("MongoMasterScheduler initialised")
        super(MongoMasterScheduler, self).__init__(**kwargs)
        self._input_queue = input_queue
        self.start()
        
    def run(self):
        # print("MongoMasterScheduler run")
        while True:
            try:
                val = self._input_queue.get(timeout=10)  #queue timeouts if it doesnt get anything for 10s
            except Empty:
                print("Timeout reached, mongo scheduler stopping")
                break
            
            if val == "DONE":
                break
           
            symbol, price, extracted_time = val
            mongoWorker = MongoWorker(symbol, price, extracted_time)
            mongoWorker.insert_into_db()
           
class MongoWorker():
    def __init__(self, symbol, price, extracted_time):
        # print("MongoWorker init")
        self._symbol = symbol
        self._price = price
        self._extracted_time = extracted_time
        
    def insert_into_db(self):
        # print("MongoWorker insertion")
        mp_db["YahooFin"].insert_one({
            "symbol": self._symbol,
            "price": self._price,
            "extracted_time": self._extracted_time
        })