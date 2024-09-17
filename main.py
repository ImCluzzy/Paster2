import logging
import os
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import telebot
import threading
import yaml
import jobs.telgram

# Создаем каталог logs, если его нет
if not os.path.exists('logs'):
    os.makedirs('logs')

# Настраиваем logging
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Файл для ошибок
error_handler = logging.FileHandler('logs/errors.log', mode='a')
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(formatter)

# Файл для предупреждений и информационных сообщений
info_warning_handler = logging.FileHandler('logs/info_and_warnings.log', mode='a')
info_warning_handler.setLevel(logging.INFO)
info_warning_handler.setFormatter(formatter)

# Создаем логгер и добавляем обработчики
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(error_handler)
logger.addHandler(info_warning_handler)

with open("config.yml", "r") as config_file:
    config = yaml.safe_load(config_file)

tg_token = config["tg"]["token"]
tg_channel = "@" + config["tg"]["channel"]
vk_token = config["vk"]["token"]
vk_group_id = config["vk"]["long"]

bot = telebot.TeleBot(tg_token)
vk = vk_api.VkApi(token=vk_token)
vk.http.headers.update({'Connection': 'close'})
vk.http.timeout = 1000
long = VkBotLongPoll(vk, vk_group_id)


def vk_bot():
    logging.info('Connecting to VK, successful!')
    for event in long.listen():
        if event.type == VkBotEventType.WALL_POST_NEW:
            logging.info('New post!')
            if event.obj.attachments:
                attachments = event.obj.attachments
                text = event.obj.text if event.obj.text else ""
                jobs.telgram.send_message_with_attachments_to_telegram(text, attachments)
            elif event.obj.text:
                text = event.obj.text
                jobs.telgram.send_message(text)
        else:
            logging.warning(event.type)
        logging.info('')


def main():
    vk_thread = threading.Thread(target=vk_bot)
    vk_thread.start()
    tg_thread = threading.Thread(target=bot.polling)
    tg_thread.start()

    while threading.active_count() > 1:
        pass


if __name__ == '__main__':
    main()