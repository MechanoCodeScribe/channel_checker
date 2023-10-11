from aiogram import types, F, Router
from loader import bot
from templates.target import TARGET
from templates.sponsors import SPONSORS
from templates.welcome import WELCOME_TEXT
from keyboards.subs_keyboard import send_keyboard, confirmed_keyboard, final_keyboard, subs_choice, mass_keyboard
from database.db_actions import db_check_user, db_add_user
from aiogram.exceptions import TelegramBadRequest
from loguru import logger


router = Router()


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
        print('Пользователь уже участник закрытого канала')
        no_id = await db_check_user(user_id)
        if no_id:
            await db_add_user(user_id)
            logger.info('add a new user to db. user already in target channel, but was not in db somehow')
    else:
        to_subscribe = await check_sponsors(user_id)
        if to_subscribe:
            await message.answer(WELCOME_TEXT)
            key = await subs_choice()
            await message.answer("Выбери способ подписки:", reply_markup=key)
        else:
            kbf = await final_keyboard()
            await message.answer('Спасибо за подписку!\nПереходи в канал лектория и слушай лекции.', reply_markup=kbf)


@logger.catch()
@router.callback_query(F.data == "manual_subscribe")
async def link_request(callback: types.CallbackQuery):
    id = callback.message.chat.id
    """
        Handle the link request.

        Args:
            message (types.Message): The incoming message.

        Returns:
            None
            :param callback:
            :param CallbackQuery:
    """
    to_subscribe = await check_sponsors(id)
    if to_subscribe:

        kb = await send_keyboard(to_subscribe)
        kbi = await confirmed_keyboard()
        await bot.send_message(id, "Каналы для подписки:", reply_markup=kb)
        await bot.send_message(id, "Для подтверждения нажми 'Я ПОДПИСАЛСЯ'", reply_markup=kbi)
    else:
        kbf = await final_keyboard()
        await bot.send_message(id, 'Спасибо за подписку!\nПереходи в канал лектория и слушай лекции.', reply_markup=kbf)


@logger.catch()
@router.callback_query(F.data == "mass_subscribe")
async def mass_link_request(callback: types.CallbackQuery):
    """
        Handle the mass subscribe request.

        Args:
            callback (types.CallbackQuery): The incoming callback query.

        Returns:
            None
    """
    user_id = callback.message.chat.id
    kb = await mass_keyboard()
    kbi = await confirmed_keyboard()
    await bot.send_message(user_id, "Папка для добавления", reply_markup=kb)
    await bot.send_message(user_id, "Для подтверждения нажми 'Я ПОДПИСАЛСЯ'", reply_markup=kbi)


@router.callback_query(F.data == "manual_subscribe_rem")
async def manual_request(callback: types.CallbackQuery):
    """
        Handle the manual subscribe request for a reminder.

        Args:
            callback (types.CallbackQuery): The incoming callback query.

        Returns:
            None
    """
    id = callback.message.chat.id

    to_subscribe = await check_sponsors(id)
    if to_subscribe:
        kb = await send_keyboard(to_subscribe)
        await bot.send_message(id, "Каналы для подписки:", reply_markup=kb)
    else:
        kbf = await final_keyboard()
        await bot.send_message(id, 'Спасибо за подписку!\nПереходи в канал лектория и слушай лекции.', reply_markup=kbf)


@logger.catch()
@router.callback_query(F.data == "mass_subscribe_rem")
async def mass_request(callback: types.CallbackQuery):
    """
        Handle the mass subscribe request for a reminder.

        Args:
            callback (types.CallbackQuery): The incoming callback query.

        Returns:
            None
    """
    id = callback.message.chat.id
    kb = await mass_keyboard()
    await bot.send_message(id, "Папка для добавления", reply_markup=kb)


@logger.catch()
async def link_force(message):
    """
        Handle the link request by command.

        Args:
            message (types.Message): The incoming message.

        Returns:
            None
    """
    to_subscribe = await check_sponsors(message.from_user.id)
    if to_subscribe:

        kb = await send_keyboard(to_subscribe)
        kbi = await confirmed_keyboard()
        await message.answer("Каналы для подписки:", reply_markup=kb)
        await message.answer("Для подтверждения нажми 'Я ПОДПИСАЛСЯ'", reply_markup=kbi)
    else:
        kbf = await final_keyboard()
        await message.answer('Спасибо за подписку!\nПереходи в канал лектория и слушай лекции.', reply_markup=kbf)





