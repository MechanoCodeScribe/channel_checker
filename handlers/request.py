from aiogram import Router, F
from loguru import logger
from templates.target import TARGET
from templates.admins import ADMINS
from templates.invite import INVITE_TEXT
from loader import bot
from checker.check import check_sponsors
from database.db_actions import db_check_user, db_add_user


router = Router()


@logger.catch()
@router.chat_join_request(F.chat.id == int(TARGET[1]))
async def request_yes(chat_join_request):
    """
        Handle chat join request.

        Args:
            chat_join_request (types.ChatJoinRequest): The incoming chat join request.

        Returns:
            None
    """
    print('NEW REQUEST')
    print(chat_join_request)
    user_id = chat_join_request.from_user.id
    if user_id in ADMINS:
        await bot.approve_chat_join_request(TARGET[1], user_id=user_id)
        logger.info('user passed the approve procedure without sponsors check as admin')
        print(f'user {user_id} has passed the approve procedure without sponsors check as admin')
    else:
        to_subscribe = await check_sponsors(user_id)
        if not to_subscribe:
            await bot.approve_chat_join_request(TARGET[1], user_id=user_id)
            logger.info('user has passed the approve procedure')
            logger.info(f'user {user_id} has passed the approve procedure')
            await bot.send_message(user_id, INVITE_TEXT)
            no_id = await db_check_user(user_id)
            if no_id:
                await db_add_user(user_id)
                logger.info('add a new user to db. user has subscribed to all sponsors')
        else:
            logger.info('user has NOT PASSED the approve procedure')
            print(f'user {user_id} has NOT PASSED the approve procedure')





