from .models import Client,Days,Appointments,Session
from sqlalchemy import select
from datetime import datetime

def f_date(date:str):
    return datetime.strptime(date,"%d-%m-%Y")
def f_time(time:str):
    
    return datetime.strptime(time,"%H:%M")
def auto_delete_day():
    global Session
    with Session() as db:   
        days_cols=db.query(Days).filter(Days.day<datetime.now().date).all()
        for d_col in days_cols:
            a_cols=db.query(Appointments).filter(Appointments.day_id==d_col.id).all()
            for a_col in a_cols:
                db.delete(a_col)
            db.delete(d_col)
        db.commit()
async def return_write(id:int):
    global Session
    async with Session() as db: 
        stmt=select(Appointments).where(Appointments.day_id==id)
        cols=await db.scalars(stmt)
    return [col for col in cols]
async def return_day_write(day:Days):
    return bool(await return_write(day.id))
async def user_return(id:int):
    global Session
    async with Session() as db:
        stmt=select(Client).where(Client.telegram_id==id)
        cols=await db.scalars(stmt)
    return [col for col in cols]

async def return_day(day:datetime.date):
    global Session
    async with Session() as db: 
        stmt=select(Days).where(Days.day==day)
        cols=await db.scalars(stmt)
    return [col for col in cols]

async def add(table:str,data:list[tuple]):
    global Session
    async with Session() as db:  
        if table=="users":
            user=await user_return(data[0][0])
            if not user:
                cols=[Client(telegram_id=telegram_id,name=name) for telegram_id,name in data ]
            else:
                user=user[-1]
                user.name=data[0][1]
        elif table=="days":
            cols=[]
            for day,start,finish in data:
                date=await return_day(f_date(day).date())
                if date:
                    for col in date:
                        print(start==finish)
                        if start!=finish:
                            col.start_time=start
                            col.finish_tim=finish
                        else:
                            await db.delete(col)
                else:
                    cols.append(Days(day=f_date(day).date(),
                        start_time=f_time(start).time(),
                        finish_time=f_time(finish).time()))
        elif table=="appointments":
            pass 
        db.add_all(cols)
        await db.commit()


if __name__=="__main__":
    with Session() as db:
        print(db.query(Days).all())