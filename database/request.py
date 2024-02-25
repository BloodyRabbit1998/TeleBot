from .models import Client,Days,Appointments,Session
from sqlalchemy import select
from datetime import datetime

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

async def return_day(day:datetime):
    global Session
    async with Session() as db:  
        col=await db.scalars(select(Days).where(Days.day==day))
    for _ in col:
        break
    else:
        col=[]
    return col
def return_days():
    global Session
    with Session() as db: 
        auto_delete_day()  
        cols=db.query(Days).filter(Days.day>=datetime.now().date)
    return cols
async def add(table:str,data:list[tuple]):
    global Session
    async with Session() as db:  
        if table=="users":
            cols=[Client(telegram_id=telegram_id,name=name) for telegram_id,name in data ]
        elif table=="days":
            cols=[Days(day=datetime.strptime(day,"%d-%m-%Y").date,start_time=datetime.strptime(start,"%H:%M").time,finish_time=datetime.strptime(finish,"%H:%M").time) for day,start,finish in data if not await return_day(day)]
            update_cols=[]
            for day,start,finish in data:
                col=await return_day(datetime.strptime(day,"%d-%m-%Y"))
                for c in col:
                    c.start_time=start
                    c.finish_tim=finish
                    update_cols.append(col)
        elif table=="appointments":
            pass 
        db.add_all(cols)
        await db.commit()
def return_cols(table:str):
    global Session
    with Session() as db:   
        pass

if __name__=="__main__":
    with Session() as db:
        print(db.query(Days).all())