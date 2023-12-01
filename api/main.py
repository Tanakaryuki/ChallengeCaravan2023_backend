from fastapi import FastAPI

from api.routers import event, user

from dotenv import load_dotenv


load_dotenv()
app = FastAPI()
app.include_router(event.router, prefix="/api")
app.include_router(user.router, prefix="/api")
