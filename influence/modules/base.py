from abc import ABC

class BaseModule(ABC):
    def __init__(self, config):
        pass

    def run(self):
        raise NotImplementedError