from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_, extract
from typing import List, Optional
from datetime import datetime, timedelta

from . import models

from . import schemas

# Create
async def create_contact(contact: schemas.ContactCreate, db: AsyncSession) -> models.Contact:
    new_contact = models.Contact(**contact.dict())
    db.add(new_contact)
    await db.commit()
    await db.refresh(new_contact)
    return new_contact

# Get by ID
async def get_contact(contact_id: int, db: AsyncSession) -> Optional[models.Contact]:
    result = await db.execute(select(models.Contact).where(models.Contact.id == contact_id))
    return result.scalar_one_or_none()

# Get all
async def get_contacts(db: AsyncSession) -> List[models.Contact]:
    result = await db.execute(select(models.Contact))
    return result.scalars().all()

# Update
async def update_contact(contact_id: int, updated: schemas.ContactUpdate, db: AsyncSession) -> Optional[models.Contact]:
    contact = await get_contact(contact_id, db)
    if contact:
        for field, value in updated.dict(exclude_unset=True).items():
            setattr(contact, field, value)
        await db.commit()
        await db.refresh(contact)
    return contact

# Delete
async def delete_contact(contact_id: int, db: AsyncSession) -> bool:
    contact = await get_contact(contact_id, db)
    if contact:
        await db.delete(contact)
        await db.commit()
        return True
    return False

# Search
async def search_contacts(query: str, db: AsyncSession) -> List[models.Contact]:
    result = await db.execute(
        select(models.Contact).where(
            or_(
                models.Contact.first_name.ilike(f"%{query}%"),
                models.Contact.last_name.ilike(f"%{query}%"),
                models.Contact.email.ilike(f"%{query}%")
            )
        )
    )
    return result.scalars().all()

# Upcoming birthdays (next 7 days)
async def upcoming_birthdays(db: AsyncSession) -> List[models.Contact]:
    today = datetime.today().date()
    in_seven_days = today + timedelta(days=7)

    result = await db.execute(
        select(models.Contact).where(
            extract('month', models.Contact.birthday) == today.month,
            extract('day', models.Contact.birthday) >= today.day,
            extract('day', models.Contact.birthday) <= in_seven_days.day
        )
    )
    return result.scalars().all()
