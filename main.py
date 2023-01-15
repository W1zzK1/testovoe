import requests
from bs4 import BeautifulSoup as bs
import os
from pydrive.auth import GoogleAuth
import pandas as pd
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.LocalWebserverAuth()

url = "https://confluence.hflabs.ru/pages/viewpage.action?pageId=1181220999"

codes = []
meaning = []

def parsingAPI():
    '''
    Парсинг самого кода ответа и описания для каждого
    '''
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"})
    soup = bs(response.text, 'lxml')

    rows = soup.find_all('td', class_="confluenceTd")

    count = 0
    for i in rows:
        if count % 2 == 0:
            codes.append(i.text)
            count += 1
        else:
            meaning.append(i.text)
            count += 1

    return codes, meaning

def write_pandas():
    '''
    Запись получченных данных в эксель таблицу через pandas
    '''
    df = pd.DataFrame({'Code': codes,
                       'Meaning': meaning})
    writer = pd.ExcelWriter('result.xlsx')
    df.to_excel(writer)
    writer.save()


def upload_dir(file_path=''):
    '''
    Загрузка фалйа на гугл диск
    '''
    try:
        drive = GoogleDrive(gauth)

        file_list = drive.ListFile({'q': "title contains 'result' and trashed=false"}).GetList()
        print(file_list[0]['title'])  # should be the title of the file we just created
        file_id = file_list[0]['id']

        file_name = 'result.xlsx'
        my_file = drive.CreateFile({'id': file_id, 'title': file_name})
        my_file.SetContentFile(file_path)
        my_file.Upload()

        return 'Success!'
    except Exception as _ex:
        return 'Got some trouble'


def main():
    parsingAPI()
    write_pandas()
    print(upload_dir(file_path='C:/Users/W1zzA/PycharmProjects/testovoe/result.xlsx'))


if __name__ =='__main__':
    main()