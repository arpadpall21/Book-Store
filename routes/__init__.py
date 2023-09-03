from fastapi import FastAPI


def init_routes(app: FastAPI) -> None:
    from routes.profile.router import profile_router
    from routes.storage.router import storage_router
    from routes.archive.router import archive_router

    app.include_router(profile_router)
    app.include_router(storage_router)
    app.include_router(archive_router)
