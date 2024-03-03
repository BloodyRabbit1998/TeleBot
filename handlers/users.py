from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
import kb,tabulate, database.request as rq
from config import *
router=Router()

last_command_user={}

@router.message(Command('info'))
@router.message(F.text=="Информация ℹ️")   
async def massage_info(msg:Message):
    await msg.answer("""
Список команд:
    Чтобы посмотреть список услуг введите /prices
    Чтобы посмотреть время для записи введите /time
    Для записи введите /write (дата) (время)   
    Для повторного просмотра этого сообщения введите /info или /start               
""",reply_markup=kb.kb_buttons["mess_start"])
    await msg.answer(reply_markup=kb.kb_buttons["info"])
     

@router.message(Command('prices'))
@router.message(F.text=="Список услуг 🧾")
async def massage_price(msg:Message):
    global data
    data=[[i, s.NameServices, f"{s.price} {BANKNOTE[1]}" ] for i, s in enumerate(await rq.return_serveces(), start=1)]
    await msg.answer(f"""
            Доступные услуги:
{tabulate.tabulate(data, headers=["No","Услуга","Цена"])}
        """,reply_markup=kb.kb_buttons["prices"])    
@router.message(F.text=="Записаться 📝")
async def message_time(msg:Message):
    global last_command,data
    if msg.text=="Записаться 📝":
        days=await rq.return_days()
        if days:
            data=[[i, d.day, d.start_time,d.finish_time] for i, d in enumerate(days, start=1)]
            last_command[msg.from_user.id]="days"
            await msg.answer(f"""
{tabulate.tabulate(data, headers=["No", "День", "Начало приема", "Конец приема"])}
Укажите номер дня для получения свободного времени.
Для обнуления информации сново нажмите "Записаться"
                         """, reply_markup=kb.InlineKeyboardMarkup(inline_keyboard=[[kb.btns_inline ["write"],]]))
        else:
            await msg.answer("Дней приема не обнаруженно!")
            await msg.answer_sticker(r'CAACAgIAAxkBAAED3RRl5ExArZDqkMwg2n4xYiLqTLO36wAC1AwAAmSX0Unr2bjSVr0jRTQE')
