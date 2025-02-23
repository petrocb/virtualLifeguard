from abc import ABC, abstractmethod

class alert(ABC):

    @abstractmethod
    def alertManger(self):
        pass

    def