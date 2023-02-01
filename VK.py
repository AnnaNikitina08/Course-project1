import requests
from datetime import datetime
import configparser
config = configparser.ConfigParser()
config.read("settings.ini")


class VK:
    def __init__(self, version='5.131'):
        self.token = config["VK"]["TOKEN_VK"]
        self.id = input('Введите id пользователя или его screen_name: ')
        if self.id.isdigit is not False:
            pass
        else:
            VK.user_id_get(self)
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}
        self.name_photos = {}
        self.date = {}

    def user_id_get(self):
        base_url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': self.id}
        res = requests.get(base_url, params={**self.params, **params}).json()
        # print(res)
        user_id = res['response'][0]['id']
        self.id = user_id

    def get_photos_info(self):
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
        print(self.name_photos)
        return


vk = VK()
