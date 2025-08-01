from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database import create_tables, drop_tables
from src import router, init_exc_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield
    

app = FastAPI(
    title='[pastebin] Auth Service',
    lifespan=lifespan,
)

init_exc_handlers(app)
app.include_router(router)

