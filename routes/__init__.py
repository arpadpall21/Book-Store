from fastapi import FastAPI


def init_routes(app: FastAPI) -> None:
    from routes.profile.router import profile_router
    from routes.store.router import store_router
    from routes.archive.router import archive_router
    from routes.ws.router import ws_router

    app.include_router(profile_router)
    app.include_router(store_router)
    app.include_router(archive_router)
    app.include_router(ws_router)
