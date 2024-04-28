import importlib
import threading
import time

import yaml
from multiprocessing import Queue

class YamlPipelineExecutor(threading.Thread):
    
    def __init__(self, pipeline_location):
        super(YamlPipelineExecutor, self).__init__()
        self._pipeline_location = pipeline_location
        self._queues = {}
        self._workers = {}
        self._queue_consumers = {}
        self._downstream_queue = {}
    
    def _load_pipeline(self):
        with open(self._pipeline_location, 'r') as inFile:
            self._yaml_data = yaml.safe_load(inFile)
            # print(self._yaml_data)
    
    def _initialise_queues(self):
        for queue in self._yaml_data['queues']:
            queue_name = queue['name']
            self._queues[queue_name] = Queue()
    
    def _initialize_workers(self):
        for worker in self._yaml_data['workers']:
            WorkerClass = getattr(importlib.import_module(worker['location']), worker['class'])
            input_queue = worker.get('input_queue') #returns None if worker doesnt have input_queue
            output_queue = worker.get('output_queue')
            worker_name = worker['name']
            num_instances = worker.get('instances', 1)
            
            self._downstream_queue[worker_name] = output_queue
            if input_queue is not None:
                self._queue_consumers[input_queue] = num_instances
            
            init_params = {
                'input_queue': self._queues[input_queue] if input_queue is not None else None,
                'output_queue': self._queues[output_queue] if output_queue is not None else None
            }

            input_values = worker.get('input_values')
            if input_values is not None:
                init_params['input_values'] = input_values
            
            self._workers[worker_name] = []
            for i in range(num_instances):
                self._workers[worker_name].append(WorkerClass(**init_params))
    
    def _join_workers(self):
        for worker_name in self._workers:
            for worker_thread in self._workers[worker_name]:
                worker_thread.join()
    
    def process_pipeline(self):
        self._load_pipeline()
        self._initialise_queues()
        self._initialize_workers()
        self._join_workers()
        
    def run(self):
        self.process_pipeline()

        while True:
            total_worker_alive = 0
            worker_stats = []
            to_del = []
            for worker_name in self._workers:
                total_worker_threads_alive = 0
                for worker_thread in self._workers[worker_name]:
                    if worker_thread.is_alive():
                        total_worker_threads_alive += 1
                total_worker_alive += total_worker_threads_alive
                
                if total_worker_threads_alive == 0:
                    if self._downstream_queue[worker_name] is not None:
                        # for output_queue in self._downstream_queue[worker_name]:
                            # print("output",worker_name, output_queue)
                        output_queue = self._downstream_queue[worker_name]
                        number_of_consumers = self._queue_consumers[output_queue]
                        for i in range(number_of_consumers):
                            self._queues[output_queue].put('DONE')
                                
                    # del self._workers[worker_name]
                    to_del.append(worker_name)
                    
                worker_stats.append([worker_name, total_worker_threads_alive])
            print(worker_stats)    
            
            if total_worker_alive == 0:
                break 
            
            # for queue in self._queues:
            #     print(queue, self._queues[queue].qsize()) # doesnt work in mac
            
            for worker_name in to_del:
                del self._workers[worker_name]
                
        #     time.sleep(1)