from sqlalchemy import BigInteger, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from app.core.config import DATABASE_URL


engine = create_async_engine(url=DATABASE_URL)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    '''Модель пользователя'''
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(String(25))
    money: Mapped[int] = mapped_column(default=0)
    laptop: Mapped[bool] = mapped_column(default=False)
    business: Mapped[str] = mapped_column(String(25), nullable=True, default=None)
    business_products: Mapped[int] = mapped_column(default=0)
    ordered_products: Mapped[int] = mapped_column(default=0)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)