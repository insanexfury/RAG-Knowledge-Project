from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.pipeline import RagPipeline
from app.api.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.pipeline = RagPipeline()

    yield

    # optional cleanup


app = FastAPI(
    lifespan=lifespan
)

app.include_router(router)