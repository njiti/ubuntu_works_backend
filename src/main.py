from fastapi import FastAPI
from .database import Base, engine
from .api import router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Ubuntu Works",
    description="Engine Behind Ubuntu Works",
    version="0.1",
)
app.include_router(router)
