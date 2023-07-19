from abc import ABC, abstractmethod

class BaseFileWriter(ABC):
    # @abstractmethod
    # def write(self, file):
    #     pass

    @abstractmethod
    def write(self, data) -> None:
        pass
    
    @abstractmethod
    def write_pair(self, key, value) -> None:
        pass