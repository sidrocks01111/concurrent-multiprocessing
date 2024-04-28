import time
import logging

from multiprocessing import Queue

from yaml_reader import YamlPipelineExecutor

# def main():
#     symbol_queue = Queue()
#     mongo_queue = Queue()
#     scraper_start_time = time.time()
    
#     # web scraper threads
#     wikiWorker = WikiWorker()
#     yahoo_fin_price_schedular_threads = []
#     num_yahoo_fin_price_workers = 5
#     for i in range(num_yahoo_fin_price_workers):
#         print("creating Yahoo Fin Worker Threads")
#         yahooFinancePriceScheduler = YahooFinancePriceScheduler(input_queue=symbol_queue, output_queue=mongo_queue)
#         yahoo_fin_price_schedular_threads.append(yahooFinancePriceScheduler)
    
#     # db threads
#     mongo_worker_schedular_threads = []
#     num_mongo_workers = 3
#     for i in range(num_mongo_workers):
#         print("creating Mongo Worker Threads")
#         mongoWorkerScheduler = MongoMasterScheduler(input_queue=mongo_queue)
#         mongo_worker_schedular_threads.append(mongoWorkerScheduler)
         
#     for symbol in wikiWorker.get_sp_500_companies():
#         print("putting in symbol queue",symbol)
#         symbol_queue.put(symbol)
    
#     for i in range(len(yahoo_fin_price_schedular_threads)):
#         symbol_queue.put('DONE')
        
#     for i in range(len(yahoo_fin_price_schedular_threads)):
#         yahoo_fin_price_schedular_threads[i].join()
        
#     for i in range(len(mongo_worker_schedular_threads)):
#         mongo_worker_schedular_threads[i].join()

#     print('Extracting Time :', round(time.time() - scraper_start_time, 1))
    

def main():
    pipeline_location = 'pipelines/wiki_yahoo_scraper_pipeline.yaml'
    yamlPipelineExecutor = YamlPipelineExecutor(pipeline_location=pipeline_location)
    # yamlPipelineExecutor.process_pipeline()
    yamlPipelineExecutor.start()
    yamlPipelineExecutor.join()
    scraper_start_time = time.time()

    print('Extracting Time :', round(time.time() - scraper_start_time, 1))      
    
if __name__ == "__main__":
    main()