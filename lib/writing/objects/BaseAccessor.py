from abc import ABC, abstractmethod
from utils.key_translation import key_translation_dict
from writing.visitors.BaseAccessorVisitor import BaseAccessorVisitor

class BaseAccessor(ABC):
    data = {}
    key_map = key_translation_dict

    def _transform_data(self, data: dict) -> dict:
        data = self._remove_empty_fields(data)
        return data

    def _remove_empty_fields(self, data: dict) -> dict:
        return {k: v for k, v in data.items() if (v is not None) and (not hasattr(v, '__len__') or len(v) > 0)}
    
    def _translate_keys(self, data: dict) -> dict:
        return {self.key_map[k]: v for k, v in data.items() if k in self.key_map}

    def get_accessor_data(self) -> dict:
        """Return the accessor data, applying formatting to the data to be printed if necessary"""
        data = self._translate_keys(self.data)
        return data
    
    @abstractmethod
    def _init_accessor_data(self):
        """Initialize the accessor data using the data from the parsed object.
        Used to select the relevant key value pairs that will be written to the output file"""
        pass
    
    @abstractmethod
    def accept(self, visitor: BaseAccessorVisitor):
        """Accept a file specific visitor to visit this accessor object and access its data"""
        pass
    

    
