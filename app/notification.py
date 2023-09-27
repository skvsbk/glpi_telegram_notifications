from datetime import datetime
import requests
import logging
import app.glpidb as glpidb
from app.serializer import *


logger = logging.getLogger(__name__)
logger.setLevel('INFO')


def send_message(chat_id_list, message, silent=False):
    for chat_id in chat_id_list:
        if chat_id == '':
            continue
        url = Config.URL_TG + f'chat_id={chat_id}&parse_mode=HTML&disable_notification={silent}&text={message}'
        response = requests.get(url)
        if response.status_code in (200, 201):
            logger.info(f'send_message() is done for chat_id = {chat_id}, silent={silent}, '
                        f'status_code={response.status_code}')
        else:
            logger.warning(f'send_message() does not send for chat_id={chat_id}, silent={silent}, '
                           f'status_code={response.status_code}')
            logger.warning('response.text=%s', response.text)
            logger.warning('response.content=%s', response.content)


def notify_new_ticket(ticket_id):
    query_ticket_string = glpidb.query_ticket(ticket_id)
    query_ticket_result = glpidb.run_db_query(query_ticket_string)

    query_exec_name_sting = glpidb.query_executors_name(ticket_id)
    query_exec_name_result = glpidb.run_db_query(query_exec_name_sting, False)

    query_exec_telid_string = glpidb.query_telegramid_for_all_executors(ticket_id)
    query_exec_telid_result = glpidb.run_db_query(query_exec_telid_string, False)

    chat_id_set = {i for i in Config.MANDATORY_NOTIFY}
    chat_id_silent_set = set()

    for item in query_exec_telid_result:
        if item['id'] == Config.NOTYIFY_ALL_OF_USER:
            # Add user for notification with sound
            chat_id_set.add(item['telegramidfield'])
            # get telegramid for all of group_id = 9 (Slesari) if item['id']=84 (Dej.slesar)
            query_string = glpidb.query_telegramid_for_group(Config.NOTYFY_ALL_IN_GRP)
            tlg_id = glpidb.run_db_query(query_string, False)
            for telid in tlg_id:
                chat_id_silent_set.add(telid['telegramidfield'])
        else:
            chat_id_silent_set.add(item['telegramidfield'])

    message = serialize_new_ticket(query_ticket_result, query_exec_name_result)
    send_message(list(chat_id_set), message)

    # Send without sound from 18 till 9 and all weekdays
    if Config.NOTIFY_START_TIME <= datetime.now().hour < Config.NOTIFY_STOP_TIME or datetime.now().weekday() in (5, 6):
        send_message(list(chat_id_silent_set), message, False)
    else:
        send_message(list(chat_id_silent_set), message, True)


def notify_new_comment(ticket_id):
    query_ticket_string = glpidb.query_ticket(ticket_id)
    query_ticket_result = glpidb.run_db_query(query_ticket_string)

    query_exec_name_sting = glpidb.query_executors_name(ticket_id)
    query_exec_name_result = glpidb.run_db_query(query_exec_name_sting, False)

    query_exec_telid_string = glpidb.query_telegramid_for_all_executors(ticket_id)
    query_exec_telid_result = glpidb.run_db_query(query_exec_telid_string, False)

    query_comment_string = glpidb.query_last_comment(ticket_id)
    query_comment_result = glpidb.run_db_query(query_comment_string)

    chat_id_set = {i for i in Config.MANDATORY_NOTIFY}

    init_id = query_ticket_result['init_id']
    exec_id = [i['id'] for i in query_exec_telid_result]
    exec_telegramid_set = {i['telegramidfield'] for i in query_exec_telid_result}
    comment_id = query_comment_result['comment_id']

    if comment_id == init_id:
        chat_id_set.update(exec_telegramid_set)
    if comment_id in exec_id:
        chat_id_set.add(query_ticket_result['init_telegramid'])
    if comment_id != init_id and comment_id != exec_id:
        chat_id_set.update(exec_telegramid_set)
        chat_id_set.add(query_ticket_result['init_telegramid'])

    comment_content = query_comment_result['comment_content']
    comment_user = query_comment_result['comment_user']
    message = serialize_new_comment(query_ticket_result, query_exec_name_result, comment_content, comment_user)
    send_message(list(chat_id_set), message)


def task_base(ticket_id):
    query_ticket_string = glpidb.query_ticket(ticket_id)
    query_ticket_result = glpidb.run_db_query(query_ticket_string)

    query_exec_name_sting = glpidb.query_executors_name(ticket_id)
    query_exec_name_result = glpidb.run_db_query(query_exec_name_sting, False)

    query_exec_telid_string = glpidb.query_telegramid_for_all_executors(ticket_id)
    query_exec_telid_result = glpidb.run_db_query(query_exec_telid_string, False)

    query_task_string = glpidb.query_task_content(ticket_id)
    query_task_result = glpidb.run_db_query(query_task_string)

    chat_id_set = {i for i in Config.MANDATORY_NOTIFY}

    init_id = query_ticket_result['init_id']
    exec_id = [i['id'] for i in query_exec_telid_result]
    task_init_id = query_task_result['task_init_id']

    if task_init_id in (init_id, exec_id):
        chat_id_set.add(query_task_result['task_exec_telegramid'])
    else:
        chat_id_set.add(query_task_result['exec_telegramid'])
        chat_id_set.add(query_task_result['task_exec_telegramid'])

    return {'ticket': query_ticket_result,
            'executors': query_exec_name_result,
            'task_result': query_task_result,
            'chat_id_set': chat_id_set}


def notify_new_task(ticket_id):
    task = task_base(ticket_id)

    message = serialize_new_task(task['ticket'], task['executors'], task['task_result'])
    send_message(list(task['chat_id_set']), message)


def notify_update_task(ticket_id):
    task = task_base(ticket_id)

    message = serialize_update_task(task['ticket'], task['executors'], task['task_result'])
    send_message(list(task['chat_id_set']), message)


def notify_ticket_solved(ticket_id):
    query_ticket_string = glpidb.query_ticket(ticket_id)
    query_ticket_result = glpidb.run_db_query(query_ticket_string)

    query_exec_name_sting = glpidb.query_executors_name(ticket_id)
    query_exec_name_result = glpidb.run_db_query(query_exec_name_sting, False)

    chat_id_set = {i for i in Config.MANDATORY_NOTIFY}

    if query_ticket_result['init_telegramid']:
        chat_id_set.add(query_ticket_result['init_telegramid'])

    message = serialize_ticket_solved(query_ticket_result, query_exec_name_result)
    send_message(list(chat_id_set), message)


if __name__ == '__main__':
    pass
