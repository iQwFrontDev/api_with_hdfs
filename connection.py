from hdfs import InsecureClient


class HdfsConnection:

    def client(self,path,user):
        return InsecureClient(url = path, user = user)


class SettingsRepository:

    def __init__(self,path: str, user: str):
        self.path = path
        self.user = user

