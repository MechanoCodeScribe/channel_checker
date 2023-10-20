from aiogram import Router, types, F
from aiogram.filters import Command
from checker.check import subs_checker, link_force
from templates.welcome import INVITE_TEXT
from filters.chat_types import ChatTypeFilter
from loguru import logger
from schedule.interval_funcs import remind
from filters.warning_flag import Check


router = Router()


@logger.catch()
@router.message(ChatTypeFilter(chat_type=["private"]), Command('start'))
async def start_command(message: types.Message):
    """
        Handle the /start command in private chat.

        Args:
            message (types.Message): The incoming message.

        Returns:
            None
    """

    # это ID приветственного стикера - можно поменять или убрать (всю строку)
    # await message.answer_sticker('CAACAgIAAxkBAAIN0WTuYS7q27mExOdwPZQWa-yl8baZAAJ9DAACyg9ASk_lHJFjepVqMAQ')

    logger.info('new start')
    await subs_checker(message)
    user_id = message.from_user.id
    if user_id not in Check.reminder:
        Check.reminder.add(user_id)
        await remind(message)


@logger.catch()
@router.message(ChatTypeFilter(chat_type=["private"]), (F.text == 'Я ПОДПИСАЛСЯ'))
async def send_confirm(message: types.Message):
    """
        Handle the "Я ПОДПИСАЛСЯ" text command in private chat.

        Args:
            message (types.Message): The incoming message.

        Returns:
            None
    """
    logger.info('pressed confirmation button')
    await subs_checker(message)


@router.message(ChatTypeFilter(chat_type=["private"]), Command('link'))
async def show_link(message: types.Message):
    """
        Handle the /get_link command in private chat.

        Args:
            message (Message): The incoming message.

        Returns:
            None
    """
    await link_force(message)


@router.message(ChatTypeFilter(chat_type=["private"]), Command('share'))
async def share(message: types.Message):
    """
        Handle the /share command in private chat.

        Args:
            message (Message): The incoming message.

        Returns:
            None
    """
    await message.answer(INVITE_TEXT)


@logger.catch()
@router.message(ChatTypeFilter(chat_type=["private"]), (F.text == 'ПРОДОЛЖИТЬ'))
async def send_continue(message: types.Message):
    """
        Handle the 'CONTINUE' button press in a private chat.

        Args:
            message (types.Message): The incoming message.

        Returns:
            None
        """
    logger.info('pressed continue button')
    await subs_checker(message)


@logger.catch()
@router.message(ChatTypeFilter(chat_type=["private"]), F.text)
async def unknown(message: types.Message):
    """
    Handle unknown commands.

    Responds to unknown commands with a message.

    Args:
        message (types.Message): The incoming message object.

    Returns:
        None
    """
    await message.answer(text="Я не знаю такой команды")

