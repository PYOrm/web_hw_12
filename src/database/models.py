from sqlalchemy import Column, String, Integer, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    soname = Column(String(50), nullable=False)
    email = Column(String(100))
    phone = Column("phone_number", String(30))
    birthday = Column("birth_day", Date)
    info = Column("Info", String(250), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    users = relationship("User", back_populates="contacts")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    update_token = Column(String)
    contacts = relationship("Contact", back_populates="users")

    def __init__(self, name, email, password, update_token=None):
        self.name = name
        self.email = email
        self.password = password
        self.update_token = update_token

    def __str__(self):
        return f"{self.name}_{self.email}_{self.password}_{self.update_token}_{self.id}"
