import sys
from email.header import decode_header
import re
import logging.config
from app.config import Config
from app.notification import notify_new_ticket, notify_new_comment, notify_new_task
from app.notification import notify_ticket_solved, notify_update_task


logging.config.dictConfig(Config.LOGGING_CONFIG)
logger = logging.getLogger(__name__)
logger.setLevel('INFO')

# SUBJECT = ''
#
# for i in range(1, 10):
#     try:
#         SUBJECT += " " + sys.argv[i]
#     except:
#         pass
#
# if SUBJECT == '':
#     logger.warning('Empty argument')
#     sys.exit()
# else:
#     logger.info('Subject: %s', SUBJECT)


# new
# SUBJECT = '=?utf-8?B?W0dMUEkgIzAwMDA4NTFdINCd0L7QstCw0Y8g0LfQsNGP0LLQutCwINCi?= =?utf-8?B?0LXRgdGC0L7QstCw0Y8g0LfQsNGP0LLQutCw?='
SUBJECT = '=?utf-8?B?W0dMUEkgIzAwMDA5ODBdINCd0L7QstCw0Y8g0LfQsNGP0LLQutCwINCe0LE=?= =?utf-8?B?0YXQvtC0?='

# add comment
# SUBJECT = '=?utf-8?B?W0dMUEkgIzAwMDA4NTFdINCd0L7QstGL0Lkg0LrQvtC80LzQtdC9?= =?utf-8?B?0YLQsNGA0LjQuSDQv9C+INC30LDRj9Cy0LrQtSDQotC10YHRgtC+0LLQsNGP?= =?utf-8?B?INC30LDRj9Cy0LrQsA==?='
# SUBJECT = '=?utf-8?B?W0dMUEkgIzAwMDA4NTFdINCd0L7QstGL0Lkg0LrQvtC80LzQtdC9?= =?utf-8?B?0YLQsNGA0LjQuSDQv9C+INC30LDRj9Cy0LrQtSDQotC10YHRgtC+0LLQsNGP?= =?utf-8?B?INC30LDRj9Cy0LrQsA==?='

# add task
# SUBJECT = '=?utf-8?B?W0dMUEkgIzAwMDA4NTFdINCd0L7QstC+0LUg0LfQsNC00LDQvdC40LU=?= =?utf-8?B?INCi0LXRgdGC0L7QstCw0Y8g0LfQsNGP0LLQutCw?='

# update task (N/A)
# SUBJECT = '=?utf-8?B?W0dMUEkgIzAwMDA4NTFdINCe0LHQvdC+0LLQu9C10L3QuNC1INC30LA=?= =?utf-8?B?0LTQsNGH0Lgg0KLQtdGB0YLQvtCy0LDRjyDQt9Cw0Y/QstC60LA=?='

# solve (YES!)
# SUBJECT = '=?utf-8?B?W0dMUEkgIzAwMDA4NTFdINCX0LDRj9Cy0LrQsCDRgNC10YjQtdC90LA=?= =?utf-8?B?INCi0LXRgdGC0L7QstCw0Y8g0LfQsNGP0LLQutCw?='


def decode_subject(subject: str):
    if subject.startswith('Undelivered'):
        return None
    subj_string = decode_header(subject)[0][0].decode('utf-8')
    logger.info('subject-string: %s', subj_string)
    ticket_number = int(re.findall(r'[0-9]{7}', subj_string)[0])
    msg_type = re.findall(r'\w+\s+\w+', subj_string)[0]
    return [ticket_number, msg_type]


def notify():
    subject = decode_subject(SUBJECT)

    if subject is None:
        return

    ticket_id = subject[0]
    msg_type = subject[1]

    if msg_type == 'Новая заявка':
        notify_new_ticket(ticket_id)

    elif msg_type == 'Новый комментарий':
        notify_new_comment(ticket_id)

    elif msg_type == 'Новое задание':
        notify_new_task(ticket_id)

    elif msg_type == 'Обновление задачи':
        notify_update_task(ticket_id)

    elif msg_type == 'Заявка решена':
        notify_ticket_solved(ticket_id)


if __name__ == '__main__':
    notify()
