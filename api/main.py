from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import event, user

from dotenv import load_dotenv


load_dotenv()
app = FastAPI()
app.include_router(event.router, prefix="/api")
app.include_router(user.router, prefix="/api")

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)
