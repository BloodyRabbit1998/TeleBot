from aiogram.types import ( InlineKeyboardButton, 
                            InlineKeyboardMarkup, 
                            KeyboardButton, 
                            ReplyKeyboardMarkup, 
                            ReplyKeyboardRemove)

btns={
    "list_price":KeyboardButton(text="📝 Список услуг", callback_data="prices"),
    "info":KeyboardButton(text="ℹ️ Информация", callback_data="info"),
    "write":KeyboardButton(text="🗓 Записаться", callback_data="write_user"),
    "help":KeyboardButton(text="🔎 Помощь", callback_data="help")
    
}

kb_buttons = {
    "start":ReplyKeyboardMarkup(keyboard=[
            [btns["list_price"],btns["info"]],btns["help"]],
            resize_keyboard=True),
    "info":ReplyKeyboardMarkup(keyboard=[
            btns["list_price"],btns["help"]],
            resize_keyboard=True),
    "prices":ReplyKeyboardMarkup(keyboard=[
            [btns["list_price"],btns["info"]],btns["help"]],
            resize_keyboard=True),
    "admin":[],
}