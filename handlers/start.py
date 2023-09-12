from aiogram import Router, types, F
from aiogram.filters import Command
from checker.check import subs_checker
from templates.welcome import WELCOME_TEXT
from filters.chat_types import ChatTypeFilter
from loguru import logger


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
    await message.answer_sticker('CAACAgIAAxkBAAIN0WTuYS7q27mExOdwPZQWa-yl8baZAAJ9DAACyg9ASk_lHJFjepVqMAQ')

    await message.answer(WELCOME_TEXT)
    logger.info('new start')
    await subs_checker(message)


@logger.catch()
@router.message(ChatTypeFilter(chat_type=["private"]), (F.text == 'Я ПОДПИСАЛСЯ'))
async def send_random_value(message: types.Message):
    """
        Handle the "Я ПОДПИСАЛСЯ" text command in private chat.

        Args:
            message (types.Message): The incoming message.

        Returns:
            None
    """
    logger.info('pressed confirmation button')
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
