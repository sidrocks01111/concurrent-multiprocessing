import threading

import requests
from bs4 import BeautifulSoup


class WikiWorkerMasterScheduler(threading.Thread):
    def __init__(self, output_queue, **kwargs):
        if 'input_queue' in kwargs:
            kwargs.pop('input_queue')
        
        self._input_values = kwargs.pop('input_values')
        self._output_queue = output_queue
        super(WikiWorkerMasterScheduler, self).__init__(**kwargs)
        self.start()
        
    def run(self):
        for entry in self._input_values:
            wikiWorker = WikiWorker(entry)
            
        symbol_counter = 0
        for symbol in wikiWorker.get_sp_500_companies():
            self._output_queue.put(symbol)
            symbol_counter += 1
            if symbol_counter > 5:
                break
        
        # for i in range(20):
        #     self._output_queue.put("DONE")
        
        
class WikiWorker():
    def __init__(self, url) -> None:
        # self._url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
        self._url = url
    
    @staticmethod    
    def _extract_companies_symbol(page_html):
        soup = BeautifulSoup(page_html, 'lxml') 
        table = soup.find(id='constituents')
        table_rows = table.find_all('tr')
        counter = 0
        for table_row in table_rows[1:]:
            if counter > 5:
                break
            counter = counter+1;
            symbol = table_row.find('td').text.strip('_n').strip('\n')
            yield symbol  
        
    def get_sp_500_companies(self):
        try:
            response = requests.get(self._url)
        except Exception as err:
            print(str(err))
            
        yield from self._extract_companies_symbol(response.text)