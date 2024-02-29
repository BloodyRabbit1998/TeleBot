from sqlalchemy import (Table,
                        Column,
                        CheckConstraint,
                        String,
                        Date,
                        Time,
                        Integer,
                        BigInteger,
                        ForeignKey)
from sqlalchemy.orm import (DeclarativeBase,
                            Mapped,
                            mapped_column,
                            relationship)
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine 
from config import URL_SQL
class Base(AsyncAttrs,DeclarativeBase): pass
 


appointment_services_association = Table(
    'appointment_services', Base.metadata,
    Column('appointment_id', Integer, ForeignKey('appointments.id')),
    Column('service_id', Integer, ForeignKey('services.id'))
)
class Client(Base):
    __tablename__ = "users"
    
    telegram_id:Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name:Mapped[str] = mapped_column(String)

class ListServices(Base):
    __tablename__="services"

    id:Mapped[int]= mapped_column(primary_key=True, index=True)
    NameServices:Mapped[str] =mapped_column(String,unique=True)
    price:Mapped[int]=mapped_column(Integer)

class Days(Base):
    __tablename__ = "days"
    id:Mapped[int] = mapped_column(primary_key=True, index=True)
    day:Mapped[Date] = mapped_column(Date,unique=True)
    start_time:Mapped[Time] = mapped_column(Time)
    finish_time:Mapped[Time] = mapped_column(Time)

    __table_args__ = (
        CheckConstraint('start_time< finish_time', name='start_before_end'),
    )
class Appointments(Base):
    __tablename__ = "appointments"
  
    id:Mapped[int] = mapped_column(primary_key=True, index=True)
    day_id:Mapped[int] = mapped_column(ForeignKey("days.id"))
    user_id:Mapped[int] = mapped_column(ForeignKey("users.telegram_id"))
    visit_time:Mapped[Time]=mapped_column(Time)
    exit_time:Mapped[Time]=mapped_column(Time)
    services=relationship("Services", secondary=appointment_services_association)

    __table_args__ = (
        CheckConstraint('visit_time<exit_time', name='start_before_visit'),
    )


engine = create_async_engine(URL_SQL, echo=True)
Session = async_sessionmaker(engine) 


async def create_db():
    async with engine.begin() as conn:
#        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

