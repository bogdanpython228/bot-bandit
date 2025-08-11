from aiogram import F, Router, Bot
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from asyncio import sleep

import app.utils.keyboards as kb
import app.database.requests as rq
from app.core.config import ADMIN


class States(StatesGroup):
    name = State()

router = Router()


@router.message(CommandStart())
async def registration(message: Message, state: FSMContext):
    user = await rq.get_user(message.from_user.id)
    if user:
        await message.answer(f'{user.name}, у тебя на счету ${user.money}', reply_markup=kb.main)
    else:
        await state.set_state(States.name)
        await message.answer('Привет! Для начала тебе нужжно ввести имя своего персонажа!')
    
    
@router.message(States.name)
async def statistics(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()
    
    await rq.add_user(message.from_user.id, data['name'])
    user = await rq.get_user(message.from_user.id)

    await message.answer(f'{user.name}, у тебя на счету ${user.money}', reply_markup=kb.main)
    await state.clear()
    
    
@router.message(F.text == 'работа')
async def job(message: Message):
    user = await rq.get_user(message.from_user.id)
    
    await message.answer(f'{user.name}, выбери работу на которой хочешь работать!', 
                         reply_markup=kb.work)
    
    
@router.message(F.text == 'грузчик')
async def loader(message: Message):
    user = await rq.get_user(message.from_user.id)
    
    await message.answer(f'{user.name}, ты попал на склад, тебе нужно отнести коробку',
                         reply_markup=kb.loader)
    
    
@router.message(F.text == 'отнести')
async def attribute(message: Message):
    await message.answer('ты относишь коробку')
    await sleep(5)
    
    user = await rq.update_money(message.from_user.id, 900)
    await message.answer(f'ты отнес коробку, твой баланс ${user.money}', reply_markup=kb.loader)
    
    
@router.message(F.text == 'таксист')
async def taxi_driver(message: Message):
    user = await rq.get_user(message.from_user.id)
    
    await message.answer(f'{user.name}, ты попал в таксопарк, бери свой заказ.',
                         reply_markup=kb.taxi_driver)
    
    
@router.message(F.text == 'взять заказ')
async def take_the_order(message: Message):
    await message.answer('ожидай заказ')
    await sleep(3)
    
    await message.answer('К тебе подсел молодой парень, '
                         'он просит тебя отвезти в соседний город.\n'
                         'Плата за поездку: $4.500', reply_markup=kb.take)


@router.message(F.text == 'отвезти')
async def take(message: Message):
    await message.answer('вы едете с пассажиром в другой город...')
    await sleep(30)
    
    user = await rq.update_money(message.from_user.id, 4500)
    await message.answer(f'ты отвез пассажира, и получил $4.500\nТвой баланс: {user.money}')
    
    await message.answer(f'{user.name}, ты попал в таксопарк, бери свой заказ.',
                         reply_markup=kb.taxi_driver)


@router.message(F.text == 'отказать')
async def refusal(message: Message):
    user = await rq.get_user(message.from_user.id)
    
    await message.answer(f'{user.name}, ты попал в таксопарк, бери свой заказ.',
                         reply_markup=kb.taxi_driver)

    
@router.message(F.text == 'бизнесы')
async def businesses(message: Message):
    user = await rq.get_user(message.from_user.id)
    if user.business == None: 
        await message.answer(f'{user.name}, у тебя нет бизнеса, но ты можешь его купить в каталоге',
                             reply_markup=kb.catalog)
    else:
        await message.answer_photo(photo=FSInputFile('app/photos/cafe.jpg'),
                                   caption='Твой бизнес: Кафе\n'
                                   f'Продукты бизнеса: {user.business_products}\n'
                                   f'Заказано продуктов: {user.ordered_products}',
                                   reply_markup=kb.business)
      
      
@router.message(F.text == 'Каталог')
async def catalog(message: Message):
    await message.answer_photo(photo=FSInputFile('app/photos/cafe.jpg'),
                               caption='Бизнесы в продаже:\nКафе: $25.000',
                               reply_markup=kb.buy)
   
   
@router.message(F.text == 'Купить')
async def buy(message: Message):
    user = await rq.get_user(message.from_user.id)
    if user.money >= 25000:
        await rq.update_business(message.from_user.id)
        await rq.update_money(message.from_user.id, -25000)
        await message.answer_photo(photo=FSInputFile('app/photos/cafe.jpg'),
                                   caption='Твой бизнес: Кафе\n'
                                   f'Продукты бизнеса: {user.business_products}\n'
                                   f'Заказано продуктов: {user.ordered_products}',
                                   reply_markup=kb.business)
    else:    
        await message.answer('У вас не хватает денег')
        await message.answer(f'{user.name}, у тебя на счету ${user.money}', reply_markup=kb.main)
   
      
@router.message(F.text == 'Склад')
async def warehouse(message: Message):
    user = await rq.get_user(message.from_user.id)
    await message.answer(f'Склад твоего бизнеса\nПродукты на складе: {user.ordered_products}',
                         reply_markup=kb.order)
    
    
@router.message(F.text == 'Продать')
async def sell(message: Message):
    user = await rq.update_money_business(message.from_user.id)
    await message.answer(f'Вы продали продукты! Ваш баланс ${user.money}', reply_markup=kb.main)
    
    
@router.message(F.text == 'заказать')
async def order(message: Message):
    user = await rq.get_user(message.from_user.id)
    if user.ordered_products > 1:
        await message.answer('Вы уже заказывали продукты, или же они у вас есть', reply_markup=kb.main)
    else:
        await message.answer(f'Твой баланс: {user.money}\n'
                            'Размера твоего склада хватает на 20.000 продуктов\n'
                            'Заказать продукты на весь склад $40.000', reply_markup=kb.warehouse)
    
    
@router.message(F.text == 'Заказать')
async def order_to_warehouse(message: Message):
    user = await rq.get_user(message.from_user.id)
    if user.money >= 40000:
        await message.answer('Вы оформили заказ. Ожидайте')
        await sleep(3)
        await rq.update_money(message.from_user.id, -40000)
        await rq.update_ordered_products(message.from_user.id)
        await message.answer(f'{user.name}, у тебя на счету ${user.money-40000}', reply_markup=kb.main)
        minute = 60
        await sleep(minute*3)
        #await rq.update_money(message.from_user.id, 65000)
        await rq.update_business_products(message.from_user.id)
    else:
        await message.answer('У вас не хватает денег на балансе.', reply_markup=kb.main)
        await message.answer_photo(photo=FSInputFile('app/photos/cafe.jpg'),
                                   caption='Твой бизнес: Кафе\n'
                                   f'Продукты бизнеса: {user.business_products}\n'
                                   f'Заказано продуктов: {user.ordered_products}',
                                   reply_markup=kb.business)
      
      
@router.message(F.text == 'топ игроков')
async def statistics_players(message: Message):
    top_players = await rq.top_players()
    
    if not top_players:
        await message.answer('Топ игроков пуст.')
        
    response = 'Топ-5 игроков по балансу:\n\n'
    for i, user in enumerate(top_players, 1):
        response += f'{i}.  {user.name} - ${user.money}\n'
        
    await message.answer(response, reply_markup=kb.main)
      
      
@router.message(Command('bebra'))
async def send_to_all(message: Message, bot: Bot):
    if message.from_user.id == ADMIN:
        if len(message.text.split()) < 2:
            await message.reply('Напишите сообщение после команды:\n/bebra ваш текст')
            return
    
        text_to_send = ' '.join(message.text.split()[1:])
    
        users = await rq.get_all_users()
    
        if not users:
            await message.reply("Нет пользователей для рассылки")
            return
    
        success = 0
        for user in users:
                await bot.send_message(chat_id=user.tg_id, text=text_to_send)
                success += 1
    
        await message.reply(f"✅ Сообщение отправлено {success} пользователям из {len(users)}")
    else:
        await message.answer('Вы не админ.')
      
    
@router.message(F.text == 'нaзaд')
async def back(message: Message):
    user = await rq.get_user(message.from_user.id)
    if user.business == None: 
        await message.answer(f'{user.name}, у тебя нет бизнеса, но ты можешь его купить в каталоге')
    else:
        await message.answer_photo(photo=FSInputFile('app/photos/cafe.jpg'),
                                   caption='Твой бизнес: Кафе\n'
                                   f'Продукты бизнеса: {user.business_products}\n'
                                   f'Заказано продуктов: {user.ordered_products}',
                                   reply_markup=kb.business)
    
    
@router.message(F.text == 'Назад')
async def back(message: Message):
    user = await rq.get_user(message.from_user.id)
    await message.answer(f'Склад твоего бизнеса\nПродукты на складе: {user.business_products}',
                         reply_markup=kb.order)
    
    
@router.message(F.text == 'Нaзaд')
async def back(message: Message):
    user = await rq.get_user(message.from_user.id)
    await message.answer(f'{user.name}, у тебя на счету ${user.money}', reply_markup=kb.main)
    
    
@router.message(F.text == 'назад')
async def back(message: Message):
    user = await rq.get_user(message.from_user.id)
    await message.answer(f'{user.name}, у тебя на счету ${user.money}', reply_markup=kb.main)
    
    
@router.message(F.text)
async def what(message: Message):
    await message.answer('Используй кнопки!')