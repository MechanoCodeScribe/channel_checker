import sqlite3 as sq
from loguru import logger


@logger.catch()
async def db_start():
    """
        Initialize the database connection and create a table if it doesn't exist.

        Args:
            None

        Returns:
            None
    """
    global db, cur
    db = sq.connect('user_base.db')
    cur = db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS profile(user_id)")
    db.commit()
    logger.info('connected to database')


@logger.catch()
async def db_check_user(user_id):
    """
        Check if a user with the given user_id exists in the database.

        Args:
            user_id (int): The user ID to check.

        Returns:
            bool: True if the user does not exist in the database, False otherwise.
        """
    global db, cur

    db = sq.connect('user_base.db')
    cur = db.cursor()

    cur.execute("SELECT * FROM profile WHERE user_id = ?", (user_id,))
    user_data = cur.fetchone()

    # Если пользователь не найден, добавляем его и возвращаем True
    if user_data is None:
        return True
    else:
        return False


@logger.catch()
async def db_add_user(user_id):
    """
        Add a new user with the given user_id to the database.

        Args:
            user_id (int): The user ID to add to the database.
    """
    global db, cur

    db = sq.connect('user_base.db')
    cur = db.cursor()

    # Добавляем пользователя в базу данных
    cur.execute("INSERT INTO profile(user_id) VALUES (?)", (user_id,))
    db.commit()


@logger.catch()
async def db_remove_user(user_id):
    """
        Remove a user with the given user_id from the database.

        Args:
            user_id (int): The user ID to remove from the database.
    """
    db = sq.connect('user_base.db')
    cur = db.cursor()

    # Удаляем пользователя из базы данных
    cur.execute("DELETE FROM profile WHERE user_id = ?", (user_id,))
    db.commit()


@logger.catch()
async def db_get_users():
    """
        Retrieve a list of all user IDs from the database.

        Returns:
            list: A list of user IDs stored in the database.
    """
    global db, cur
    db = sq.connect('user_base.db')
    cur = db.cursor()

    # вытаскиваем список всех пользователей из базы данных
    cur.execute("SELECT user_id FROM profile")
    user_ids = cur.fetchall()
    db.close()
    logger.info('extracting all users from db for the regular check')
    print('list of users in database:', user_ids)
    return user_ids
