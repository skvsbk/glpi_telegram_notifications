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


def run_db_query(query, single=True):
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
        logger.warning('run_db_query() - error')
        logger.warning(e)
    finally:
        logger.info('the run_db_query() is done ')
        connection.close()
    return result


def query_telegramid_for_group(group_id):
    """
    SELECT glpi_plugin_fields_usertelegramids.telegramidfield FROM glpi_groups_users groups_users
    JOIN glpi_plugin_fields_usertelegramids ON glpi_plugin_fields_usertelegramids.items_id = groups_users.users_id
    WHERE groups_users.groups_id = 9
    AND glpi_plugin_fields_usertelegramids.items_id != 84
    """
    query = (f"SELECT glpi_plugin_fields_usertelegramids.telegramidfield FROM glpi_groups_users groups_users "
             f"JOIN glpi_plugin_fields_usertelegramids "
             f"ON glpi_plugin_fields_usertelegramids.items_id = groups_users.users_id "
             f"WHERE groups_users.groups_id = {group_id} "
             f"AND glpi_plugin_fields_usertelegramids.items_id != {Config.NOTYIFY_ALL_OF_USER}")

    logger.info('query_telegramid_for_group() is done for group_id=%s', group_id)
    return query


def query_telegramid_for_all_executors(ticket_id):
    """
    SSELECT items_id AS id, telegramidfield
    FROM glpi_plugin_fields_usertelegramids
    WHERE items_id IN
        (SELECT users_id FROM glpi_tickets_users
        WHERE tickets_id = 919 AND type = 2
        UNION
        SELECT users_id FROM glpi_groups_users
        WHERE groups_id = (SELECT groups_id FROM glpi_groups_tickets
                           WHERE tickets_id = 919 AND type = 2))
    """
    query = (f"SELECT items_id AS id, telegramidfield "
             f"FROM glpi_plugin_fields_usertelegramids "
             f"WHERE items_id IN "
             f"(SELECT users_id FROM glpi_tickets_users "
             f"WHERE tickets_id = {ticket_id} AND type = 2 "
             f"UNION "
             f"SELECT users_id FROM glpi_groups_users "
             f"WHERE groups_id = (SELECT groups_id FROM glpi_groups_tickets "
             f"WHERE tickets_id = {ticket_id} AND type = 2))")
    logger.info('query_telegramid_for_all_executors() is done for ticket_id=%s', ticket_id)
    return query


def query_executors_name(ticket_id):
    """
    SELECT CONCAT(glpi_users.realname, ' ', glpi_users.firstname) as name
    FROM glpi_tickets_users
    JOIN glpi_users ON glpi_users.id = glpi_tickets_users.users_id
    WHERE tickets_id = 919 AND type = 2
    UNION
    SELECT glpi_groups.name as name
    FROM glpi_groups_tickets
    JOIN glpi_groups ON glpi_groups.id = glpi_groups_tickets.groups_id
    WHERE tickets_id = 919 AND type = 2
    """
    query = (f"SELECT CONCAT(glpi_users.realname, ' ', glpi_users.firstname) as name "
             f"FROM glpi_tickets_users "
             f"JOIN glpi_users ON glpi_users.id = glpi_tickets_users.users_id "
             f"WHERE tickets_id = {ticket_id} AND type = 2 "
             f"UNION "
             f"SELECT glpi_groups.name as name "
             f"FROM glpi_groups_tickets "
             f"JOIN glpi_groups ON glpi_groups.id = glpi_groups_tickets.groups_id "
             f"WHERE tickets_id = {ticket_id} AND type = 2")
    logger.info('query_executors_name() is done for ticket_id=%s', ticket_id)
    return query


def query_last_comment(ticket_id):
    """
    SELECT comments.users_id AS comment_id, comments.content AS comment_content,
    CONCAT(glpi_users.realname, ' ', glpi_users.firstname) AS comment_user
    FROM glpi_itilfollowups AS comments
    JOIN glpi_users ON glpi_users.id = comments.users_id
    WHERE comments.items_id = 851
    ORDER BY comments.date_creation DESC
    LIMIT 1
    """
    query = (f"SELECT comments.users_id AS comment_id, comments.content AS comment_content, "
             f"CONCAT(glpi_users.realname, ' ', glpi_users.firstname) AS comment_user "
             f"FROM glpi_itilfollowups AS comments "
             f"JOIN glpi_users ON glpi_users.id = comments.users_id "
             f"WHERE comments.items_id = {ticket_id} "
             f"ORDER BY comments.date_creation DESC "
             f"LIMIT 1")
    logger.info('query_last_comment() is done for ticket_id=%s', ticket_id)
    return query


def query_ticket(ticket_id):
    # users_id_recipient - initiator
    """ New variant
    SELECT ticket.id, ticket.name, ticket.content, ticket.date_creation, ticket.status, ticket.urgency,
    ticket.users_id_recipient AS init_id,
    CONCAT(users_init.realname, ' ', users_init.firstname ) AS init_fio,
    init_telegramids.telegramidfield AS init_telegramid
    FROM glpi_tickets AS ticket
    JOIN glpi_users AS users_init ON users_init.id = ticket.users_id_recipient
    LEFT JOIN glpi_plugin_fields_usertelegramids AS init_telegramids ON init_telegramids.items_id = users_init.id
    WHERE ticket.id = 851
    """

    query = (f"SELECT ticket.id, ticket.name, ticket.content, ticket.date_creation, ticket.status, ticket.urgency, "
             f"ticket.users_id_recipient AS init_id, "
             f"CONCAT(users_init.realname, ' ', users_init.firstname ) AS init_fio, "
             f"init_telegramids.telegramidfield AS init_telegramid "
             f"FROM glpi_tickets AS ticket "
             f"JOIN glpi_users AS users_init ON users_init.id = ticket.users_id_recipient "
             f"LEFT JOIN glpi_plugin_fields_usertelegramids AS init_telegramids "
             f"ON init_telegramids.items_id = users_init.id "
             f"WHERE ticket.id = {ticket_id} ")

    logger.info('query_ticket() is done for ticket_id=%s', ticket_id)
    return query


def query_task_content(ticket_id):
    """
    SELECT task.content AS task_content, task.state AS task_status,
    task.users_id AS task_init_id,CONCAT(user_task_init.realname, ' ', user_task_init.firstname ) AS task_init_fio,
    task_init_telegramids.telegramidfield AS task_init_telegramid,
    task.users_id_tech AS task_exec_id,
    CONCAT(user_task_exec.realname, ' ', user_task_exec.firstname ) AS task_exec_fio,
    task_exec_telegramids.telegramidfield AS task_exec_telegramid
    FROM glpi_tickettasks AS task
    JOIN glpi_users AS user_task_exec ON user_task_exec.id = task.users_id_tech
    JOIN glpi_users AS user_task_init ON user_task_init.id = task.users_id
    LEFT JOIN glpi_plugin_fields_usertelegramids AS task_exec_telegramids
    ON task_exec_telegramids.items_id = task.users_id_tech
    LEFT JOIN glpi_plugin_fields_usertelegramids AS task_init_telegramids
    ON task_init_telegramids.items_id = task.users_id
    WHERE tickets_id = 851
    ORDER BY task.date DESC
    LIMIT 1
    """
    query = (f"SELECT task.content AS task_content, task.state AS task_status, "
             f"task.users_id AS task_init_id, "
             f"task_init_telegramids.telegramidfield AS task_init_telegramid, "
             f"CONCAT(user_task_init.realname, ' ', user_task_init.firstname ) AS task_init_fio, "
             f"task.users_id_tech AS task_exec_id, "
             f"CONCAT(user_task_exec.realname, ' ', user_task_exec.firstname ) AS task_exec_fio, "
             f"task_exec_telegramids.telegramidfield AS task_exec_telegramid "
             f"FROM glpi_tickettasks AS task "
             f"JOIN glpi_users AS user_task_exec ON user_task_exec.id = task.users_id_tech "
             f"JOIN glpi_users AS user_task_init ON user_task_init.id = task.users_id "
             f"LEFT JOIN glpi_plugin_fields_usertelegramids AS task_exec_telegramids "
             f"ON task_exec_telegramids.items_id = task.users_id_tech "
             f"LEFT JOIN glpi_plugin_fields_usertelegramids AS task_init_telegramids "
             f"ON task_init_telegramids.items_id = task.users_id "
             f"WHERE tickets_id = {ticket_id} "
             f"ORDER BY task.date DESC "
             f"LIMIT 1")
    logger.info('query_task_content() is done for ticket_id=%s', ticket_id)
    return query
