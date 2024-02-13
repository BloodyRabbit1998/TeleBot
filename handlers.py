from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
from config import *
#import kb

router=Router()

@router.message(Command("start"))
async def start_handler(msg:Message):
    await msg.answer("""
    Вас приветсвует Ланская Алена - лучшый массажер планеты!
    Чтобы посмотреть список услуг введите /prices
    Чтобы посмотреть время для записи введите /time
    Для записи введите /write (дата) (время)   
    Для повторного просмотра этого сообщения введите /info или /start               
""")
    
@router.message(Command('info'))
async def massage_info(msg:Message):
     await msg.answer("""
Список команд:
    Чтобы посмотреть список услуг введите /prices
    Чтобы посмотреть время для записи введите /time
    Для записи введите /write (дата) (время)   
    Для повторного просмотра этого сообщения введите /info или /start               
""")

@router.message(Command('prices'))
async def massage_price(msg:Message):
    mess=""
    for i,service in enumerate(PRICES):
        mess+=f"{i+1}\t{service}:\t{PRICES[service]} {BANKNOTE[1]}\n"
    await msg.answer(f"""
            Доступные услуги:
{mess}       
""")


@router.message(Command('id'))
async def massage_id(msg:Message):
    await msg.answer(f"Ваш ID: {msg.from_user.id}")

@router.message(Command('status'))
async def massage_status(msg:Message):
    if str(msg.from_user.id) in ADMINS:
        await msg.answer(f"Вы админ") 
    else:
        await msg.answer(f"Вы клиент") 



