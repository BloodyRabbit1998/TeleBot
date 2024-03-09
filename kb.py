from aiogram.types import ( InlineKeyboardButton, 
                            InlineKeyboardMarkup, 
                            KeyboardButton, 
                            ReplyKeyboardMarkup, 
                            ReplyKeyboardRemove,
                            )
from aiogram.utils.keyboard import InlineKeyboardBuilder,ReplyKeyboardBuilder
btns={
    "list_price"        :           KeyboardButton(text="Список услуг 🧾"),
    "info"              :           KeyboardButton(text="Информация ℹ️",),
    "tableinfo"         :           KeyboardButton(text="Посмотреть раписание🗒️"),
    "help"              :           KeyboardButton(text="Помощь 🆘"),
    "write"             :           KeyboardButton(text="Записаться 📝"),

}
btns_inline={
    "write"             :           InlineKeyboardButton(text="Записаться 📝",callback_data="client write"),
    "list_price"        :           InlineKeyboardButton(text="Список услуг 🧾", callback_data="client list"),
    "сontact"           :           InlineKeyboardButton(text="Связаться 📞", callback_data="client сontact"),
    "tableinfo"         :           InlineKeyboardButton(text="Посмотреть раписание🗒️",callback_data="client listday"),

}
admin_btn={
    "add_time_week":KeyboardButton(text="Настроить неделю приема"),
    "timetable":KeyboardButton(text="Посмотреть сегодняшний день"),
    "timetables":KeyboardButton(text="Посмотреть все приемы"),
    "cancel appointment":KeyboardButton(text="Отменить прием")
}
kb_buttons = {
        "start"         :       ReplyKeyboardMarkup(keyboard=[
                                [btns["list_price"],btns["info"]],
                                [btns['write'],btns["tableinfo" ]],
                                [btns['help']]],
                                resize_keyboard=True),
        "info"          :       ReplyKeyboardMarkup(keyboard=[
                                [btns["list_price"]],
                                [btns['write'],btns["tableinfo" ]],
                                [btns["help"]],],
                                resize_keyboard=True),
        "prices"        :       ReplyKeyboardMarkup(keyboard=[
                                [btns["list_price"],btns["info"]],
                                [btns['write'],btns["tableinfo" ]],],
                                resize_keyboard=True),
        "admin"         :        ReplyKeyboardMarkup(keyboard=[
                                [btns["list_price"],btns["info"]],
                                [admin_btn['timetable'],admin_btn['timetables']],
                                [admin_btn['add_time_week']]],
                                resize_keyboard=True),
        "msg_start"     :       InlineKeyboardMarkup(inline_keyboard=[
                                [btns_inline["list_price"],btns_inline["write"]],
                                [btns_inline["tableinfo"]],
                                [btns_inline["сontact"]],
                                ]),

}
def menu_kb(text:str|list):
    builder=ReplyKeyboardBuilder()
    if isinstance(text,str):
        text=[text]
    for i in text:
        builder.button(text=i)
    builder.adjust([2])
    return builder.as_markup(resize_keyboard=True,one_time_keyboard=True)
    

def return_kb(btns:list[tuple])->InlineKeyboardMarkup:
    kb_buttons=[]
    for text, callback_data in btns:
        kb_buttons.append([InlineKeyboardButton(text=text, callback_data=callback_data)])
    return InlineKeyboardMarkup(inline_keyboard=kb_buttons)