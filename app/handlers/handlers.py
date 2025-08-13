from aiogram import F, Router, Bot
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from asyncio import sleep
from random import randint

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
    
    if user.laptop == True:
        await message.answer(f'{user.name}, выбери работу на которой хочешь работать!', 
                             reply_markup=kb.work_laptop)
    else:
        await message.answer(f'{user.name}, выбери работу на которой хочешь работать!', 
                             reply_markup=kb.work)
    
    
@router.message(F.text == '📦 грузчик')
async def loader(message: Message):
    user = await rq.get_user(message.from_user.id)
    
    await message.answer(f'{user.name}, ты попал на склад, тебе нужно отнести коробку\n'
                         'плата за 1 коробку $600-900',
                         reply_markup=kb.loader)
    
    
@router.message(F.text == 'отнести')
async def attribute(message: Message):
    await message.answer('ты относишь коробку')
    await sleep(5)
    
    user = await rq.update_money(message.from_user.id, randint(6, 9)*100)
    await message.answer(f'ты отнес коробку, твой баланс ${user.money}', reply_markup=kb.loader)
    
    
@router.message(F.text == '🚕 таксист')
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

    
@router.message(F.text == '⚡ электрик')
async def electrician(message: Message):
    user = await rq.get_user(message.from_user.id)
    
    await message.answer(f'{user.name}, тебе нужно идти к дому чинить проводку', 
                         reply_markup=kb.electrician)
    
    
@router.message(F.text == 'идти')
async def go(message: Message):
    await message.answer('ты идешь к дому')
    await sleep(5)

    await message.answer('ты дошел до дома, теперь чини проводку', reply_markup=kb.wiring)
    
    
@router.message(F.text == 'чинить')
async def repair(message: Message):
    await message.answer('ты чинишь проводку')
    await sleep(20)
    
    user = await rq.update_money(message.from_user.id, 3000)
    await message.answer(f'ты починил проводку и за это получил $3.000\nТвой баланс: {user.money}')
    await message.answer(f'{user.name}, тебе нужно идти к дому чинить проводку', 
                         reply_markup=kb.electrician)
    
    
@router.message(F.text == '💻 хакер')
async def hacker(message: Message):
    user = await rq.get_user(message.from_user.id)
    await message.answer(f'{user.name}, ты теперь хакер!\n'
                         'твоя цель взламывать банки, криптобиржи корпорации и всякое другое!\n'
                         'твой заработок будет в районе $15.000 - 30.000.\nно есть шанс 20% '
                         'что тебя поймает полиция и выдаст штраф в размере $30.000\n'
                         'ты готов?', reply_markup=kb.hacker)
    
    
@router.message(F.text == 'продолжить')
async def continuee(message: Message):
    await message.answer('идет процесс взлома... (займет 1 минуту)')
    await sleep(10)
    if randint(1, 5) == 1:
        await message.answer('вас поймала полиция!')
        user = await rq.update_money(message.from_user.id, -30000)
        await message.answer(f'увы, взлом не удался и с вас сняли $30.000. ваш баланс ${user.money}')
        await message.answer(f'{user.name}, сделаем взлом еще раз?', reply_markup=kb.hacker)
    else:
        user = await rq.update_money(message.from_user.id, randint(15, 30)*1000)
        await message.answer(f'взлом удался! твой баланс ${user.money}')
        await message.answer(f'{user.name}, сделаем взлом еще раз?', reply_markup=kb.hacker)
    
    
@router.message(F.text == 'бизнес')
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
                               caption='Бизнесы в продаже:\nКафе: $50.000',
                               reply_markup=kb.buy)
   
   
@router.message(F.text == 'Купить')
async def buy(message: Message):
    user = await rq.get_user(message.from_user.id)
    if user.money >= 50000:
        await rq.update_business(message.from_user.id)
        await rq.update_money(message.from_user.id, -50000)
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
        await rq.update_business_products(message.from_user.id)
    else:
        await message.answer('У вас не хватает денег на балансе.', reply_markup=kb.main)
        await message.answer_photo(photo=FSInputFile('app/photos/cafe.jpg'),
                                   caption='Твой бизнес: Кафе\n'
                                   f'Продукты бизнеса: {user.business_products}\n'
                                   f'Заказано продуктов: {user.ordered_products}',
                                   reply_markup=kb.business)
      
      
@router.message(F.text == 'магазин')
async def shop(message: Message):
    user = await rq.get_user(message.from_user.id)
    if user.laptop == True:
        await message.answer('магазин техники пуст!')
        await message.answer(f'{user.name}, у тебя на счету ${user.money}', reply_markup=kb.main)
    else:
        await message.answer('Открылся новый магазин техники!\nНоутбук: $40.000', 
                             reply_markup=kb.buy_laptop)
      
      
@router.message(F.text == 'Kупить')
async def buy_laptop(message: Message):
    user = await rq.get_user(message.from_user.id)
    if user.money >= 40000:
        await rq.update_laptop(message.from_user.id)
        await rq.update_money(message.from_user.id, -40000)
        await message.answer('вы купили нотбук!\n(проверьте список работ!)')
        await message.answer(f'{user.name}, у тебя на счету ${user.money}', reply_markup=kb.main)
    else:    
        await message.answer('У вас не хватает денег')
        await message.answer(f'{user.name}, у тебя на счету ${user.money}', reply_markup=kb.main)
      
      
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
    
    
@router.message(F.text == 'назaд')
async def back(message: Message):
    user = await rq.get_user(message.from_user.id)
    
    await message.answer(f'{user.name}, тебе нужно идти к дому чинить проводку', 
                         reply_markup=kb.electrician)
    
    
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