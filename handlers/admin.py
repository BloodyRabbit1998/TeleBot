from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command,CommandStart
from config import *
import kb,tabulate,database.request as rq
from datetime import datetime,timedelta

router=Router()

@router.message(CommandStart())
@router.message(F.text=="start")
async def start_handler(msg:Message):
    await msg.answer_sticker(r"CAACAgQAAxkBAAED3Q1l5EuHETdkCgz_OEPKmjcPJXwyxQACAwYAAgtetBq169NzfwFttTQE",reply_markup=kb.kb_buttons["start"])
    if str(msg.from_user.id) in ADMINS:
        await msg.answer(f"Вы админ",reply_markup=kb.kb_buttons["admin"]) 
        await msg.answer("""
        Доступны следующие команты:
    /start          - запуск бота
    /status         - проверка статуса админа 
    /week           - начать настройка дней приема       
    /services       - начать настройку перечня услуг
    /myday          - посмотреть записи на заданый день
                         """)  
    else:
        await rq.add("users",data=[[msg.from_user.id,str(msg.from_user.first_name)]])
        await msg.answer("""
Вас приветсвует Ланская Алена!
Чтобы посмотреть список услуг введите /prices
Чтобы посмотреть время для записи введите /time
Для записи введите /write (дата) (время)   
Для повторного просмотра этого сообщения введите /info или /start               
""",reply_markup=kb.kb_buttons["msg_start"])
      
@router.message(Command('id'))
@router.message(F.text=="id")
async def massage_id(msg:Message):
    await msg.answer(f"Ваш ID: {msg.from_user.id}/n")

@router.message(Command('status'))
@router.message(F.text=="status")
async def massage_status(msg:Message):
    if str(msg.from_user.id) in ADMINS:
        await msg.answer(f"Вы админ")
        await msg.answer("""
        Доступны следующие команты:
    /start          - запуск бота
    /status         - проверка статуса админа 
    /week           - начать настройка дней приема       
    /services       - начать настройку перечня услуг
    /myday          - посмотреть записи на заданый день
                         """)   
    else:
        await msg.answer(f"Вы клиент") 

last_command_admin=None

days=["ПН","ВТ","СР","ЧТ","ПТ","СБ","ВС"]
@router.message(Command("week"))
@router.message(F.text=="week")
@router.message(F.text=="Настроить неделю приема")
async def admin_time_week(msg:Message):
    if str(msg.from_user.id) in ADMINS:
        global last_command_admin
        last_command_admin="week"
        await msg.answer(f"Укажите дату начала приемов в формате: \n (день начала)-(месяц числом)-(год) (день конца)-(месяц числом)-(год) через пробел ") 
    else:
        await msg.answer(f"У вас нет доступа!") 

@router.message(Command("template"))
async def template_command(msg): 
    global last_command_admin,days,table

    if str(msg.from_user.id) in ADMINS and last_command_admin=="week_day":
        mess=""
        for i,_,_,status,time,_ in table:
            time1,time2=time.split("-") if status!='свободно' else ["00:00","00:00"]
            time1=datetime.strptime(time1,"%H:%M")
            time2=datetime.strptime(time2,"%H:%M")
            mess+=f'{i} {time1.strftime("%H:%M")} {time2.strftime("%H:%M")}\n'
        await msg.answer(mess)
    else:
        await msg.answer(f"У вас нет доступа!") 

@router.message(F.text.in_(["OK!","ok!",'ok',"Save","save"]))  
async def save(msg):
    global last_command_admin,days,table
    if last_command_admin=="week_day" and str(msg.from_user.id) in ADMINS: 
        data=[(day, 
        time.split("-")[0], 
        time.split("-")[1]) 
        for _,day,_,status, time,_ in table  
        if status=="активен" or await rq.return_day(datetime.strptime(day,"%d-%m-%Y").date() )]
        
        await rq.add("days",data)
        await msg.answer("Сохранено!")
        await msg.answer_sticker(r'CAACAgIAAxkBAAEDwRZl3LobBpEP_TR6wZ9ason3Ds5juQACaQADQDHADUw0nE7lxYF2NAQ')
        last_command_admin=None

@router.message(F.text.regexp(r"^\d [01]\d|2[0-3]:[0-5]\d [01]\d|2[0-3]:[0-5]\d$"))
async def admin_time_week_day(msg:Message):
    global last_command_admin
    global days
    global table
    if last_command_admin=="week_day" and str(msg.from_user.id) in ADMINS:
        for day in msg.text.split("\n"):
            i,time1,time2=day.split()
            i=int(i)-1
            date=await rq.return_day(datetime.strptime(table[i][1],'%d-%m-%Y').date())
            time1=datetime.strptime(time1,"%H:%M")
            time2=datetime.strptime(time2,"%H:%M")
            table[i][3]="активен" if time1!=time2 else 'свободно'
            table[i][4]=f"{time1.strftime('%H:%M')}-{time2.strftime('%H:%M')}"
            if date:
                table[i][5]="*" if await rq.return_day_write(date) else "-"
            else:
                table[i][5]=""
        mess=f"""
Дни для работы. 
{tabulate.tabulate(table, headers=["  №  ","Дата","День недели","Статус","Время",'Наличие приема'],tablefmt="heavy_outline")}
Для назначения активных дней укажите № дня из списка и через пробел время начала и конца приема в формате (часы):(минуты)
Для удаления дня введите 00:00 00:00 или одинаковое время 
для вывода эскиза заполнения введите /template
После завершения настройки введите OK!
"""

        await msg.answer(mess)

@router.message(F.text.regexp(r"^\d{2}-\d{2}-\d{4} \d{2}-\d{2}-\d{4}$"))
async def admin_time_week_day(msg:Message):
    global last_command_admin
    global days
    global table
    if last_command_admin=="week" and str(msg.from_user.id) in ADMINS:
        
        date_start, date_finish=msg.text.split()
        date_start=datetime.strptime(date_start,"%d-%m-%Y")
        date_finish=datetime.strptime(date_finish,"%d-%m-%Y")
        table=[]
        i=1
        while date_start<=date_finish:
            date=await rq.return_day(date_start.date())
            if len(date)>0:
                date=date[-1]
                table.append([i,
                                date.day.strftime("%d-%m-%Y"),
                                days[date.day.weekday()],
                                "активен",
                                f"{date.start_time:%H:%M}-{date.finish_time:%H:%M}",
                                "*" if await rq.return_day_write(date) else "-"])
            else:
                table.append([i,
                                date_start.strftime("%d-%m-%Y"),
                                days[date_start.weekday()],
                                "свободно","00:00-00:00","-"])
            i+=1
            date_start+=timedelta(days=1)
        mess=f"""
Дни для работы. 

{tabulate.tabulate(table, headers=["  №  ","Да'та","День недели","Статус","Время",'Наличие приема'],tablefmt="heavy_outline")}
Для назначения активных дней укажите № дня из списка и через пробел время начала и конца приема в формате (часы):(минуты)
Для удаления дня введите 00:00 00:00 или одинаковое время 
для вывода эскиза заполнения введите /template
После завершения настройки введите OK!
"""
        last_command_admin="week_day"
        await msg.answer(mess)





#================USER_COMMANDS=================#
                
