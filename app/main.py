from fastapi import FastAPI, Request
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from starlette.status import HTTP_429_TOO_MANY_REQUESTS

from app.routers import contacts, auth, users
from app.services.limiter import limiter
from app import database

app = FastAPI(title="Contacts API", debug=True)

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)


@app.exception_handler(RateLimitExceeded)
async def ratelimit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=HTTP_429_TOO_MANY_REQUESTS,
        content={"detail": "Rate limit exceeded. Try again later."}
    )

app.include_router(contacts.router)
app.include_router(auth.router)
app.include_router(users.router)


@app.on_event("startup")
async def on_startup():
    async with database.engine.begin() as conn:
        await conn.run_sync(database.Base.metadata.create_all)
