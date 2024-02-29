from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
import kb,tabulate, database.request as rq
from config import *
router=Router()

@router.message(F.text=="Информация ℹ️")   
@router.message(Command('info'))
async def massage_info(msg:Message):
     await msg.answer("""
Список команд:
    Чтобы посмотреть список услуг введите /prices
    Чтобы посмотреть время для записи введите /time
    Для записи введите /write (дата) (время)   
    Для повторного просмотра этого сообщения введите /info или /start               
""",reply_markup=kb.kb_buttons["info"])
     
@router.message(F.text=="Список услуг 🧾")
@router.message(Command('prices'))
async def massage_price(msg:Message):
    mess=""
    for i,service in enumerate(PRICES):
        mess+=f"{i+1}    {service}:    {PRICES[service]} {BANKNOTE[1]}\n"
    await msg.answer(f"""
            Доступные услуги:
{mess}       
""")

@router.message(F.text=="Записаться 📝")
async def message_time(msg:Message):
    pass

last_command_admin=None

