import asyncio
from loguru import logger
from loader import bot
from handlers import start, request
from aiogram import Dispatcher
from database.db_actions import db_start
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from schedule.interval_funcs import interval_func
from utils.set_bot_commands import set_default_commands
from checker import check


@logger.catch()
async def main() -> None:
    """
        The main entry point for the bot's execution.

        This function initializes the dispatcher with memory storage, sets default commands,
        includes routers for different functionalities, deletes any pending webhook updates,
        and starts polling for updates from the bot.

        Returns:
            None
    """

    dp = Dispatcher()
    await set_default_commands()

    dp.include_router(start.router)
    dp.include_router(request.router)
    dp.include_router(check.router)


    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

    #  устанавливается интервал частоты проверки на подписку пользователей из базы данных на каналы спонсоров
    #  интервал можно менять
    scheduler.add_job(interval_func, trigger='interval', minutes=2, args=[bot])
    scheduler.start()

    # Initialize logging for information and errors
    logger.add("info.log", rotation="100 MB", encoding='utf-8', level="INFO")
    logger.add("errors.log", rotation="100 MB", encoding='utf-8', level="ERROR")
    logger.info('Start running')

    await db_start()

    # Delete any pending updates from the webhook
    await bot.delete_webhook(drop_pending_updates=True)

    # Start polling for updates using the dispatcher
    await dp.start_polling(bot)


if __name__ == "__main__":
    # Run the main function using the asyncio event loop
    asyncio.run(main())


