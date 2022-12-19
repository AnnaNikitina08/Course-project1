import requests
import json
from pprint import pprint
from datetime import datetime
import mimetypes
import os
from tqdm import tqdm
import configparser
config = configparser.ConfigParser()
config.read("settings.ini")

class API_VK:

    def __init__(self, version='5.131'):
        self.token = config["VK"]["TOKEN_VK"]
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}
        self.name_photos = {}
        self.date = {}


    def _get_photos_info(self):
        """ Получает список фотографий из профиля пользователя ВКонтакте
       с копией изображения z размера"""
        base_url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': self.id,
                  'album_id': 'profile',
                  'photo_sizes': 1,
                  'extended': 1,
        }
        dict_photos = requests.get(base_url, params={**self.params, **params}).json()
        for photo in dict_photos['response']['items']:
            url = photo['sizes'][-1]['url']
            count_likes = photo['likes']['count']
            self.date[url] = photo['date']
            if count_likes not in self.name_photos.values():
                self.name_photos[url] = count_likes
            else:
                self.name_photos[url] = count_likes, datetime.fromtimestamp(self.date[url]).strftime('%Y-%m-%d')
        print(len(self.name_photos))
        pprint(self.name_photos)
        return

class API_YA:
    def __init__(self, token_disk):
        self.token_disk = token_disk

    def _get_headers(self):
        return {
            'Content-type': 'application/json',
            'Authorization': f'OAuth {self.token_disk}'
        }

    def _create_folder(self):
        """Создает папку с именем folder_name на Яндекс-диске"""
        # base_host = 'https://cloud-api.yandex.net'
        folder_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        params = {'path': folder_name}
        folder = requests.put(folder_url, headers=self._get_headers(),
                                       params=params)
        if folder.status_code == 409:
            answer = input('Такая папка уже существует, добавить в нее файлы?(y/n)')
            if answer == 'y':
                return True
        else:
            print(folder.status_code)
        return

    def upload(self, user_id, num_photos, name_photos):
        """Загружает фотографии из списка в созданную папку"""
        url_upload = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        num_photo = -1
        for key, value in tqdm(name_photos.items(), ncols=100,
                           dynamic_ncols=True, desc='Loading'):
            num_photo += 1
            if num_photo == num_photos:
                break
            params = {'path': f'{folder_name}/{value}', 'url':key,
                      'disable_redirects': True}
            response_upload = requests.post(url_upload,
                                            headers=self._get_headers(),
                                            params=params)
            if response_upload.status_code == 202:
                print('Загрузка прошла успешно!')
            else:
                print(f'Ошибка: {response_upload.status_code}')

        list_info_photo = []
        with open('photos_info.json', 'w') as file:
            for key, value in vk.name_photos.items():
                list_info_photo.append(
                   {
                       'file_name': value,
                       'size': 'z'
                   }
                )

            json.dump(list_info_photo, file)


if __name__ == '__main__':

    user_id = int(input('Введите id пользователя: '))
    token_disk = input('Введите токен Яндекс диска: ')
    folder_name = input("Введите название папки, в которой хотите хранить фото БЕЗ ПРОБЕЛОВ: ")
    vk = API_VK()
    ya = API_YA(token_disk)
    num_photos = int(input(f'Введите количество фото из {len(vk.name_photos)}, которое хотите '
                       f'загрузить'))
    vk._get_photos_info()
    # pprint(vk.name_photos)
    ya._create_folder()
    ya.upload(user_id, num_photos, vk.name_photos)








