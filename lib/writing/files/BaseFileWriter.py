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
    
    @abstractmethod
    def build(self) -> None:
        """Builds the pdf file, printing the content to the file and saves it to the specified filename"""
        pass
    
    @abstractmethod
    def get_file_stream(self):
        """Builds the pdf file, writes the content to a file stream, and returns the file stream"""
        pass