from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.repository import contacts as repository_contacts
from src.schemas import ContactResponse, ContactModel
from src.services.auth import auth_service

router = APIRouter(prefix="/contacts")


@router.get("/", response_model=list[ContactResponse])
async def read_contacts(name: str = None, soname: str = None, email: str = None, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    if name or soname or email:
        res = await repository_contacts.get_contact_(db, name=name, soname=soname, email=email, user=current_user)
    else:
        res = await repository_contacts.get_all_contacts(db, current_user)
    return res


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_by_id(contact_id: int, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    return await repository_contacts.get_contact_by_id(db, contact_id, current_user)


@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(contact_id: int, current_user: User = Depends(auth_service.get_current_user), db=Depends(get_db)):
    return await repository_contacts.delete_contact(db, contact_id, current_user)


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_by_id(contact_id: int, body: ContactModel, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    return await repository_contacts.update_contact_by_id(db, contact_id, body, current_user)


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactModel, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    return await repository_contacts.create_contact(db, body, current_user)


@router.get("/upcoming_birthdays/", response_model=list[ContactResponse])
async def upcoming_birthdays(current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    return await repository_contacts.get_upcoming_birthdays(db, current_user)
