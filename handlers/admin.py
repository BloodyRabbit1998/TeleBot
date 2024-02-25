from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
from config import *
import kb,tabulate,database.request as rq
from datetime import datetime,timedelta

router=Router()           

@router.message(Command("start"))
async def start_handler(msg:Message):
    if str(msg.from_user.id) in ADMINS:
        await msg.answer(f"Вы админ",reply_markup=kb.kb_buttons["admin"]) 
    else:
        await msg.answer("""
Вас приветсвует Ланская Алена - лучшый массажер планеты!
Чтобы посмотреть список услуг введите /prices
Чтобы посмотреть время для записи введите /time
Для записи введите /write (дата) (время)   
Для повторного просмотра этого сообщения введите /info или /start               
""",reply_markup=kb.kb_buttons["start"])
        
@router.message(Command('id'))
async def massage_id(msg:Message):
    await msg.answer(f"Ваш ID: {msg.from_user.id}/n {msg}")

@router.message(Command('status'))
async def massage_status(msg:Message):
    if str(msg.from_user.id) in ADMINS:
        await msg.answer(f"Вы админ") 
    else:
        await msg.answer(f"Вы клиент") 

last_command_admin=None

days=["ПН","ВТ","СР","ЧТ","ПТ","СБ","ВС"]

@router.message(F.text=="Настроить неделю приема")
async def admin_time_week(msg:Message):
    if str(msg.from_user.id) in ADMINS:
        global last_command_admin
        last_command_admin="week"
        await msg.answer(f"Укажите дату начала приемов в формате: \n (день начала)-(месяц числом)-(год) (день конца)-(месяц числом)-(год) через пробел ") 
    else:
        await msg.answer(f"У вас нет доступа!") 

@router.message()
@router.message(Command("template"))
async def return_command(msg):
    if str(msg.from_user.id) in ADMINS:  
        global last_command_admin
        global days
        global table
        if last_command_admin=="week":
            date_start, date_finish=msg.text.split()
            date_start=datetime.strptime(date_start,"%d-%m-%Y")
            date_finish=datetime.strptime(date_finish,"%d-%m-%Y")
            table=[]
            i=1
            while date_start<=date_finish:
                date=await rq.return_day(date_start)
                table.append([i,date_start.strftime("%d-%m-%Y"),days[date_start.weekday()],"свободно","","-"] if not date else [i,date.day,days[datetime.strftime(date.day).weekday()],"активен",f"{date.start_time}-{date.finish_time}",""])
                i+=1
                date_start+=timedelta(days=1)
            mess=f"""
Дни для работы. 
{tabulate.tabulate(table, headers=["  №  ","Дата","День недели","Статус","Время",'Наличие приема'],tablefmt="heavy_outline")}
Для назначения активных дней укажите № дня из списка и через пробел время начала и конца приема в формате (часы):(минуты)
Для удаления дня введите 00:00 00:00 или одинаковое время 
для вывода эскиза заполнения введите /template
После завершения настройки введите OK!
"""
            last_command_admin="week_day"
            await msg.answer(mess)

        elif last_command_admin=="week_day":
            if msg.text=="/template":
                mess=""
                for i,_,_,status,time,_ in table:
                    time1,time2=time.split("-") if status!='свободно' else ["00:00","00:00"]
                    time1=datetime.strptime(time1,"%H:%M")
                    time2=datetime.strptime(time2,"%H:%M")
                    mess+=f'{i} {time1.strftime("%H:%M")} {time2.strftime("%H:%M")}\n'
                await msg.answer(mess)
            elif msg.text in ["OK!","ok!",'ok']:
                data=[(day, time.split("-")[0], time.split("-")[1]) for _,day,_,status, time,_ in table if status=="активен"]
                await rq.add("days",data)
                await msg.answer("Сохранено!")
                await msg.answer_sticker(r'CAACAgIAAxkBAAEDubZl2wXOTo-MjdBeswp5dyI1n0VoRAACYQEAAhAabSLviIx9qppNBzQE')
            else:
                for day in msg.text.split("\n"):
                    print(day)
                    i,time1,time2=day.split()
                    i=int(i)-1
                    time1=datetime.strptime(time1,"%H:%M")
                    time2=datetime.strptime(time2,"%H:%M")
                    table[i][3]="активен" if time1!=time2 else 'свободно'
                    table[i][4]=f"{time1.strftime('%H:%M')}-{time2.strftime('%H:%M')}"
                mess=f"""
Дни для работы. 
{tabulate.tabulate(table, headers=["  №  ","Дата","День недели","Статус","Время",'Наличие приема'],tablefmt="heavy_outline")}
Для назначения активных дней укажите № дня из списка и через пробел время начала и конца приема в формате (часы):(минуты)
Для удаления дня введите 00:00 00:00 или одинаковое время 
для вывода эскиза заполнения введите /template
После завершения настройки введите OK!
"""

                await msg.answer(mess)


