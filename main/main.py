from contextlib import asynccontextmanager

from fastapi import FastAPI

from main.routers.post import router as post_router
from main.database import database


# db connection established before running the API
# context manager/ cet-up , tear-down and pauses in the middle until something happens
@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connnect()
    yield
    await database.disconnect()


# create FAST app, it will keep lifespan of db till the app is shut down.
app = FastAPI(lifespan=lifespan)

# include the routers in the app , can add prefixes such as (post_router, prefix="/posts")
app.include_router(post_router)
