from fastapi import APIRouter


profile_router = APIRouter(prefix='/profile')


@profile_router.get('/{username}')
async def get_profile(username: str):
    return {'username': username}
