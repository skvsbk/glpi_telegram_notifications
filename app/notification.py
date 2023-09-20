import logging

import requests
import logging
import app.glpidb as glpidb
from app.serializer import *


logger = logging.getLogger(__name__)
logger.setLevel('INFO')


def send_message(chat_id_list, message):
    for chat_id in chat_id_list:
        response = requests.get(Config.URL_TG + f'chat_id={chat_id}&parse_mode=HTML&text={message}')
        if response in (200, 201):
            logger.info('send_message() is done for chat_id = %s', chat_id)
        else:
            logger.warning('send_message() does not send for chat_id = %s', chat_id)


def notify_new_ticket(ticket_id):
    query = glpidb.query_new(ticket_id)
    msg_body = glpidb.get_info(query)

    chat_id_list = []
    if msg_body['exec_id'] == 84:
        # get telegramid for all of group_id = 9 (Slesari)
        query = glpidb.query_tlgid(9)
        tlg_id = glpidb.get_info(query, False)
        for item in tlg_id:
            chat_id_list.append(item['telegramidfield'])
    else:
        if msg_body['exec_telegramid']:
            chat_id_list.append(msg_body['exec_telegramid'])

    message = msg_new_ticket(msg_body)
    send_message(chat_id_list, message)


def notify_new_comment(ticket_id):
    query = glpidb.query_comment(ticket_id)
    msg_body = glpidb.get_info(query)

    chat_id_list = []
    init_id = msg_body['init_id']
    exec_id = msg_body['exec_id']
    comment_id = msg_body['comment_id']

    if comment_id == init_id:
        chat_id_list.append(msg_body['exec_telegramid'])
    if comment_id == exec_id:
        chat_id_list.append(msg_body['init_telegramid'])
    if comment_id != init_id and comment_id != exec_id:
        chat_id_list.append(msg_body['exec_telegramid'])
        chat_id_list.append(msg_body['init_telegramid'])

    message = msg_new_comment(msg_body)
    send_message(chat_id_list, message)


def notify_new_task(ticket_id):
    query = glpidb.query_task(ticket_id)
    msg_body = glpidb.get_info(query)

    chat_id_list = []
    init_id = msg_body['init_id']
    exec_id = msg_body['exec_id']
    task_init_id = msg_body['task_init_id']

    if task_init_id in (init_id, exec_id):
        chat_id_list.append(msg_body['task_exec_telegramid'])
    if task_init_id not in (init_id, exec_id):
        chat_id_list.append(msg_body['exec_telegramid'])
        chat_id_list.append(msg_body['task_exec_telegramid'])

    message = msg_new_task(msg_body)
    send_message(chat_id_list, message)


def notify_update_task(ticket_id):
    query = glpidb.query_task(ticket_id)
    msg_body = glpidb.get_info(query)

    chat_id_list = []
    init_id = msg_body['init_id']
    exec_id = msg_body['exec_id']
    task_init_id = msg_body['task_init_id']

    if task_init_id in (init_id, exec_id):
        chat_id_list.append(msg_body['task_exec_telegramid'])
    if task_init_id not in (init_id, exec_id):
        chat_id_list.append(msg_body['exec_telegramid'])
        chat_id_list.append(msg_body['task_exec_telegramid'])

    message = msg_update_task(msg_body)
    send_message(chat_id_list, message)


def notify_ticket_solved(ticket_id):
    query = glpidb.query_new(ticket_id)
    msg_body = glpidb.get_info(query)

    chat_id_list = []

    if msg_body['init_telegramid']:
        chat_id_list.append(msg_body['init_telegramid'])

    message = msg_ticket_solved(msg_body)
    send_message(chat_id_list, message)
