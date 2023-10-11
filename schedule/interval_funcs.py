from database.db_actions import db_get_users, db_remove_user
from checker.check import check_target, check_sponsors
from datetime import datetime, timedelta
from keyboards.subs_keyboard import subs_choice_remind, subs_choice, continue_keyboard
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loader import bot
from templates.target import TARGET
from aiogram.exceptions import TelegramForbiddenError
from loguru import logger
from templates.admins import ADMINS


@logger.catch()
async def interval_func(bot):
    """
        Check user subscriptions at specified intervals and send warnings.

        Args:
            bot (Bot): The Telegram Bot instance.

        Returns:
            None
    """
    user_ids = await db_get_users()
    if user_ids:
        for user_id in user_ids:
            user_id = user_id[0]
            try:
                print('Checking id: ---------------------', user_id)
                result = await check_target(user_id)
                if result:
                    to_subscribe = await check_sponsors(user_id)
                    if to_subscribe and user_id not in ADMINS:
                        await warning_msg(bot, user_id, to_subscribe)
                    elif to_subscribe:
                        print(f'user {user_id} is admin and will not be deleted')
                elif result == False:
                    print(f'deleting user from db. User {user_id} has left the target channel')
                    await db_remove_user(user_id)
                else:
                    logger.error('check_target function returned None - check internet connection')
                    continue
            except:
                logger.error('unknown error when checking if user is in the target channel')
                logger.error(f'unknown error when checking if user {user_id} is in the target channel')
                continue
    else:
        logger.info('database is empty')


@logger.catch()
async def warning_msg(bot, user_id):
    """
        Send a warning message to a user with a keyboard to renew subscriptions.

        Args:
            bot (Bot): The Telegram Bot instance.
            user_id (int): The user's Telegram ID.

        Returns:
            None
    """
    try:
        key = await subs_choice_remind()
        await bot.send_message(user_id, 'Чтобы остаться в лектории, нужно возобновить\nподписки на лекторов. Если этого не сделать, то\nчерез 10 минут канал лектория станет недоступен\n\nВыбери способ подписки:', reply_markup=key)
        scheduler = AsyncIOScheduler()

        #  здесь устанавливается время, через которое юзера удалят, если он не возобновить подписку на каналы спонсоров
        scheduler.add_job(check_and_kick, trigger='date', run_date=datetime.now() + timedelta(seconds=600), args=[user_id])

        scheduler.start()
        logger.info('warning message will be sent')

    except TelegramForbiddenError:
        logger.error('the bot is blocked by user. User will be deleted from database')
        logger.info('the bot is blocked by user. User will be deleted from database')
        print(f'the bot is blocked by user {user_id}. User will be deleted from database')
        await db_remove_user(user_id)
        await bot.ban_chat_member(chat_id=TARGET[1], user_id=user_id)
        await bot.unban_chat_member(chat_id=TARGET[1], user_id=user_id)


@logger.catch()
async def check_and_kick(user_id):
    """
        Check if a user has resumed subscriptions after a warning message.
        If not, kick the user from the target channel and remove them from the database.

        Args:
            user_id (int): The user's Telegram ID.

        Returns:
            None
    """
    result = await check_target(user_id)
    if result:
        try:
            to_subscribe = await check_sponsors(user_id)
            if to_subscribe:
                logger.info('kicking user and deleting from db. User has not resume subscriptions after warning')
                print(f'_______KICKING USER {user_id}________')
                await bot.ban_chat_member(chat_id=TARGET[1], user_id=user_id)
                await bot.unban_chat_member(chat_id=TARGET[1], user_id=user_id)
                await db_remove_user(user_id)
                try:
                    key = await subs_choice()
                    await bot.send_message(user_id, 'Пришлось ограничить доступ к каналу лектория из-за того, что ты не подписан на всех лекторов. Если хочешь вернуться, выбери способ подписки:', reply_markup=key)
                except TelegramForbiddenError:
                    logger.error('the bot is blocked by user. User will be deleted from database')
                    logger.info('the bot is blocked by user. User will be deleted from database')
            else:
                logger.info('user has resumed subscriptions')
                print(f'________USER {user_id} WILL STAY________')
        except TelegramForbiddenError:
            pass
    elif result == False:
        logger.info('user has left target channel after warning. Deleting user for db ')
        await db_remove_user(user_id)
    else:
        logger.error('check_target function returned None - check internet connection')
        pass


@logger.catch()
async def remind(message):
    """
        Schedule a reminder to send a check message.

        Args:
            message (types.Message): The incoming message.

        Returns:
            None
    """
    now = datetime.now()
    desired_time = datetime(now.year, now.month, now.day, 19)
    if now >= desired_time:
        desired_time += timedelta(days=1)
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(send_remind_check, trigger='date', run_date=desired_time, args=[message])
    scheduler.start()


@logger.catch()
async def send_remind_check(message):
    """
        Send a reminder check message to the user.

        Args:
            message (types.Message): The incoming message.

        Returns:
            None
    """
    user_id = message.from_user.id
    result = await check_target(user_id)
    if not result and user_id not in ADMINS:
        try:
            key = await continue_keyboard()
            await message.answer("Заметил, что ты так и не попал в канал лектория.\nХочешь продолжить?", reply_markup=key)
        except TelegramForbiddenError:
            logger.error('the bot is blocked by user. Remind message was not sent')
            print(f'the bot is blocked by user {user_id}. Remind message was not sent')






