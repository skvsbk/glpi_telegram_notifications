import os
from dotenv import load_dotenv


class Config:
    load_dotenv('./.env')

    BOT_TOKEN = os.getenv('BOT_TOKEN')
    URL_GLPI = os.getenv('URL_GLPI')

    LOG_FILENAME = './app/log/bot_creation.log'
    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s module:%(name)s %(levelname)s: %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "logfile": {
                "formatter": "default",
                "level": "INFO",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": LOG_FILENAME,
                "backupCount": 7,
            },
        },
        "root": {
            "level": "WARNING",
            "handlers": [
                "logfile",
            ]
        }
    }

    # Database usage
    DB_HOST = os.getenv('DB_HOST')
    DB_NAME = os.getenv('DB_NAME')
    DB_USER = os.getenv('DB_USER')
    DB_PASS = os.getenv('DB_PASS')

    # Telegram url https://api.telegram.org/bot<TOKEN>/sendMessage?chat_id=<CHAT_ID>&parse_mode=HTML&text=Hello%20World
    URL_TG = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?'

    GLPI_STATUS = {1: 'Новый',
                   2: 'В работе (назначена)',
                   3: 'В работе (запланирована)',
                   4: 'Ожидающие',
                   5: 'Решена',
                   6: 'Закрыто'}

    GLPI_URGENCY = {1: "Низкая",
                    2: "Очень низкая",
                    3: "Обычная",
                    4: "Высокая",
                    5: "Очень высокая"}

    GLPI_TASK_STATUS = {0: 'Информация',
                        1: 'К исполнению',
                        2: 'Выполнена'}

    # List of telegram_id (chief engineer etc)
    MANDATORY_NOTIFY = []

    # id of Дежурный слесарь
    NOTYIFY_ALL_OF_USER = 84
    # id group of Слесари
    NOTYFY_ALL_IN_GRP = 9

    DO_NOT_NOTIFY_TICKET_NAME = ("Обход",)

    # Notification period
    NOTIFY_START_TIME = 9
    NOTIFY_STOP_TIME = 18
