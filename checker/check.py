from aiogram import types
from loader import bot
from templates.target import TARGET
from templates.sponsors import SPONSORS
from keyboards.subs_keyboard import send_keyboard, confirmed_keyboard, final_keyboard
from database.db_actions import db_check_user, db_add_user
from aiogram.exceptions import TelegramBadRequest
from loguru import logger


@logger.catch()
async def check_target(user_id):
    """
        This function checks if a user is a member, creator, or administrator of the TARGET channel.

        Args:
            user_id: The ID of the user to check.

        Returns:
            bool: True if the user is a member, creator, or administrator of the TARGET channel; False otherwise.
    """
    result = await bot.get_chat_member(chat_id=TARGET[1], user_id=user_id)
    print("checking user's status in TARGET channel. user_id: ", user_id, result.status)
    if str(result.status) == "ChatMemberStatus.MEMBER" or str(result.status) == "ChatMemberStatus.CREATOR" or str(
            result.status) == "ChatMemberStatus.ADMINISTRATOR":
        return True
    else:
        return False


@logger.catch()
async def check_sponsors(user_id):
    """
        This function checks if a user has left or been kicked from any of the SPONSORS channels.

        Args:
            user_id: The ID of the user to check.

        Returns:
            list: A list of SPONSORS channels that the user should subscribe to.
    """
    to_subscribe = []
    for sponsor in SPONSORS:
        try:
            result = await bot.get_chat_member(chat_id=sponsor[1], user_id=user_id)
            print(f"User {user_id} status in sponsor's channel ({sponsor[0]}):", result.status)
            if str(result.status) == "ChatMemberStatus.LEFT" or str(result.status) == "ChatMemberStatus.KICKED":
                to_subscribe.append(sponsor)
        except TelegramBadRequest:
            print('bot has lost admin rights in channel:', sponsor[0])
            logger.error('bot has lost admin rights in one of channels')
            continue
    return to_subscribe


@logger.catch()
async def subs_checker(message: types.Message):
    """
        This function checks if a user is a member of a target channel, and based on that, it provides the appropriate response.

        Args:
            message (types.Message): The message object representing the user's message.

        Returns:
            None
    """
    user_id = message.from_user.id
    result = await check_target(user_id)
    if result:
        await message.answer("Ты уже участник закрытого канала")
        no_id = await db_check_user(user_id)
        if no_id:
            await db_add_user(user_id)
            logger.info('add a new user to db. user already in target channel, but was not in db somehow')
    else:
        to_subscribe = await check_sponsors(user_id)
        if to_subscribe:
            kb = await send_keyboard(to_subscribe)
            kbi = await confirmed_keyboard()
            await message.answer("Каналы для подписки:", reply_markup=kb)
            await message.answer("Для подтверждения нажмите 'Я ПОДПИСАЛСЯ'", reply_markup=kbi)
        else:
            kbf = await final_keyboard()
            await message.answer('Спасибо за подписку на спонсоров!', reply_markup=kbf)
            no_id = await db_check_user(user_id)
            if no_id:
                await db_add_user(user_id)
                logger.info('add a new user to db. user has subscribed to all sponsors')




