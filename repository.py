import requests
from key import secret_key
import json
from connection import HdfsConnection, SettingsRepository



class BankDataParser:


    def __init__(self,**kwargs):
        self.url = kwargs['url']
        self.params = {k:v for k,v in kwargs.items() if k != 'url'}
        self.session = requests.Session()
        self.headers = {
            f"apikey": secret_key
        }
        self.data = kwargs.get('data', {})

    def get_data(self) -> dict:

        with self.session as s:
            s.headers.update(self.headers)
            s.params.update(self.params)
            self.data = s.get(self.url).json()

        return self

    def sort_by_key(self, key_path: str, reverse: bool = False):
        if not self.data or 'data' not in self.data:
            raise ValueError("Нет ключа 'data' для сортировки.")

        target_list = self.data['data']

        def extract_value(item, path):
            if '.' in path:
                val = item
                for k in path.split('.'):
                    if isinstance(val, dict):
                        val = val.get(k)
                    else:
                        return ""
                return val if val is not None else ""

            def find_recursively(d, target_key):
                if isinstance(d, dict):
                    if target_key in d:
                        return d[target_key]
                    for v in d.values():
                        result = find_recursively(v, target_key)
                        if result is not None:
                            return result
                return None

            res = find_recursively(item, path)
            return res if res is not None else ""

        self.data['data'] = sorted(target_list, key=lambda x: extract_value(x, key_path), reverse=reverse)

        return self


    def __repr__(self):
        return repr(self.data)



class Saver(HdfsConnection,SettingsRepository):


    def __init__(self,path:str,user:str):
        super().__init__(path,user)

    def saver(self,data):
        client = self.client(self.path,self.user)
        client.write('test.json', json.dumps(data))

class Reader(HdfsConnection,SettingsRepository):

    def __init__(self,path:str,user:str):
        super().__init__(path,user)

    def reader(self,path):
        client = self.client(self.path,self.user)
        try:
            with client.read(path) as reader:
                model = json.load(reader)
            return model
        except Exception as e:
            print(e)


