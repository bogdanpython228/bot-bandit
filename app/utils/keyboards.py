from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Меню
main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='работа')],
    #[KeyboardButton(text='казино')],
    [KeyboardButton(text='бизнес'), KeyboardButton(text='магазин')],
    [KeyboardButton(text='топ игроков')]
],
                           one_time_keyboard=True,
                           resize_keyboard=True)

# Работы
work = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='📦 грузчик')],
    [KeyboardButton(text='⚡ электрик')],
    [KeyboardButton(text='🚕 таксист')],
    [KeyboardButton(text='назад')]
],
                           one_time_keyboard=True,
                           resize_keyboard=True)

work_laptop = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='📦 грузчик')],
    [KeyboardButton(text='⚡ электрик')],
    [KeyboardButton(text='🚕 таксист')],
    [KeyboardButton(text='💻 хакер')],
    [KeyboardButton(text='назад')]
])

# Грузчик
loader = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='отнести')],
    [KeyboardButton(text='назад')]
],
                             one_time_keyboard=True,
                             resize_keyboard=True)

# Таксист
taxi_driver = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='взять заказ')],
    [KeyboardButton(text='назад')]
],
                                  one_time_keyboard=True,
                                  resize_keyboard=True)

# Взятие заказа
take = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='отвезти')],
    [KeyboardButton(text='отказать')]
],
                           one_time_keyboard=True,
                           resize_keyboard=True)

# Электрик
electrician = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='идти')],
    [KeyboardButton(text='назад')]
],
                             one_time_keyboard=True,
                             resize_keyboard=True)     

# Ремонтирование проводки
wiring = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='чинить')],
    [KeyboardButton(text='назад')]
],
                             one_time_keyboard=True,
                             resize_keyboard=True)

hacker = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='продолжить')],
    [KeyboardButton(text='назад')]
],
                             one_time_keyboard=True,
                             resize_keyboard=True)

# Бизнес
business = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='склад')],
    [KeyboardButton(text='продать')],
    [KeyboardButton(text='назад')]
],
                               one_time_keyboard=True,
                               resize_keyboard=True)

# Заказ продуктов
order = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='заказать')],
    [KeyboardButton(text='назад')]
],
                            one_time_keyboard=True,
                            resize_keyboard=True)

# Каталог
catalog = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='каталог')],
    [KeyboardButton(text='назад')]
],
                              one_time_keyboard=True,
                              resize_keyboard=True)

# Купить
buy = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='купить')],
    [KeyboardButton(text='назад')]
],
                          one_time_keyboard=True,
                          resize_keyboard=True)