class Strategy:
    def __init__(self,handler, queue):
        self.handler = handler 
        self.queue = queue
    def calculate_signals(self, event):
        pass