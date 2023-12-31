from fastapi import FastAPI

from database.database_adapter import DatabaseAdapter
from routes import init_routes
from utils.logger import init_user_profile_activity_logger
from utils.helpers import fill_db_with_fake_books


app = FastAPI()
database = DatabaseAdapter()
init_routes(app)
init_user_profile_activity_logger(app)


@app.on_event('startup')
async def app_startup():
    database.connect()
    fill_db_with_fake_books(database)


@app.on_event('shutdown')
async def app_teardown():
    from routes.ws.router import admin_connection_manager

    database.disconnect()
    await admin_connection_manager.disconnect_all_clients()
