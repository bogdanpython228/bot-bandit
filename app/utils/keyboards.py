from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Меню
main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='работа')],
    #[KeyboardButton(text='казино')],
    [KeyboardButton(text='бизнесы')],
    [KeyboardButton(text='топ игроков')]
],
                           one_time_keyboard=True,
                           resize_keyboard=True)

# Работы
work = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='грузчик')],
    [KeyboardButton(text='таксист')],
    [KeyboardButton(text='назад')]
],
                           one_time_keyboard=True,
                           resize_keyboard=True)

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

# Бизнес
business = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Склад')],
    [KeyboardButton(text='Продать')],
    [KeyboardButton(text='Нaзaд')]
],
                               one_time_keyboard=True,
                               resize_keyboard=True)

# Заказ продуктов
order = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='заказать')],
    [KeyboardButton(text='нaзaд')]
],
                            one_time_keyboard=True,
                            resize_keyboard=True)

# Подтверждение заказа продуктов
warehouse = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Заказать')],
    [KeyboardButton(text='Назад')]
],
                                one_time_keyboard=True,
                                resize_keyboard=True)

# Каталог
catalog = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Каталог')],
    [KeyboardButton(text='Нaзaд')]
],
                              one_time_keyboard=True,
                              resize_keyboard=True)

# Купить
buy = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Купить')],
    [KeyboardButton(text='Нaзaд')]
],
                          one_time_keyboard=True,
                          resize_keyboard=True)