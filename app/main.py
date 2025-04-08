from fastapi import FastAPI
from app.routers import contacts
from app import models, database

app = FastAPI(title="Contacts API", debug=True)

# Підключення роутерів
app.include_router(contacts.router)

# Ініціалізація таблиць при старті (тільки для прикладу)
@app.on_event("startup")
async def on_startup():
    async with database.engine.begin() as conn:
        await conn.run_sync(database.Base.metadata.create_all)
