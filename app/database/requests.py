from sqlalchemy import select, desc
from app.database.models import async_session
from app.database.models import User


async def add_user(tg_id: int, name: str):
    '''Добавляет пользователя в БД.
    
    Args:
        tg_id: телеграм ID пользователя
        name: имя пользователя
        
    Returns:
        True если все прошло успешно, user если такой пользователь есть в БД
    '''
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        
        if user:
            return user

        session.add(User(tg_id=tg_id, name=name, money=0, business=None))
        await session.commit()
        return True
    
    
async def get_user(tg_id: int):
    '''Получает данные пользователя.
    
    Args:
        tg_id: телеграм ID пользователя
        
    Returns:
        user если все прошло успешно, False если такого пользователя нет
    '''
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        
        if not user:
            return False
        
        return user
    
    
async def update_money(tg_id: int, new_money: int):
    '''Изменяет баланс пользователя.
    
    Args:
        tg_id: телеграм ID пользователя
        new_money: то, на сколько изменится баланс
        
    Returns:
        user если все прошло успешно, False если такого пользователя нет
    '''
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        
        if not user:
            return False
        
        user.money += new_money
        await session.commit()
        await session.refresh(user)
        return user
    
    
async def update_ordered_products(tg_id: int):
    '''Обновляет кол-во заказанных продуктов.
    
    Args:
        tg_id: телеграм ID пользователя
        
    Returns:
        user если все прошло успешно, False если такого пользователя нет
    '''
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        
        if not user:
            return False
        
        user.ordered_products = 20000
        await session.commit()
        await session.refresh(user)
        return user
    
    
async def update_business_products(tg_id: int):
    '''Прибавляет к кол-ву продуктов бизнеса заказанные продукты.
    
    Args:
        tg_id: телеграм ID пользователя
        
    Returns:
        user если все прошло успешно, False если такого пользователя нет
    '''
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        
        if not user:
            return False
        
        user.business_products += user.ordered_products
        user.ordered_products = 0
        await session.commit()
        await session.refresh(user)
        return user
    
    
async def update_money_business(tg_id: int):
    '''Продает продукты бизнеса и начисляет деньги в баланс пользователя.
    
    Args:
        tg_id: телеграм ID пользователя
        
    Returns:
        user если все прошло успешно, False если такого пользователя нет
    '''
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        
        if not user:
            return False
        
        user.money += user.business_products * 3
        user.business_products = 0
        await session.commit()
        await session.refresh(user)
        return user
    
    
async def update_business(tg_id: int):
    '''Добавляет бизнес пользователю.
    
    Args:
        tg_id: телеграм ID пользователя
        
    Returns:
        user если все прошло успешно, False если такого пользователя нет
    '''
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        
        if not user:
            return False
        
        user.business = 'Кафе'
        await session.commit()
        await session.refresh(user)
        return user
        
        
async def update_laptop(tg_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        
        if not user:
            return False
        
        user.laptop = True
        await session.commit()
        await session.refresh(user)
        return user
        
        
async def top_players():
    '''Показывает топ игроков по балансу'''
    async with async_session() as session:
        result = await session.scalars(select(User).order_by(desc(User.money)).limit(5))
        return result.all()
    
    
async def get_all_users():
    '''Получает всех пользователей'''
    async with async_session() as session:
        result = await session.execute(select(User))
        return result.scalars().all()