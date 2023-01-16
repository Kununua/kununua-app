import time

class Timer(object):
    
    def __init__(self, start_time=None, end_time=None):
        self.start_time = start_time
        self.end_time = end_time
        
    def start_timer(self):
        self.start_time = time.time()
        
    def end_timer(self):
        self.end_time = time.time()
        
    def get_time(self):
        return self.end_time - self.start_time