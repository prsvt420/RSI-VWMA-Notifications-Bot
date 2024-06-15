from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker, AsyncSession

from bot.config import DATABASE_URL

async_engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=False)
async_session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)
