import json
from YA import ya
from VK import vk
import configparser
config = configparser.ConfigParser()
config.read("settings.ini")


if __name__ == '__main__':
    vk.user_id_get()
    vk.get_photos_info()
    vk.user_id_get()
    vk.get_photos_info()
    ya.create_folder()
    ya.upload()


    def photo_info():
        list_info_photo = []
        num_photo = 0
        for key, value in vk.name_photos.items():
            num_photo += 1
            list_info_photo.append(
                {
                    'file_name': value,
                    'size': 'z'
                }
            )
            if num_photo == ya.num_photos:
                break
        with open('photos_info.json', 'w') as file:
            json.dump(list_info_photo, file)

    photo_info()
