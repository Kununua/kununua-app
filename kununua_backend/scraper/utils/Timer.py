import time

class Timer(object):
    
    def __init__(self, start_time=None, stop_time=None):
        self.start_time = start_time
        self.stop_time = stop_time
        
    def start(self):
        self.start_time = time.time()
        
    def stop(self):
        self.stop_time = time.time()
        
    def get_time(self):
        return self.stop_time - self.start_time