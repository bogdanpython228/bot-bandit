from aiogram import F, Router, Bot
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.exceptions import TelegramForbiddenError
from asyncio import sleep
from random import randint, choice
from datetime import datetime, timedelta

import app.utils.keyboards as kb
import app.database.requests as rq
from app.data.clients import clients
from app.core.config import ADMIN


class States(StatesGroup):
    name = State()
    menu = State()
    job = State()
    loader = State()
    electrician = State()
    wiring_repair = State()
    taxi_driver = State()
    waiting_for_accept = State()
    hacker = State()
    catalog = State()
    buy_business = State()
    business = State()
    business_warehouse = State()
    warehouse = State()
    shop = State()

router = Router()


@router.message(CommandStart())
async def registration(message: Message, state: FSMContext):
    user = await rq.get_user(message.from_user.id)
    if user:
        await state.set_state(States.menu)
        await message.answer(f'{user.name}, у тебя на счету ${user.money}', reply_markup=kb.main)
    else:
        await state.set_state(States.name)
        await message.answer('Привет! Для начала тебе нужжно ввести имя своего персонажа!')
    
    
@router.message(States.name)
async def statistics(message: Message, state: FSMContext):
    name = message.text
    
    await rq.add_user(message.from_user.id, name)
    user = await rq.get_user(message.from_user.id)

    await state.set_state(States.menu)
    await message.answer(f'{user.name}, у тебя на счету ${user.money}', reply_markup=kb.main)

    
@router.message(Command('bebra'))
async def send_to_all(message: Message, bot: Bot):
    if message.from_user.id == ADMIN:
        if len(message.text.split()) < 2:
            await message.reply('напишите сообщение после команды:\n/bebra ваш текст')
            return
    
        text_to_send = ' '.join(message.text.split()[1:])
    
        users = await rq.get_all_users()
    
        if not users:
            await message.reply("нет пользователей для рассылки")
            return
    
        success = 0
        blocked = 0
        
        for user in users:
            try:
                await bot.send_message(chat_id=user.tg_id, text=text_to_send)
                success += 1
            except TelegramForbiddenError:
                await rq.delete_user(user.tg_id)
                blocked += 1
    
        await message.reply(f'✅ сообщение отправлено {success} пользователям из {len(users)}\n'
                            f'заблокировано пользователей: {blocked}')
    else:
        await message.answer('вы не админ.')
    
    
@router.message(States.menu)
async def menu(message: Message, state: FSMContext):
    user = await rq.get_user(message.from_user.id)
    if not user:
        await message.answer('пожалуйста начните с /start')
        return
    
    elif message.text == 'работа':
        if user.laptop == False:
            await state.set_state(States.job)
            await message.answer(f'{user.name}, выбери работу на которой хочешь работать!', 
                                 reply_markup=kb.work)
        else:
            await state.set_state(States.job)
            await message.answer(f'{user.name}, выбери работу на которой хочешь работать!', 
                                 reply_markup=kb.work_laptop)
            
            
    elif message.text == 'бизнес':
        if user.business == None: 
            await state.set_state(States.catalog)
            await message.answer(f'{user.name}, у тебя нет бизнеса, '
                                 'но ты можешь его купить в каталоге',
                                 reply_markup=kb.catalog)
        else:
            await state.set_state(States.business)
            await message.answer_photo(photo=FSInputFile('app/data/cafe.jpg'),
                                       caption='твой бизнес: кафе\n'
                                       f'продукты бизнеса: {user.business_products}\n'
                                       f'заказано продуктов: {user.ordered_products}',
                                       reply_markup=kb.business)
        
        
    elif message.text == 'магазин':
        if user.laptop == False:
            await state.set_state(States.shop)
            await message.answer('открылся новый магазин техники!\nноутбук: $50.000', 
                                 reply_markup=kb.buy)
        else:
            await message.answer('магазин техники пуст!')
            await message.answer(f'{user.name}, у тебя на счету ${user.money}',
                                 reply_markup=kb.main)
            
            
    elif message.text == 'топ игроков':
        top_players = await rq.top_players()
    
        if not top_players:
            await message.answer('топ игроков пуст.')
        
        response = 'топ-10 игроков по балансу:\n\n'
        for i, user in enumerate(top_players, 1):
            response += f'{i}.  {user.name} - ${user.money}\n'
        
        await message.answer(response, reply_markup=kb.main)
        
        
    else:
        await message.answer('используй кнопки!')
    
    
@router.message(States.job)
async def job(message: Message, state: FSMContext):
    user = await rq.get_user(message.from_user.id)
    if not user:
        await message.answer('пожалуйста начните с /start')
        return
    
    if message.text == '📦 грузчик':
        await state.set_state(States.loader)
        await message.answer(f'{user.name}, ты попал на склад, тебе нужно отнести коробку\n'
                             'плата за 1 коробку $600-900',
                             reply_markup=kb.loader)
        
        
    elif message.text == '⚡ электрик':
        await state.set_state(States.electrician)
        await message.answer(f'{user.name}, тебе нужно идти к дому чинить проводку', 
                             reply_markup=kb.electrician)
    
    
    elif message.text == '🚕 таксист':
        await state.set_state(States.taxi_driver)
        await message.answer(f'{user.name}, ты попал в таксопарк, бери свой заказ.',
                             reply_markup=kb.taxi_driver)
        
        
    elif message.text == '💻 хакер':
        await state.set_state(States.hacker)
        await message.answer(f'{user.name}, ты теперь хакер!\n'
                            'твоя цель взламывать банки, криптобиржи корпорации и всякое другое!\n'
                            'твой заработок будет в районе $15.000 - 30.000.\nно есть шанс 20% '
                            'что тебя поймает полиция и выдаст штраф в размере $30.000\n'
                            'ты готов?', reply_markup=kb.hacker)
        
        
    elif message.text == 'назад':
        await state.set_state(States.menu)
        await message.answer(f'{user.name}, у тебя на счету ${user.money}', reply_markup=kb.main)
        
        
    else:
        await message.answer('используй кнопки!')
    
    
@router.message(States.loader)
async def loader(message: Message, state: FSMContext):
    user = await rq.get_user(message.from_user.id)
    if not user:
        await message.answer('пожалуйста начните с /start')
        return
    
    if message.text == 'отнести':
        user_data = await state.get_data()
        last_carry = user_data.get('last_carry_time')
        
        if last_carry and datetime.now() - last_carry < timedelta(seconds=5):
            remaining = 5 - (datetime.now() - last_carry).seconds
            await message.answer(f'подождите {remaining} сек. перед переносом следующей коробки', 
                                 reply_markup=kb.loader)
            return

        await state.update_data(last_carry_time=datetime.now())
        
        await message.answer('ты относишь коробку')
        await sleep(5)
    
        user = await rq.update_money(message.from_user.id, randint(6, 9)*100)
        await message.answer(f'ты отнес коробку, твой баланс ${user.money}',
                             reply_markup=kb.loader)
        
        
    elif message.text == 'назад':
        if user.laptop == False:
            await state.set_state(States.job)
            await message.answer(f'{user.name}, выбери работу на которой хочешь работать!', 
                                 reply_markup=kb.work)
        else:
            await state.set_state(States.job)
            await message.answer(f'{user.name}, выбери работу на которой хочешь работать!', 
                                 reply_markup=kb.work_laptop)

     
    else:
        await message.answer('используй кнопки!')
    
    
@router.message(States.electrician)
async def electrician(message: Message, state: FSMContext):
    user = await rq.get_user(message.from_user.id)
    if not user:
        await message.answer('пожалуйста начните с /start')
        return
    
    if message.text == 'идти':
        await message.answer('ты идешь к дому')
        await sleep(5)

        await state.set_state(States.wiring_repair)
        await message.answer('ты дошел до дома, теперь чини проводку', reply_markup=kb.wiring)
        
            
    elif message.text == 'назад':
        if user.laptop == False:
            await state.set_state(States.job)
            await message.answer(f'{user.name}, выбери работу на которой хочешь работать!', 
                                 reply_markup=kb.work)
        else:
            await state.set_state(States.job)
            await message.answer(f'{user.name}, выбери работу на которой хочешь работать!', 
                                 reply_markup=kb.work_laptop)
            
            
    else:
        await message.answer('используй кнопки!')
        
    
@router.message(States.wiring_repair)
async def wiring_repair(message: Message, state: FSMContext):
    user = await rq.get_user(message.from_user.id)
    if not user:
        await message.answer('пожалуйста начните с /start')
        return
    
    if message.text == 'чинить':
        user_data = await state.get_data()
        last_carry = user_data.get('last_carry_time')
        
        if last_carry and datetime.now() - last_carry < timedelta(seconds=20):
            remaining = 20 - (datetime.now() - last_carry).seconds
            await message.answer(f'подождите {remaining} сек. перед починкой следующей проводкой', 
                                 reply_markup=kb.loader)
            return

        await state.update_data(last_carry_time=datetime.now())
        
        await message.answer('ты чинишь проводку')
        await sleep(20)
    
        user = await rq.update_money(message.from_user.id, 3000)
        await message.answer(f'ты починил проводку и за это получил $3.000\n'
                             f'твой баланс: {user.money}')
        await state.set_state(States.electrician)
        await message.answer(f'{user.name}, тебе нужно идти к дому чинить проводку', 
                             reply_markup=kb.electrician) 
            
    elif message.text == 'назад':
        await state.set_state(States.electrician)
        await message.answer(f'{user.name}, тебе нужно идти к дому чинить проводку', 
                             reply_markup=kb.electrician) 
    
    
    else:
        await message.answer('используй кнопки!')
    
    
@router.message(States.taxi_driver)
async def taxi_driver(message: Message, state: FSMContext):
    user = await rq.get_user(message.from_user.id)
    if not user:
        await message.answer('пожалуйста начните с /start')
        return
    
    if message.text == 'взять заказ':
        await message.answer('ожидай заказ')
        await sleep(3)
    
        client = choice(list(clients.values()))
        await state.update_data(current_client=client)
        await state.set_state(States.waiting_for_accept)
    
        await message.answer(client['description'], reply_markup=kb.take)
    
    
    elif message.text == 'назад':
        if user.laptop == False:
            await state.set_state(States.job)
            await message.answer(f'{user.name}, выбери работу на которой хочешь работать!', 
                                 reply_markup=kb.work)
        else:
            await state.set_state(States.job)
            await message.answer(f'{user.name}, выбери работу на которой хочешь работать!', 
                                 reply_markup=kb.work_laptop)
        
    
    else:
        await message.answer('используй кнопки!')
    
    
@router.message(States.waiting_for_accept)
async def waiting_for_accept(message: Message, state: FSMContext):
    user = await rq.get_user(message.from_user.id)
    if not user:
        await message.answer('пожалуйста начните с /start')
        return
    
    if message.text == 'отвезти':
        data = await state.get_data()
        client = data['current_client']
        
        user_data = await state.get_data()
        last_carry = user_data.get('last_carry_time')
        
        if last_carry and datetime.now() - last_carry < timedelta(seconds=client['time']):
            remaining = client['time'] - (datetime.now() - last_carry).seconds
            await message.answer(f'подождите {remaining} сек. перед следующей поездкой', 
                                 reply_markup=kb.take)
            return

        await state.update_data(last_carry_time=datetime.now())
 
        await message.answer('вы едете с пассажиром...')
        await sleep(client['time'])
 
        user = await rq.update_money(message.from_user.id, client['reward'])
        await message.answer(f'ты отвез пассажира и получил ${client['reward']}\n'
                             f'твой баланс: {user.money}')
        
        await state.set_state(States.taxi_driver)
        await message.answer(f'{user.name}, ты попал в таксопарк, бери свой заказ.',
                             reply_markup=kb.taxi_driver)
 
    
    elif message.text == 'отказать':
        await state.set_state(States.taxi_driver)
        await message.answer(f'{user.name}, ты попал в таксопарк, бери свой заказ.',
                             reply_markup=kb.taxi_driver)
    
    
    else:
        await message.answer('используй кнопки!')
    
    
@router.message(States.hacker)
async def hacker(message: Message, state: FSMContext):
    user = await rq.get_user(message.from_user.id)
    if not user:
        await message.answer('пожалуйста начните с /start')
        return
    
    if message.text == 'продолжить':
        user_data = await state.get_data()
        last_carry = user_data.get('last_carry_time')
        
        if last_carry and datetime.now() - last_carry < timedelta(seconds=60):
            remaining = 60 - (datetime.now() - last_carry).seconds
            await message.answer(f'подождите {remaining} сек. перед следующим взломом', 
                                 reply_markup=kb.hacker)
            return
        
        await state.update_data(last_carry_time=datetime.now())
        
        await message.answer('идет процесс взлома... (займет 1 минуту)')
        await sleep(60)
        if randint(1, 5) == 1:
            await message.answer('вас поймала полиция!')
            user = await rq.update_money(message.from_user.id, -30000)
            await message.answer(f'увы, взлом не удался и с вас сняли $30.000. '
                                 f'ваш баланс ${user.money}')
            await message.answer(f'{user.name}, сделаем взлом еще раз?', reply_markup=kb.hacker)
        else:
            user = await rq.update_money(message.from_user.id, randint(15, 30)*1000)
            await message.answer(f'взлом удался! твой баланс ${user.money}')
            await message.answer(f'{user.name}, сделаем взлом еще раз?', reply_markup=kb.hacker)
    
    
    elif message.text == 'назад':
        if user.laptop == False:
            await state.set_state(States.job)
            await message.answer(f'{user.name}, выбери работу на которой хочешь работать!', 
                                 reply_markup=kb.work)
        else:
            await state.set_state(States.job)
            await message.answer(f'{user.name}, выбери работу на которой хочешь работать!', 
                                 reply_markup=kb.work_laptop)
    
    
    else:
        await message.answer('используй кнопки!')
    
    
@router.message(States.catalog)
async def catalog(message: Message, state: FSMContext):
    user = await rq.get_user(message.from_user.id)
    if not user:
        await message.answer('пожалуйста начните с /start')
        return
    
    if message.text == 'каталог':
        await state.set_state(States.buy_business)
        await message.answer_photo(photo=FSInputFile('app/data/cafe.jpg'),
                                   caption='бизнесы в продаже:\nкафе: $100.000',
                                   reply_markup=kb.buy)
    
    
    elif message.text == 'назад':
        await state.set_state(States.menu)
        await message.answer(f'{user.name}, у тебя на счету ${user.money}', reply_markup=kb.main)
    
    
    else:
        await message.answer('используй кнопки!')
    
    
@router.message(States.buy_business)
async def buy_business(message: Message, state: FSMContext):
    user = await rq.get_user(message.from_user.id)
    if not user:
        await message.answer('пожалуйста начните с /start')
        return
    
    if message.text == 'купить':
        if user.money >= 100000:
            await rq.update_business(message.from_user.id)
            await rq.update_money(message.from_user.id, -100000)
            await message.answer('вы купили бизнес!')
            await state.set_state(States.business)
            await message.answer_photo(photo=FSInputFile('app/data/cafe.jpg'),
                                   caption='твой бизнес: кафе\n'
                                   f'продукты бизнеса: {user.business_products}\n'
                                   f'заказано продуктов: {user.ordered_products}',
                                   reply_markup=kb.business)
        else:    
            await message.answer('у вас не хватает денег')
            await state.set_state(States.menu)
            await message.answer(f'{user.name}, у тебя на счету ${user.money}',
                                 reply_markup=kb.main) 
    
    
    elif message.text == 'назад':
        await state.set_state(States.catalog)
        await message.answer(f'{user.name}, у тебя нет бизнеса, '
                             'но ты можешь его купить в каталоге',
                             reply_markup=kb.catalog)
    
    else:
        await message.answer('используй кнопки!')
    
    
@router.message(States.business)
async def business(message: Message, state: FSMContext):
    user = await rq.get_user(message.from_user.id)
    if not user:
        await message.answer('пожалуйста начните с /start')
        return
    
    if message.text == 'склад':
        await state.set_state(States.business_warehouse)
        await message.answer(f'склад твоего бизнеса\nпродукты на складе: {user.ordered_products}',
                             reply_markup=kb.order)
    
    
    elif message.text == 'продать':
        user = await rq.update_money_business(message.from_user.id)
        await message.answer(f'вы продали продукты! ваш баланс ${user.money}')
        await message.answer_photo(photo=FSInputFile('app/data/cafe.jpg'),
                                   caption='твой бизнес: кафе\n'
                                   f'продукты бизнеса: {user.business_products}\n'
                                   f'заказано продуктов: {user.ordered_products}',
                                   reply_markup=kb.business)
    
    
    elif message.text == 'назад':
        await state.set_state(States.menu)
        await message.answer(f'{user.name}, у тебя на счету ${user.money}', reply_markup=kb.main) 
    
    
    else:
        await message.answer('используй кнопки!')
    
    
@router.message(States.business_warehouse)
async def business_warehouse(message: Message, state: FSMContext):
    user = await rq.get_user(message.from_user.id)
    if not user:
        await message.answer('пожалуйста начните с /start')
        return
    
    if message.text == 'заказать':
        if user.ordered_products > 1:
            await state.set_state(States.menu)
            await message.answer('вы уже заказывали продукты, или же они у вас есть', 
                                 reply_markup=kb.main)
        else:
            await state.set_state(States.warehouse)
            await message.answer(f'твой баланс: {user.money}\n'
                                 'размера твоего склада хватает на 20.000 продуктов\n'
                                 'заказать продукты на весь склад $40.000',
                                 reply_markup=kb.order)
            
            
    elif message.text == 'назад':
        await state.set_state(States.business)
        await message.answer_photo(photo=FSInputFile('app/data/cafe.jpg'),
                                   caption='твой бизнес: кафе\n'
                                   f'продукты бизнеса: {user.business_products}\n'
                                   f'заказано продуктов: {user.ordered_products}',
                                   reply_markup=kb.business)
    
    
    else:
        await message.answer('используй кнопки!')
    
    
@router.message(States.warehouse)
async def warehouse(message: Message, state: FSMContext):
    user = await rq.get_user(message.from_user.id)
    if not user:
        await message.answer('пожалуйста начните с /start')
        return
    
    if message.text == 'заказать':
        if user.money >= 40000:
            await message.answer('вы оформили заказ. Ожидайте')
            await sleep(3)
            await rq.update_money(message.from_user.id, -40000)
            await rq.update_ordered_products(message.from_user.id)
            await state.set_state(States.menu)
            await message.answer('через 10 минут приедут продукты...')
            await message.answer(f'{user.name}, у тебя на счету ${user.money-40000}', 
                                 reply_markup=kb.main)
            minute = 60
            await sleep(minute*10)
            await rq.update_business_products(message.from_user.id)
        else:
            await message.answer('у вас не хватает денег на балансе.')
            await state.set_state(States.business)
            await message.answer_photo(photo=FSInputFile('app/data/cafe.jpg'),
                                       caption='твой бизнес: кафе\n'
                                       f'продукты бизнеса: {user.business_products}\n'
                                       f'заказано продуктов: {user.ordered_products}',
                                       reply_markup=kb.business)
    
    
    elif message.text == 'назад':
        await state.set_state(States.business_warehouse)
        await message.answer(f'склад твоего бизнеса\nпродукты на складе: {user.ordered_products}',
                             reply_markup=kb.order)
    
    
    else:
        await message.answer('используй кнопки!')
    
    
@router.message(States.shop)
async def shop(message: Message, state: FSMContext):
    user = await rq.get_user(message.from_user.id)
    if not user:
        await message.answer('пожалуйста начните с /start')
        return
    
    if message.text == 'купить':
        if user.money >= 50000:
            await rq.update_laptop(message.from_user.id)
            await rq.update_money(message.from_user.id, -50000)
            await message.answer('вы купили ноутбук!\n(проверьте список работ!)')
            await state.set_state(States.menu)
            await message.answer(f'{user.name}, у тебя на счету ${user.money-50000}', 
                                 reply_markup=kb.main)
        else:    
            await message.answer('У вас не хватает денег')
            await state.set_state(States.menu)
            await message.answer(f'{user.name}, у тебя на счету ${user.money}', 
                                 reply_markup=kb.main)
    
    
    elif message.text == 'назад':
        await state.set_state(States.menu)
        await message.answer(f'{user.name}, у тебя на счету ${user.money}', 
                             reply_markup=kb.main)
    
    
    else:
        await message.answer('используй кнопки!')
    
    
@router.message(F.text)
async def what(message: Message):
    await message.answer('используй команду /start чтобы перейти в меню')