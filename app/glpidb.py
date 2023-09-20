import logging
import pymysql
from app.config import Config


logger = logging.getLogger(__name__)
logger.setLevel('INFO')


def db_connetion():
    # DB credentials
    db_host = Config.DB_HOST
    db_name = Config.DB_NAME
    db_user = Config.DB_USER
    db_pass = Config.DB_PASS

    # Connect to DB
    return pymysql.connect(
        host=db_host,
        user=db_user,
        password=db_pass,
        db=db_name,
        cursorclass=pymysql.cursors.DictCursor)

def get_info(query, single=True):
    connection = db_connetion()
    result = None
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            if single:
                result = cursor.fetchone()
            else:
                result = cursor.fetchall()

    except Exception as e:
        logger.warning('get_ticket_info() - error ticket_id')
        logger.warning(e)
    finally:
        logger.info('the get_ticket_info() is done ')
        connection.close()
    return result


def query_tlgid(group_id):
    """
    SELECT glpi_plugin_fields_usertelegramids.telegramidfield FROM glpi_groups_users groups_users
    JOIN glpi_plugin_fields_usertelegramids ON glpi_plugin_fields_usertelegramids.items_id = groups_users.users_id
    WHERE groups_users.groups_id = 9
    """
    query = (f"SELECT glpi_plugin_fields_usertelegramids.telegramidfield FROM glpi_groups_users groups_users "
             f"JOIN glpi_plugin_fields_usertelegramids "
             f"ON glpi_plugin_fields_usertelegramids.items_id = groups_users.users_id "
             f"WHERE groups_users.groups_id = {group_id}")
    logger.info('query_tlgid() is done for group_id = %s', group_id)
    return query


def query_new(ticket_id):
    # users_id_recipient - initiator
    """
    SELECT ticket.id, ticket.name, ticket.content, ticket.date_creation, ticket.status, ticket.urgency,
    ticket.users_id_recipient AS init_id,
    CONCAT(users_init.realname, ' ', users_init.firstname ) AS init_fio,
    init_telegramids.telegramidfield AS init_telegramid,
    executor.users_id AS exec_id,
    CONCAT(users_exec.realname, ' ', users_exec.firstname ) AS exec_fio,
    exec_telegramids.telegramidfield AS exec_telegramid
    FROM glpi_tickets AS ticket
    JOIN glpi_tickets_users AS executor ON ticket.id = executor.tickets_id
    JOIN glpi_users AS users_exec ON users_exec.id = executor.users_id
    JOIN glpi_users AS users_init ON users_init.id = ticket.users_id_recipient
    LEFT JOIN glpi_plugin_fields_usertelegramids AS exec_telegramids  ON exec_telegramids.items_id = users_exec.id
    LEFT JOIN glpi_plugin_fields_usertelegramids AS init_telegramids ON init_telegramids.items_id = users_init.id
    WHERE ticket.id = 851
    AND executor.type = 2
    """
    query = (f"SELECT ticket.id, ticket.name, ticket.content, ticket.date_creation, ticket.status, ticket.urgency, "
             f"ticket.users_id_recipient AS init_id, "
             f"CONCAT(users_init.realname, ' ', users_init.firstname ) AS init_fio, "
             f"init_telegramids.telegramidfield AS init_telegramid, "
             f"executor.users_id AS exec_id, "
             f"CONCAT(users_exec.realname, ' ', users_exec.firstname ) AS exec_fio, "
             f"exec_telegramids.telegramidfield AS exec_telegramid "
             f"FROM glpi_tickets AS ticket "
             f"JOIN glpi_tickets_users AS executor ON ticket.id = executor.tickets_id "
             f"JOIN glpi_users AS users_exec ON users_exec.id = executor.users_id "
             f"JOIN glpi_users AS users_init ON users_init.id = ticket.users_id_recipient "
             f"LEFT JOIN glpi_plugin_fields_usertelegramids AS exec_telegramids  "
             f"ON exec_telegramids.items_id = users_exec.id "
             f"LEFT JOIN glpi_plugin_fields_usertelegramids AS init_telegramids "
             f"ON init_telegramids.items_id = users_init.id "
             f"WHERE ticket.id = {ticket_id} "
             f"AND executor.type = 2")
    logger.info('query_new() is done for ticket_id = %s', ticket_id)
    return query

def query_comment(ticket_id):
    """
    SELECT ticket.id, ticket.name, ticket.content, ticket.date_creation, ticket.status, ticket.urgency,
    ticket.users_id_recipient AS init_id,
    CONCAT(users_init.realname, ' ', users_init.firstname ) AS init_fio,
    init_usertelegramids.telegramidfield AS init_telegramid,
    executor.users_id AS exec_id,
    CONCAT(users_exec.realname, ' ', users_exec.firstname ) AS exec_fio,
    exec_usertelegramids.telegramidfield AS exec_telegramid,
    comments.users_id AS comment_id,
    CONCAT(users_comment.realname, ' ', users_comment.firstname ) AS comment_fio,
    comments.content AS comment_content
    FROM glpi_tickets AS ticket
    JOIN glpi_tickets_users AS executor ON ticket.id = executor.tickets_id
    JOIN glpi_users AS users_exec ON users_exec.id = executor.users_id
    JOIN glpi_users AS users_init ON users_init.id = ticket.users_id_recipient
    JOIN glpi_itilfollowups AS comments ON comments.items_id = ticket.id
    JOIN glpi_users AS users_comment ON users_comment.id = comments.users_id
    LEFT JOIN glpi_plugin_fields_usertelegramids AS exec_usertelegramids ON exec_usertelegramids.items_id = users_exec.id
    LEFT JOIN glpi_plugin_fields_usertelegramids AS init_usertelegramids ON init_usertelegramids.items_id = users_init.id
    WHERE ticket.id = 851 AND executor.type = 2
    ORDER BY comments.date_creation DESC
    LIMIT 1
    """
    query = (f"SELECT ticket.id, ticket.name, ticket.content, ticket.date_creation, ticket.status, ticket.urgency, "
             f"ticket.users_id_recipient AS init_id, "
             f"CONCAT(users_init.realname, ' ', users_init.firstname ) AS init_fio, "
             f"init_usertelegramids.telegramidfield AS init_telegramid, "
             f"executor.users_id AS exec_id, "
             f"CONCAT(users_exec.realname, ' ', users_exec.firstname ) AS exec_fio, "
             f"exec_usertelegramids.telegramidfield AS exec_telegramid, "
             f"comments.users_id AS comment_id,  "
             f"CONCAT(users_comment.realname, ' ', users_comment.firstname ) AS comment_fio, "
             f"comments.content AS comment_content "
             f"FROM glpi_tickets AS ticket "
             f"JOIN glpi_tickets_users AS executor ON ticket.id = executor.tickets_id "
             f"JOIN glpi_users AS users_exec ON users_exec.id = executor.users_id "
             f"JOIN glpi_users AS users_init ON users_init.id = ticket.users_id_recipient "
             f"JOIN glpi_itilfollowups AS comments ON comments.items_id = ticket.id "
             f"JOIN glpi_users AS users_comment ON users_comment.id = comments.users_id "
             f"LEFT JOIN glpi_plugin_fields_usertelegramids AS exec_usertelegramids ON exec_usertelegramids.items_id = users_exec.id "
             f"LEFT JOIN glpi_plugin_fields_usertelegramids AS init_usertelegramids ON init_usertelegramids.items_id = users_init.id "
             f"WHERE ticket.id = {ticket_id} AND executor.type = 2 "
             f"ORDER BY comments.date_creation DESC "
             f"LIMIT 1")
    logger.info('query_comment() is done for ticket_id = %s', ticket_id)
    return query


def query_task(ticket_id):
    """
    SELECT ticket.id, ticket.name, ticket.content, ticket.date_creation,
    ticket.users_id_recipient AS init_id,
    CONCAT(users_init.realname, ' ', users_init.firstname ) AS init_fio,
    executor.users_id AS exec_id,
    CONCAT(users_exec.realname, ' ', users_exec.firstname ) AS exec_fio,
    exec_telegramids.telegramidfield AS exec_telegramid,
    task.content AS task_content, task.state AS task_status, task.users_id AS task_init_id,
    CONCAT(user_task_init.realname, ' ', user_task_init.firstname ) AS task_init_fio,
    task_init_telegramids.telegramidfield AS task_init_telegramid,
    task.users_id_tech AS task_exec_id,
    CONCAT(user_task_exec.realname, ' ', user_task_exec.firstname ) AS task_exec_fio,
    task_exec_telegramids.telegramidfield AS task_exec_telegramid
    FROM glpi_tickets AS ticket
    JOIN glpi_tickets_users AS executor ON ticket.id = executor.tickets_id
    JOIN glpi_users AS users_exec ON users_exec.id = executor.users_id
    JOIN glpi_tickettasks AS task ON task.tickets_id = ticket.id
    JOIN glpi_users AS user_task_exec ON user_task_exec.id = task.users_id_tech
    JOIN glpi_users AS users_init ON users_init.id = ticket.users_id_recipient
    JOIN glpi_users AS user_task_init ON user_task_init.id = task.users_id
    LEFT JOIN glpi_plugin_fields_usertelegramids AS task_exec_telegramids ON task_exec_telegramids.items_id = task.users_id_tech
    LEFT JOIN glpi_plugin_fields_usertelegramids AS task_init_telegramids  ON task_init_telegramids.items_id = users_init.id
    LEFT JOIN glpi_plugin_fields_usertelegramids AS exec_telegramids ON exec_telegramids.items_id = users_exec.id
    WHERE ticket.id = 851 AND executor.type = 2
    ORDER BY task.date DESC
    LIMIT 1
    """
    query = (f"SELECT ticket.id, ticket.name, ticket.content, ticket.date_creation, "
             f"ticket.users_id_recipient AS init_id, "
             f"CONCAT(users_init.realname, ' ', users_init.firstname ) AS init_fio, "
             f"executor.users_id AS exec_id, "
             f"CONCAT(users_exec.realname, ' ', users_exec.firstname ) AS exec_fio, "
             f"exec_telegramids.telegramidfield AS exec_telegramid, "
             f"task.content AS task_content, task.state AS task_status, task.users_id AS task_init_id, "
             f"CONCAT(user_task_init.realname, ' ', user_task_init.firstname ) AS task_init_fio, "
             f"task_init_telegramids.telegramidfield AS task_init_telegramid, "
             f"task.users_id_tech AS task_exec_id, "
             f"CONCAT(user_task_exec.realname, ' ', user_task_exec.firstname ) AS task_exec_fio, "
             f"task_exec_telegramids.telegramidfield AS task_exec_telegramid "
             f"FROM glpi_tickets AS ticket "
             f"JOIN glpi_tickets_users AS executor ON ticket.id = executor.tickets_id "
             f"JOIN glpi_users AS users_exec ON users_exec.id = executor.users_id "
             f"JOIN glpi_tickettasks AS task ON task.tickets_id = ticket.id "
             f"JOIN glpi_users AS user_task_exec ON user_task_exec.id = task.users_id_tech "
             f"JOIN glpi_users AS users_init ON users_init.id = ticket.users_id_recipient "
             f"JOIN glpi_users AS user_task_init ON user_task_init.id = task.users_id "
             f"LEFT JOIN glpi_plugin_fields_usertelegramids AS task_exec_telegramids "
             f"ON task_exec_telegramids.items_id = task.users_id_tech "
             f"LEFT JOIN glpi_plugin_fields_usertelegramids AS task_init_telegramids "
             f"ON task_init_telegramids.items_id = users_init.id "
             f"LEFT JOIN glpi_plugin_fields_usertelegramids AS exec_telegramids "
             f"ON exec_telegramids.items_id = users_exec.id "
             f"WHERE ticket.id = {ticket_id} AND executor.type = 2 "
             f"ORDER BY task.date DESC " 
             f"LIMIT 1")
    logger.info('query_task() is done for ticket_id = %s', ticket_id)
    return query
