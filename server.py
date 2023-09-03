from fastapi import FastAPI, Request

from storage.database_adapter import DatabaseAdapter
from routes import init_routes
from utils.logger import init_user_profile_activity_logger


app = FastAPI()
database = DatabaseAdapter()
init_routes(app)
init_user_profile_activity_logger(app)


@app.on_event('startup')
async def app_startup():
    database.connect()


@app.on_event('shutdown')
async def app_teardown():
    database.connect()
