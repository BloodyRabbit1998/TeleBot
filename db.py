from sqlalchemy import (create_engine, 
                        CheckConstraint,
                        Column, 
                        Integer, 
                        String,
                        Date,
                        Time,
                        ForeignKey)
from sqlalchemy.orm import (DeclarativeBase,
                            sessionmaker)

from datetime import datetime

class Base(DeclarativeBase): pass
  
class Client(Base):
    __tablename__ = "users"
    
    telegram_id = Column(Integer, primary_key=True)
    name = Column(String)

class Days(Base):
    __tablename__ = "days"
    id = Column(Integer, primary_key=True, index=True)
    day = Column(Date,unique=True)
    start_time = Column(Time)
    finish_time = Column(Time)

    __table_args__ = (
        CheckConstraint('start_time< end_time', name='start_before_end'),
    )
class Appointments(Base):
    __tablename__ = "appointments"
  
    id = Column(Integer, primary_key=True, index=True)
    day_id = Column(Integer,ForeignKey("days.id"))
    user_id = Column(Integer,ForeignKey("users.telegram_id"))
    visit_time=Column(Time)
    visit_time=Column(Time)

    __table_args__ = (
        CheckConstraint('visit_time< visit_time', name='start_before_visit'),
    )


engine = create_engine("sqlite:///db.db", echo=True)
Base.metadata.create_all(bind=engine)
print("База данных и таблица созданы")

Session = sessionmaker(autoflush=False, bind=engine) 

def auto_delete_day():
    global Session
    with Session(autoflush=False, bind=engine) as db:   
        days_cols=db.query(Days).filter(Days.day<datetime.now().date).all()
        for d_col in days_cols:
            a_cols=db.query(Appointments).filter(Appointments.day_id==d_col.id).all()
            for a_col in a_cols:
                db.delete(a_col)
            db.delete(d_col)
        db.commit()

def return_day(day):
    global Session
    with Session(autoflush=False, bind=engine) as db:  
        print(day) 
        col=db.query(Days).filter(Days.day==day).first()
    return col
def return_days():
    global Session
    with Session(autoflush=False, bind=engine) as db:   
        cols=db.query(Days).filter(Days.day>=datetime.now().date)
    return cols
def add(table:str,data:list[tuple]):
    global Session
    with Session(autoflush=False, bind=engine) as db:  
        if table=="users":
            cols=[Client(telegram_id=telegram_id,name=name) for telegram_id,name in data ]
        elif table=="days":
            cols=[Days(day=day,start_time=start,finish_time=finish) for day,start,finish in data if return_day(day)]
            update_cols=[]
            for day,start,finish in data:
                col=return_day(day)
                if col:
                    col.start_time=start
                    col.finish_tim=finish
                    update_cols.append(col)
        elif table=="appointments":
            pass 
        db.add_all(cols)
        db.commit()
def return_cols(table:str):
    global Session
    with Session(autoflush=False, bind=engine) as db:   
        pass

if __name__=="__main__":
    pass