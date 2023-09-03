import json
from datetime import datetime, timezone

from fastapi import FastAPI, Request


def init_user_profile_activity_logger(app: FastAPI) -> None:
    async def set_body(request: Request, body: bytes):
        async def receive():
            return {"type": "http.request", "body": body}
        request._receive = receive

    async def get_body(request: Request) -> bytes:
        body = await request.body()
        await set_body(request, body)
        return body

    @app.middleware('http')
    async def log_user_activity(request: Request, call_next):
        if request.url.path.startswith('/profile'):
            # fastAPI middlewares are buggy, we cannot read the request body with [async request.json()]
            # this ugly ugly code is a workaround for that
            body = json.loads(await get_body(request))
            response = await call_next(request)
            if response.status_code < 300:
                with open('./logs/user_profile_activity.log', 'a') as file:
                    file.write(_create_log_entry(body['email'], _get_activity(request.url)))
                return response

        return await call_next(request)


def _create_log_entry(email: str, activity: str) -> str:
    return f'[{_get_current_time_for_log_entry()}] [email: {email}] [activity: {activity}]\n'


def _get_activity(url: str) -> str:
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


def _get_current_time_for_log_entry() -> str:
    current_time_str = str(datetime.now(timezone.utc))
    return current_time_str[:current_time_str.index('.')]
