from abc import ABC, abstractmethod

class FrameProvider(ABC):

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def release(self):
        pass