from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from sqlmodel import Session, select
from contextlib import asynccontextmanager
from pydantic import BaseModel

from .database import engine, create_db_and_tables
from .models import Contact, ContactCreate, ContactUpdate
from .crud import create_contact, get_contacts, get_contact, update_contact, delete_contact
from .llm import client, tools


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
def get_session():
    with Session(engine) as session:
        yield session

class ChatRequest(BaseModel):
    prompt: str

@app.post("/chat")
def process_natural_language(request: ChatRequest, session: Session = Depends(get_session)):
    response = client.models.generate_content(
        model='gemini-2.5-flash', # change to gemini-2.0-flash if rate limits are exceeded
        contents=request.prompt,
        config={"tools": tools}
    )

    if not response.function_calls:
        return {"message": "I do not understand the request or it does not concern the phonebook."}

    fc = response.function_calls[0]
    name = fc.name
    args = fc.args

    if name == "create_contact":
        contact_data = ContactCreate(name=args["name"], phone=args["phone"])
        return create_contact(session, contact_data)

    elif name == "get_all_contacts":
        return get_contacts(session)

    elif name == "get_contact":
        contact = session.exec(select(Contact).where(Contact.name == args["name"])).first()
        if contact:
            return contact
        return {"error": f"Contact {args['name']} not found."}

    # for Update and Delete operations we need to find the contact by name first
    # then update or delete it based on ID
    elif name in ["delete_contact", "update_contact"]:
        contact = session.exec(select(Contact).where(Contact.name == args["name"])).first()
        if not contact:
            return {"error": f"There is no such contact {args['name']}."}

        if name == "delete_contact":
            delete_contact(session, contact.id)
            return {"message": f"Deleted contact: {args['name']}"}

        elif name == "update_contact":
            update_fields = {}
            if "new_name" in args:
                update_fields["name"] = args["new_name"]
            if "new_phone" in args:
                update_fields["phone"] = args["new_phone"]
            update_data = ContactUpdate(**update_fields)
            return update_contact(session, contact.id, update_data)

    return {"error": "Unrecognized operation."}

# create contact
@app.post("/contacts", response_model=Contact)
def create_contact_endpoint(contact: ContactCreate, session: Session = Depends(get_session)):
    return create_contact(session, contact)

# read all contacts
@app.get("/contacts", response_model=list[Contact])
def get_contacts_endpoint(session: Session = Depends(get_session)):
    return get_contacts(session)

# read single contact
@app.get("/contacts/{contact_id}", response_model=Contact)
def get_contact_endpoint(contact_id: int, session: Session = Depends(get_session)):
    return get_contact(session, contact_id)

# update contact
@app.put("/contacts/{contact_id}", response_model=Contact)
def update_contact_endpoint(contact_id: int, contact: ContactUpdate, session: Session = Depends(get_session)):
    return update_contact(session, contact_id, contact)

# delete contact
@app.delete("/contacts/{contact_id}")
def delete_contact_endpoint(contact_id: int, session: Session = Depends(get_session)):
    return delete_contact(session, contact_id)

# --- Static frontend ---
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
def serve_frontend():
    return FileResponse("frontend/index.html")