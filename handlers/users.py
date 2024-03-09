from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
import kb,tabulate, database.request as rq
from datetime import datetime, timedelta
from aiogram.fsm.context import FSMContext 
from states import Users
from config import *
router=Router()


days=["ПН","ВТ","СР","ЧТ","ПТ","СБ","ВС"]

@router.message(Command('info'))
@router.message(F.text=="Информация ℹ️")   
async def massage_info(msg:Message):
    await msg.answer("""
Список команд:
    Чтобы посмотреть список услуг введите /prices
    Чтобы посмотреть время для записи введите /time
    Для записи введите /write (дата) (время)   
    Для повторного просмотра этого сообщения введите /info или /start               
""",reply_markup=kb.kb_buttons["msg_start"])
    await msg.answer_contact(PHONE,NAME,reply_markup=kb.kb_buttons["info"])
     

@router.message(Command('prices'))
@router.message(F.text=="Список услуг 🧾")
async def massage_price(msg:Message):
    global data
    data=[[i, s.NameServices, f"{s.price} {BANKNOTE[1]}" ] for i, s in enumerate(await rq.return_serveces(), start=1)]
    await msg.answer(f"""
            Доступные услуги:
{tabulate.tabulate(data, headers=["No","Услуга","Цена"])}
        """,reply_markup=kb.kb_buttons["prices"])   
 
@router.message(F.text=="Записаться 📝",)
async def message_time(msg:Message,state:FSMContext):
    global data
    state.clear()
    days=await rq.return_days()
    if days:
        data=[[i, d.day, d.start_time,d.finish_time] for i, d in enumerate(days, start=1)]
        btns=kb.InlineKeyboardMarkup(inline_keyboard=[[kb.InlineKeyboardButton(text=f'{day:%d-%m-%Y} с {start} до {finish}' , callback_data=f'user write {day:%d-%m-%Y}') ]for _,day,start,finish in data])
        state.set_state(Users.choice_day)
        await msg.answer(f"""
{tabulate.tabulate(data, headers=["No", "День", "Начало приема", "Конец приема"])}
Укажите номер дня для получения свободного времени.
Для обнуления информации сново нажмите "Записаться"
                        """, reply_markup=btns)
    else:
        await msg.answer("Дней приема не обнаруженно!")
        await msg.answer_sticker(r'CAACAgIAAxkBAAED3RRl5ExArZDqkMwg2n4xYiLqTLO36wAC1AwAAmSX0Unr2bjSVr0jRTQE')

@router.callback_query(F.data.regexp(r"user write \d{2}-\d{2}-\d{4}$"))
async def write_callback(call:types.CallbackQuery, state:FSMContext):
    global days
    date=call.data.split()[-1]
    date=datetime.strptime(date, "%d-%m-%Y").date()
    day=await rq.return_day(date)
    print("\n"*5,await state.get_state(),"\n"*5)
    if day:
        day=day[-1]
        a=await rq.return_write(day.id)
        a_time=[write.visit_time for write in a]
        start= day.start_time
        data=[]
        while start<day.finish_time:
            if start not in a_time:
                data.append((f"{day.day:%d/%m/%Y}({days[datetime.weekday(day.day)]})\t:\t{start:%H:%M}",f"user time {day.day:%d-%m-%Y} {start:%H:%M}"))
            start=(datetime.strptime(f"{start:%H:%M}","%H:%M")+timedelta(minutes=30)).time()
        state.update_data(choice_day=date)
        state.set_state(Users.choice_time)
        await call.message.answer(f"""
            Выбрано: {date:%d-%m-%Y} ({days[datetime.weekday(date)]})
            Введите время для записи в формате час:минута или выберите предложенное время

""",reply_markup=kb.return_kb(data))   

@router.callback_query(F.data.regexp(r"user time \d{2}-\d{2}-\d{4} [01]\d|2[0-3]:[0-5]\d$"))
async def write_callback(call:types.CallbackQuery,state:FSMContext):
    day,time=call.data.split()[-2:]
    day=await rq.return_day(datetime.strptime(day, "%d-%m-%Y").date())
    if day:
        day=day[-1]
        btns=[(f"{s.id}) {s.NameServices}:\n{s.price} {BANKNOTE[1]}",f"user write {day.day:%d-%m-%Y} {time} id{s.id} ") for s in await rq.return_serveces()]
        btns=kb.return_kb(btns)
        time=datetime.strptime(time, "%H:%M").time()
        state.update_data(choice_time=time)
        state.set_state(Users.choice_service)
        await call.message.answer(f"""Вы хотите записаться на {day.day:%d-%m-%Y} в {time:%H:%M}
Выберите услугу:""",reply_markup=btns)
        
@router.callback_query(F.data.regexp(r"user write \d{2}-\d{2}-\d{4} [01]\d|2[0-3]:[0-5]\d id\d $"))
async def write_callback(call:types.CallbackQuery,state:FSMContext):
    day,time,id_service=call.data.split()[-3:]
    day=datetime.strptime(day, "%d-%m-%Y").date()
    time=datetime.strptime(time, "%H:%M").time()  
    id_service=int(id_service[2:])  
    day=await rq.return_day(day)
    if day:
        day=day[-1]
        state.update_data(choice_service=id_service) 
        await  rq.add("appointments",[(day.id,call.message.from_user.id,time,(datetime.strptime(f"{time:%H:%M}","%H:%M")+timedelta(minutes=30+(time.minute%30))).time(),id_service)])
        state.clear()
        service=await rq.return_serveces(id=id_service)[-1]
        await call.message.answer(f"""Вы записаны на {day.day:%d-%m-%Y} в {time:%H:%M} на услугу:{service.NameServices}
Стоймость услуги:{service.price}""")

@router.message(F.text.regexp(r"\d{2}:\d{2}$"))
async def write_time(msg:Message):
    global last_command
    if last_command[msg.from_user.id]=="time":
        date=datetime.strptime(msg.text,"%H:%M").time()
        day=await rq.return_day(datetime.strptime(msg.text,"%H:%M"))