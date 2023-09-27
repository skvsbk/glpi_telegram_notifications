from .config import Config


def serialize_new_ticket(msg_body, executors):
    msg_exec = ', '.join([i['name'] for i in executors])
    message = (f"<b><u>Оповещение:</u></b>\n"
               f"Новая заявка № {msg_body['id']}\n"
               f"Дата создания: {msg_body['date_creation']}\n"
               f"Срочность: {Config.GLPI_URGENCY[msg_body['urgency']]}\n"
               f"Статус: {Config.GLPI_STATUS[msg_body['status']]}\n"
               f"Тема: {msg_body['name']}\n"
               f"Описание: {msg_body['content'].replace('&lt;p&gt;', '').replace('&lt;/p&gt;', ' ')}\n"
               f"Инициатор: {msg_body['init_fio']}\n"
               f"Исполнитель: {msg_exec}")
    return message


def serialize_new_comment(msg_body, executors, comment_content, comment_user):
    msg_exec = ', '.join([i['name'] for i in executors])
    message = (f"<b><u>Оповещение:</u></b>\n"
               f"Новый комментарий по заявке № {msg_body['id']}\n"
               # f"Дата: {msg_body['date_creation']}\n"
               # f"Срочность: {Config.GLPI_URGENCY[msg_body['urgency']]}\n"
               f"Статус: {Config.GLPI_STATUS[msg_body['status']]}\n"
               f"Тема заявки: {msg_body['name']}\n"
               f"Описание заявки: {msg_body['content'].replace('&lt;p&gt;', '').replace('&lt;/p&gt;', ' ')}\n"
               f"Инициатор заявки: {msg_body['init_fio']}\n"
               f"Исполнитель заявки: {msg_exec}\n"
               f"Комментатор: <b>{comment_user}</b>\n"
               f"Комментарий: <b>{comment_content.replace('&lt;p&gt;', '').replace('&lt;/p&gt;', ' ')}</b>")
    return message


def serialize_new_task(msg_body, executors, task):
    msg_exec = ', '.join([i['name'] for i in executors])
    task_content = task['task_content'].replace('&lt;p&gt;', '').replace('&lt;/p&gt;', ' ')
    message = (f"<b><u>Оповещение:</u></b>\n"
               f"Новая задача по заявке № {msg_body['id']}\n"
               # f"Дата: {msg_body['date_creation']}\n"
               # f"Срочность: {Config.GLPI_URGENCY[msg_body['urgency']]}\n"
               # f"Статус: {Config.GLPI_STATUS[msg_body['status']]}\n"
               f"Тема заявки: {msg_body['name']}\n"
               f"Описание заявки: {msg_body['content'].replace('&lt;p&gt;', '').replace('&lt;/p&gt;', ' ')}\n"
               f"Инициатор заявки: {msg_body['init_fio']}\n"
               f"Исполнитель заявки: {msg_exec}\n"
               f"Описание задачи: <b>{task_content}</b>\n"
               f"Статус задачи: <b>{Config.GLPI_TASK_STATUS[task['task_status']]}</b>\n"
               f"Инициатор задачи: <b>{task['task_init_fio']}</b>\n"
               f"Исполнитель задачи: <b>{task['task_exec_fio']}</b>")
    return message


def serialize_update_task(msg_body, executors, task):
    msg_exec = ', '.join([i['name'] for i in executors])
    task_content = task['task_content'].replace('&lt;p&gt;', '').replace('&lt;/p&gt;', ' ')
    message = (f"<b><u>Оповещение:</u></b>\n"
               f"Обновление задачи по заявке № {msg_body['id']}\n"
               # f"Дата: {msg_body['date_creation']}\n"
               # f"Срочность: {Config.GLPI_URGENCY[msg_body['urgency']]}\n"
               # f"Статус: {Config.GLPI_STATUS[msg_body['status']]}\n"
               f"Тема заявки: {msg_body['name']}\n"
               f"Описание заявки: {msg_body['content'].replace('&lt;p&gt;', '').replace('&lt;/p&gt;', ' ')}\n"
               f"Инициатор заявки: {msg_body['init_fio']}\n"
               f"Исполнитель заявки: {msg_exec}\n"
               f"Описание задачи: <b>{task_content}</b>\n"
               f"Статус задачи: <b>{Config.GLPI_TASK_STATUS[task['task_status']]}</b>\n"
               f"Инициатор задачи: <b>{task['task_init_fio']}</b>\n"
               f"Исполнитель задачи: <b>{task['task_exec_fio']}</b>")
    return message


def serialize_ticket_solved(msg_body, executors):
    msg_exec = ', '.join([i['name'] for i in executors])
    message = (f"<b><u>Оповещение:</u></b>\n"
               f"Заявка № <b>{msg_body['id']}</b> решена\n"
               f"Дата создания: {msg_body['date_creation']}\n"
               f"Срочность: {Config.GLPI_URGENCY[msg_body['urgency']]}\n"
               f"Статус: <b>{Config.GLPI_STATUS[msg_body['status']]}</b>\n"
               f"Тема: {msg_body['name']}\n"
               f"Описание: {msg_body['content'].replace('&lt;p&gt;', '').replace('&lt;/p&gt;', ' ')}\n"
               f"Инициатор: {msg_body['init_fio']}\n"
               f"Исполнитель: {msg_exec}")
    return message
