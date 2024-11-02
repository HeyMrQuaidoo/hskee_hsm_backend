from fastapi import FastAPI


# local imports
from app.core.config import settings
from app.core.lifespan import lifespan
from app.core.routes import configure_routes
from app.core.middleware import configure_middleware


async def on_fetch(request, env):
    import asgi

    return await asgi.fetch(app, request, env)


# app = FastAPI()
app = FastAPI(title=settings.APP_NAME, description="", lifespan=lifespan)

# configure middleware and routes
configure_middleware(app)
configure_routes(app)