from fastapi import FastAPI

from api.routers import event, user

app = FastAPI()
app.include_router(event.router, prefix="/api")
app.include_router(user.router, prefix="/api")
