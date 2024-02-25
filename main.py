import asyncio
import logging
import database.models as models
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

import config
from handlers.users import router as r1
from handlers.admin import router as r2
 
async def main():
    await models.create_db()
    bot = Bot(token=config.BOT_TOKEN,parse_mode=ParseMode.HTML)
    dp=Dispatcher(storege=MemoryStorage())
    dp.include_routers(r1,r2)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Программа завершена принудительно!")