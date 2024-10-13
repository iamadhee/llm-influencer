from abc import abstractmethod, ABC


class BaseContentGenerator(ABC):
    @abstractmethod
    def run(self, *args, **kwargs):
        pass
