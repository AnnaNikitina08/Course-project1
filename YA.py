import requests
# import json
from VK import vk
from tqdm import tqdm
import configparser
config = configparser.ConfigParser()
config.read("settings.ini")


class YA:
    def __init__(self):
        self.token = config["YA"]["TOKEN_YA"]
        self.num_photos = int(input(f'Введите количество фото, которое хотите загрузить  '))
        self.folder_name = input("Введите название папки, в которой хотите хранить фото БЕЗ ПРОБЕЛОВ: ")

    def _get_headers(self):
        return {
            'Content-type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def create_folder(self):
        """Создает папку с именем folder_name на Яндекс-диске"""
        folder_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        params = {"path": {self.folder_name}}
        folder = requests.put(folder_url, headers=self._get_headers(), params=params)
        if folder.status_code == 409:
            answer = input('Такая папка уже существует, добавить в нее файлы?(y/n)')
            if answer == 'y':
                return True
        else:
            print(folder.status_code)
        return

    def upload(self):
        """Загружает фотографии из списка в созданную папку"""
        url_upload = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        num_photo = -1
        for key, value in tqdm(vk.name_photos.items(), ncols=100,
                               dynamic_ncols=True, desc='Loading'):
            num_photo += 1
            if num_photo > self.num_photos:
                break
            params = {'path': f'{self.folder_name}/{value}', 'url': key,
                      'disable_redirects': True}
            response_upload = requests.post(url_upload,
                                            headers=self._get_headers(),
                                            params=params)

            if response_upload.status_code == 202:
                print('Загрузка прошла успешно!')
            else:
                print(f'Ошибка: {response_upload.status_code}')


ya = YA()
