from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#DATABASE_URL = "postgresql+asyncpg://postgres:Amigad@2@localhost/RAG"(This url is not working beacuse of my password have @ that's why I have to use the converted link)
#URL-encode 
DATABASE_URL = "postgresql+asyncpg://postgres:Amigada%402@localhost/RAG"


engine = create_async_engine(DATABASE_URL, echo=True)

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()
