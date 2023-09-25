import json
from datetime import datetime, timezone

from fastapi import FastAPI, Request


# fastAPI middlewares are buggy, we cannot read the request body with [async request.json()]
# this ugly code is a workaround for that
def init_user_profile_activity_logger(app: FastAPI) -> None:
    from server import database

    async def set_body(request: Request, body: bytes):
        async def receive():
            return {"type": "http.request", "body": body}
        request._receive = receive

    async def get_body(request: Request) -> bytes:
        body = await request.body()
        await set_body(request, body)
        return body

    @app.middleware('http')
    async def log_user_profile_activity(request: Request, call_next):
        if request.url.path.startswith('/profile'):
            user_email = None
            if request.method == 'POST':
                body = json.loads(await get_body(request))
                user_email = body.get('email')
            else:
                session_id = request.cookies.get('sessionId')
                user_email = database.get_user_email_from_session_id(session_id)

            response = await call_next(request)
            if response.status_code >= 200 and response.status_code < 300:
                log_user_activity(user_email, _get_user_activity(request.url))
                return response

        return await call_next(request)


def log_user_activity(email: str, activity: str) -> None:
    with open('./log/user.log', 'a') as file:
        file.write(f'[{_get_current_log_time()}] [email: {email}] [activity: {activity}]\n')


def log_email_activity(email: str, activity: str) -> None:
    with open('./log/email.log', 'a') as file:
        file.write(f'[{_get_current_log_time()}] [email: {email}] [activity: {activity}]\n')


def _get_user_activity(url: str) -> str:
    if url.path == '/profile/register':
        return 'register new profile'
    elif url.path == '/profile/delete':
        return 'delete profile'
    elif url.path == '/profile/login':
        return 'login'
    elif url.path == '/profile/logout':
        return 'logout'
    else:
        return 'unknown activity'


def _get_current_log_time() -> str:
    current_time_str = str(datetime.now(timezone.utc))
    return current_time_str[:current_time_str.index('.')]
