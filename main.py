from fastapi import FastAPI

from src.api import contacts, utils, birstdays

app = FastAPI()

app.include_router(utils.router, prefix="/api")
app.include_router(contacts.router, prefix="/api")
app.include_router(birstdays.router, prefix="/api")
