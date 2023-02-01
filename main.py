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
