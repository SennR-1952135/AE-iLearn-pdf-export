from lib.writing.objects.BaseAccessor import BaseAccessor

class DBIDTransformer:
    def __init__(self) -> None:
        self.id_counter = 0
        self.id_map = {}

    def get_key_mapping(self) -> dict:
        return self.id_map

    def generate_new_id(self) -> str:
        self.id_counter
        new_id = self.id_counter
        self.id_counter += 1
        return '__' + str(new_id) + '__'
    
    def _is_id_key(self, key: str) -> bool:
        return key == 'id' or key.find('Id') != -1 or key.find('ID') != -1
    
    # def generate_new_accessor_id(self) -> str:
    #     new_id = self.generate_new_id()
    #     return f'<a name="{new_id}"/>{new_id}'

    def accessor(self, wr: BaseAccessor) -> None:
      """transforms all values containing a 'db' id to a new 'local' id"""
      if isinstance(wr, list):
        for item in wr:
          self.accessor(item)
      else:
        for key, value in wr.data.items():
          if isinstance(value, dict) or isinstance(value, list):
            self.accessor(value)
          elif self._is_id_key(key):
              db_id = value
              if db_id in self.id_map:
                wr.data[key] = self.id_map[db_id]
              else:
                new_id = self.generate_new_id()
                self.id_map[db_id] = new_id
                wr.data[key] = new_id
        
    def json(self, obj: dict) -> None:
      """transforms all values containing a 'db' id to a new 'local' id"""
      if isinstance(obj, list):
        for item in obj:
          self.json(item)
      elif isinstance(obj, dict):
        for key, value in obj.items():
          if isinstance(value, dict) or isinstance(value, list):
            self.json(value)
          elif self._is_id_key(key):
              db_id = value
              if db_id in self.id_map:
                obj[key] = self.id_map[db_id]
              else:
                new_id = self.generate_new_id()
                self.id_map[db_id] = new_id
                obj[key] = new_id