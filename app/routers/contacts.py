from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from .. import schemas, crud, database

router = APIRouter(prefix="/contacts", tags=["Contacts"])

# Dependency
get_db = database.get_db

# Create contact
@router.post("/", response_model=schemas.ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(contact: schemas.ContactCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_contact(contact, db)

# Get all contacts
@router.get("/", response_model=List[schemas.ContactResponse])
async def get_contacts(db: AsyncSession = Depends(get_db)):
    return await crud.get_contacts(db)

# Get contact by ID
@router.get("/{contact_id}", response_model=schemas.ContactResponse)
async def get_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    contact = await crud.get_contact(contact_id, db)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

# Update contact
@router.put("/{contact_id}", response_model=schemas.ContactResponse)
async def update_contact(contact_id: int, updated: schemas.ContactUpdate, db: AsyncSession = Depends(get_db)):
    contact = await crud.update_contact(contact_id, updated, db)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

# Delete contact
@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await crud.delete_contact(contact_id, db)
    if not deleted:
        raise HTTPException(status_code=404, detail="Contact not found")

# Search contacts
@router.get("/search/", response_model=List[schemas.ContactResponse])
async def search_contacts(query: str, db: AsyncSession = Depends(get_db)):
    return await crud.search_contacts(query, db)

# Get upcoming birthdays
@router.get("/upcoming_birthdays/", response_model=List[schemas.ContactResponse])
async def get_upcoming_birthdays(db: AsyncSession = Depends(get_db)):
    return await crud.upcoming_birthdays(db)
