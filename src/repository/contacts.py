
import datetime
from typing import Type

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactModel


async def get_all_contacts(db: Session, user: User, skip: int = 0, limit: int = 100) -> list[Type[Contact]]:
    return db.query(Contact).filter_by(user_id=user.id).offset(skip).limit(limit).all()


async def get_contact_by_id(db: Session, contact_id: int, user: User) -> Type[Contact] | None:
    return db.query(Contact).filter_by(id=contact_id, user_id=user.id).first()


async def get_contact_(db: Session, name: str | None, soname: str | None, email: str | None, user: User) -> list[
    Type[Contact]]:
    res = db.query(Contact).filter_by(user_id=user.id)
    if name:
        res = res.filter_by(name=name)

    if soname:
        res = res.filter_by(soname=soname)

    if email:
        res = res.filter_by(email=email)
    return res.all()


async def delete_contact(db: Session, contact_id: int, user: User) -> Contact | None:
    contact = db.query(Contact).filter(contact_id=Contact.id, user_id=user.id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def update_contact_by_id(db: Session, contact_id: int, body: ContactModel, user: User) -> Contact | None:
    contact = db.query(Contact).filter_by(id=contact_id).first()
    if contact:
        contact.name = body.name
        contact.soname = body.soname
        contact.phone = body.phone
        contact.email = body.email
        contact.birthday = body.birthday
        contact.info = body.info
        contact.user_id = user.id
        db.commit()
    return contact


async def create_contact(db: Session, body: ContactModel, user: User) -> Contact | None:
    contact = Contact(name=body.name, soname=body.soname, email=body.email, phone=body.phone, info=body.info,
                      birthday=body.birthday, user_id=user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def get_upcoming_birthdays(db: Session, user: User) -> list[Type[Contact]] | None:
    nearest_birthdays = []
    today = datetime.date.today()
    contacts = db.query(Contact).filter(user_id=user.id).all()
    for contact in contacts:
        birthday = contact.birthday
        birthday_date_in_year = datetime.date.replace(birthday, year=today.year)
        if 0 > (birthday_date_in_year - today).days:
            birthday_date_in_year = datetime.date.replace(birthday, year=today.year + 1)
        if (birthday_date_in_year - today).days <= 7:
            nearest_birthdays.append(contact)
    return nearest_birthdays

