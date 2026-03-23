from repository import BankDataParser, Saver, Reader


def run(url:str, per_page: int,page: int,country:str, user: str = 'root',path: str = None):
    data = BankDataParser(url = url,per_page = per_page,page = page,country = country).get_data()
    client = Saver(path=path,user=user)
    client.saver(data.data)






if __name__ == '__main__':
    per_page = 10
    page = 1
    country = 'AE'
    MAIN_URL = "https://api.apilayer.com/bank_data/all"
    path = 'http://namenode:9870'
    country = 'AE'
    run(url = MAIN_URL,page = page,per_page = per_page,country = country,path=path)