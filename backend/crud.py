# Functions for DB operations (create, read, update, delete)
from sqlmodel import Session, select
from .models import Contact, ContactCreate, ContactUpdate

# Create contact (name stored lowercase, must be unique)
def create_contact(session: Session, contact: ContactCreate):
    contact_name = contact.name.lower()

    # Check if a contact with this name already exists
    existing = session.get(Contact, contact_name)
    if existing:
        return {"error": f"Contact '{contact_name}' already exists. Please use a unique name for each contact."}

    db_contact = Contact(name=contact_name, phone=contact.phone)
    session.add(db_contact)
    session.commit()
    session.refresh(db_contact)
    return db_contact

# Read all contacts
def get_contacts(session: Session):
    result = session.exec(select(Contact))
    return result.all()

# Read single contact by name
def get_contact(session: Session, name: str):
    return session.get(Contact, name.lower())

# Update contact by name
def update_contact(session: Session, name: str, contact: ContactUpdate):
    db_contact = session.get(Contact, name.lower())
    if not db_contact:
        return None

    update_data = contact.model_dump(exclude_unset=True)

    # If renaming, lowercase the new name and check uniqueness
    if "name" in update_data:
        new_name = update_data["name"].lower()
        if new_name != db_contact.name:
            existing = session.get(Contact, new_name)
            if existing:
                return {"error": f"Contact '{new_name}' already exists. Please use a unique name."}
            # Delete old record and create new one (PK change)
            old_phone = db_contact.phone
            session.delete(db_contact)
            session.flush()
            new_contact = Contact(
                name=new_name,
                phone=update_data.get("phone", old_phone)
            )
            session.add(new_contact)
            session.commit()
            session.refresh(new_contact)
            return new_contact
        # Same name, just remove from update_data
        del update_data["name"]

    for key, value in update_data.items():
        setattr(db_contact, key, value)

    session.add(db_contact)
    session.commit()
    session.refresh(db_contact)
    return db_contact

# Delete contact by name
def delete_contact(session: Session, name: str):
    db_contact = session.get(Contact, name.lower())
    if not db_contact:
        return None
    session.delete(db_contact)
    session.commit()
    return True