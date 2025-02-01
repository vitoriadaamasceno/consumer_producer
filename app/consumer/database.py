from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, types
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@db/noticia"
Base = declarative_base()

class Noticia(Base):
    __tablename__ = "noticias"

    id = Column(types.Integer, primary_key=True, index=True)
    titulo = Column(types.String)
    data_publicacao = Column(types.String)
    link = Column(types.String)

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)
async def get_db_session():
    async with AsyncSessionLocal() as session:
        yield session