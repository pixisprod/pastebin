from contextlib import asynccontextmanager

from fastapi import FastAPI

from src import router, init_handlers

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title='[pastebin] API Gateway',
    lifespan=lifespan,
)

init_handlers(app)
app.include_router(router)
