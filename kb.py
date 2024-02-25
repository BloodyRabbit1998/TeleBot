from aiogram.types import ( InlineKeyboardButton, 
                            InlineKeyboardMarkup, 
                            KeyboardButton, 
                            ReplyKeyboardMarkup, 
                            ReplyKeyboardRemove)

btns={
    "list_price"    :       KeyboardButton(text="Список услуг 🧾"),
    "info"          :       KeyboardButton(text="Информация ℹ️",),
    "write"         :       KeyboardButton(text="Записаться 📝"),
    "help"          :       KeyboardButton(text="Помощь 🆘"),

}
admin_btn={
    "add_time_week":KeyboardButton(text="Настроить неделю приема")
}
kb_buttons = {
    "start":ReplyKeyboardMarkup(keyboard=[
            [btns["list_price"],btns["info"]],
            [btns['help']]],
            resize_keyboard=True),
    "info":ReplyKeyboardMarkup(keyboard=[
            [btns["list_price"]],[btns["help"]]],
            resize_keyboard=True),
    "prices":ReplyKeyboardMarkup(keyboard=[
            [btns["list_price"],btns["info"]]],
            resize_keyboard=True),
    "admin":ReplyKeyboardMarkup(keyboard=[
            [btns["list_price"],btns["info"]],
            [admin_btn['add_time_week'],]],
            resize_keyboard=True),
}

tree_command={

}