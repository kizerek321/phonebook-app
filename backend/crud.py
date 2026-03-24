# Functions for DB operations (create, read, update, delete)
from sqlmodel import Session, select
from .models import Contact, ContactCreate, ContactUpdate

# Create contact
def create_contact(session: Session, contact: ContactCreate):
    db_contact = Contact.model_validate(contact)
    session.add(db_contact)
    session.commit()
    session.refresh(db_contact)
    return db_contact

# Read all contacts
def get_contacts(session: Session):
    result = session.exec(select(Contact))
    return result.all()

# Read single contact
def get_contact(session: Session, contact_id: int):
    result = session.get(Contact, contact_id)
    return result

def update_contact(session: Session, contact_id: int, contact: ContactUpdate):
    db_contact = session.get(Contact, contact_id)
    if not db_contact:
        return None
        
    update_data = contact.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_contact, key, value)
            
    session.add(db_contact)
    session.commit()
    session.refresh(db_contact)
    return db_contact

def delete_contact(session: Session, contact_id: int):
    db_contact = session.get(Contact, contact_id)
    if not db_contact:
        return None
    session.delete(db_contact)
    session.commit()
    return True