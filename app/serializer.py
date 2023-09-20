from .config import Config


def msg_new_ticket(msg_body):
    message = (f"<b><u>Оповещение:</u></b>\n"
               f"Новая заявка № {msg_body['id']}\n"
               f"Дата создания: {msg_body['date_creation']}\n"
               f"Срочность: {Config.GLPI_URGENCY[msg_body['urgency']]}\n"
               f"Статус: {Config.GLPI_STATUS[msg_body['status']]}\n"
               f"Тема: {msg_body['name']}\n"
               f"Описание: {msg_body['content'].replace('&lt;p&gt;', '').replace('&lt;/p&gt;', ' ')}\n"
               f"Инициатор: {msg_body['init_fio']}\n"
               f"Исполнитель: {msg_body['exec_fio']}")
    return message


def msg_new_comment(msg_body):
    message = (f"<b><u>Оповещение:</u></b>\n"
               f"Новый комментарий по заявке № {msg_body['id']}\n"
               # f"Дата: {msg_body['date_creation']}\n"
               # f"Срочность: {Config.GLPI_URGENCY[msg_body['urgency']]}\n"
               f"Статус: {Config.GLPI_STATUS[msg_body['status']]}\n"
               f"Тема заявки: {msg_body['name']}\n"
               f"Описание заявки: {msg_body['content'].replace('&lt;p&gt;', '').replace('&lt;/p&gt;', ' ')}\n"
               f"Инициатор заявки: {msg_body['init_fio']}\n"
               f"Исполнитель заявки: {msg_body['exec_fio']}\n"
               f"Комментатор: <b>{msg_body['comment_fio']}</b>\n"
               f"Комментарий: <b>{msg_body['comment_content'].replace('&lt;p&gt;', '').replace('&lt;/p&gt;', ' ')}</b>")
    return message


def msg_new_task(msg_body):
    task_content = msg_body['task_content'].replace('&lt;p&gt;', '').replace('&lt;/p&gt;', ' ')
    message = (f"<b><u>Оповещение:</u></b>\n"
               f"Новая задача по заявке № {msg_body['id']}\n"
               # f"Дата: {msg_body['date_creation']}\n"
               # f"Срочность: {Config.GLPI_URGENCY[msg_body['urgency']]}\n"
               # f"Статус: {Config.GLPI_STATUS[msg_body['status']]}\n"
               f"Тема заявки: {msg_body['name']}\n"
               f"Описание заявки: {msg_body['content'].replace('&lt;p&gt;', '').replace('&lt;/p&gt;', ' ')}\n"
               f"Инициатор заявки: {msg_body['init_fio']}\n"
               f"Исполнитель заявки: {msg_body['exec_fio']}\n"
               f"Описание задачи: <b>{task_content}</b>\n"
               f"Статус задачи: <b>{Config.GLPI_TASK_STATUS[msg_body['task_status']]}</b>\n"
               f"Инициатор задачи: <b>{msg_body['task_init_fio']}</b>\n"
               f"Исполнитель задачи: <b>{msg_body['task_exec_fio']}</b>")
    return message


def msg_update_task(msg_body):
    task_content = msg_body['task_content'].replace('&lt;p&gt;', '').replace('&lt;/p&gt;', ' ')
    message = (f"<b><u>Оповещение:</u></b>\n"
               f"Обновление задачи по заявке № {msg_body['id']}\n"
               # f"Дата: {msg_body['date_creation']}\n"
               # f"Срочность: {Config.GLPI_URGENCY[msg_body['urgency']]}\n"
               # f"Статус: {Config.GLPI_STATUS[msg_body['status']]}\n"
               f"Тема заявки: {msg_body['name']}\n"
               f"Описание заявки: {msg_body['content'].replace('&lt;p&gt;', '').replace('&lt;/p&gt;', ' ')}\n"
               f"Инициатор заявки: {msg_body['init_fio']}\n"
               f"Исполнитель заявки: {msg_body['exec_fio']}\n"
               f"Описание задачи: <b>{task_content}</b>\n"
               f"Статус задачи: <b>{Config.GLPI_TASK_STATUS[msg_body['task_status']]}</b>\n"
               f"Инициатор задачи: <b>{msg_body['task_init_fio']}</b>\n"
               f"Исполнитель задачи: <b>{msg_body['task_exec_fio']}</b>")
    return message


def msg_ticket_solved(msg_body):
    message = (f"<b><u>Оповещение:</u></b>\n"
               f"Заявка № <b>{msg_body['id']}</b> решена\n"
               f"Дата создания: {msg_body['date_creation']}\n"
               f"Срочность: {Config.GLPI_URGENCY[msg_body['urgency']]}\n"
               f"Статус: <b>{Config.GLPI_STATUS[msg_body['status']]}</b>\n"
               f"Тема: {msg_body['name']}\n"
               f"Описание: {msg_body['content'].replace('&lt;p&gt;', '').replace('&lt;/p&gt;', ' ')}\n"
               f"Инициатор: {msg_body['init_fio']}\n"
               f"Исполнитель: {msg_body['exec_fio']}")
    return message
