from aiogram.types import ( InlineKeyboardButton, 
                            InlineKeyboardMarkup, 
                            KeyboardButton, 
                            ReplyKeyboardMarkup, 
                            ReplyKeyboardRemove)

btns={
    "list_price"    :       KeyboardButton(text="Список услуг 🧾"),
    "info"          :       KeyboardButton(text="Информация ℹ️",),
    "write"         :       KeyboardButton(text="Записаться 📝"),
    "tableinfo"     :       KeyboardButton(text="Посмотреть раписание🗒️"),
    "help"          :       KeyboardButton(text="Помощь 🆘"),

}
admin_btn={
    "add_time_week":KeyboardButton(text="Настроить неделю приема"),
    "timetable":KeyboardButton(text="Посмотреть сегодняшний день"),
    "timetables":KeyboardButton(text="Посмотреть все приемы"),
    "cancel appointment":KeyboardButton(text="Отменить прием")
}
kb_buttons = {
    "start":ReplyKeyboardMarkup(keyboard=[
            [btns["list_price"],btns["info"]],
            [btns['write'],btns["tableinfo" ]],
            [btns['help']]],
            resize_keyboard=True),
    "info":ReplyKeyboardMarkup(keyboard=[
            [btns["list_price"]],[btns["help"]],
            [btns['write'],btns["tableinfo" ]],],
            resize_keyboard=True),
    "prices":ReplyKeyboardMarkup(keyboard=[
            [btns["list_price"],btns["info"]],
            [btns['write'],btns["tableinfo" ]],],
            resize_keyboard=True),
    "admin":ReplyKeyboardMarkup(keyboard=[
            [btns["list_price"],btns["info"]],
            [admin_btn['timetable'],admin_btn['timetables']],
            [admin_btn['add_time_week']]],
            resize_keyboard=True),
}
