from aiogram.types import ( InlineKeyboardButton, 
                            InlineKeyboardMarkup, 
                            KeyboardButton, 
                            ReplyKeyboardMarkup, 
                            ReplyKeyboardRemove)

btns={
    "list_price"        :           KeyboardButton(text="Список услуг 🧾"),
    "info"              :           KeyboardButton(text="Информация ℹ️",),
    "tableinfo"         :           KeyboardButton(text="Посмотреть раписание🗒️"),
    "help"              :           KeyboardButton(text="Помощь 🆘"),
    "write"             :           KeyboardButton(text="Записаться 📝"),

}
btns_inline={
    "write"             :           InlineKeyboardButton(text="Записаться 📝",callback_data="Записаться 📝"),
    "list_price"        :           InlineKeyboardButton(text="Список услуг 🧾", callback_data="Список услуг 🧾"),
    "сontact"           :           InlineKeyboardButton(text="Связаться 📞", callback_data="сontact"),
    "tableinfo"         :           InlineKeyboardButton(text="Посмотреть раписание🗒️",callback_data="Посмотреть раписание🗒️"),

}
admin_btn={
    "add_time_week":KeyboardButton(text="Настроить неделю приема"),
    "timetable":KeyboardButton(text="Посмотреть сегодняшний день"),
    "timetables":KeyboardButton(text="Посмотреть все приемы"),
    "cancel appointment":KeyboardButton(text="Отменить прием")
}
kb_buttons = {
        "start"         :        ReplyKeyboardMarkup(keyboard=[
                                [btns["list_price"],btns["info"]],
                                [btns['write'],btns["tableinfo" ]],
                                [btns['help']]],
                                resize_keyboard=True),
        "info"          :         ReplyKeyboardMarkup(keyboard=[
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
