from datetime import datetime, timedelta
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from templates.target import TARGET
from loader import bot
from loguru import logger


@logger.catch()
async def send_keyboard(to_subscribe):
    """
        Create and return an inline keyboard with buttons for subscribing to sponsor channels.

        Args:
            to_subscribe (list): A list of sponsor channels to subscribe to, each containing channel information.

        Returns:
            InlineKeyboardMarkup: An inline keyboard with buttons for subscribing to sponsor channels.
    """
    buttons = []
    for channel in to_subscribe:
        btn = InlineKeyboardButton(text=channel[0], url=channel[2])
        buttons.append([btn])
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    return kb


@logger.catch()
async def final_keyboard():
    """
        Create and return a final inline keyboard with a link to the target channel.

        Returns:
            InlineKeyboardMarkup: An inline keyboard with a button to navigate to the target channel.
    """

    #  здесь устанавливается срок действия пригласительной ссылки - бот ее сам генерирует
    #  срок действия можно менять
    expire_time = datetime.now() + timedelta(days=1)

    invite_link = await bot.create_chat_invite_link(TARGET[1], expire_date=expire_time, creates_join_request=True)
    invite_url = invite_link.invite_link
    button = InlineKeyboardButton(text="ПЕРЕЙТИ В КАНАЛ", url=invite_url)
    kbf = InlineKeyboardMarkup(inline_keyboard=[[button]])
    logger.info('sending a linc for the target channel')
    return kbf


@logger.catch()
async def confirmed_keyboard() -> ReplyKeyboardMarkup:
    """
        Create and return a reply keyboard with a confirmation button.

        Returns:
            ReplyKeyboardMarkup: A reply keyboard with a button for confirming an action.
    """
    kbi = ReplyKeyboardBuilder()
    kbi.button(text="Я ПОДПИСАЛСЯ")
    kbi.adjust(1)
    return kbi.as_markup(resize_keyboard=True, one_time_keyboard=True)
