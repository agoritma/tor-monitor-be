import logging
from os import environ

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import auth, chat, dashboard, forecast, goods, sales

load_dotenv()
logger = logging.getLogger(__name__)
logging.info("Starting FastAPI app")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        (
            "*"
            if environ.get("DEV_ENV") == "dev"
            else environ.get("FRONTEND_URL", "http://localhost:3000")
        )
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(goods.router)
app.include_router(sales.router)
app.include_router(chat.router)
app.include_router(forecast.router)
