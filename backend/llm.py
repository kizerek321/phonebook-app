# Google GenAI logic and tool definitions
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()
client = genai.Client()

tools = [{
    "function_declarations":[
        {
            "name": "create_contact",
            "description": "Create a new contact in phonebook",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "name": {"type": "STRING", "description": "Name of the person"},
                    "phone": {"type": "STRING", "description": "Phone number of the person"}
                },
                "required": ["name", "phone"]
            }
        },
        {
            "name": "delete_contact",
            "description": "Delete a contact from phonebook",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "name": {"type": "STRING", "description": "Name of the person"}
                },
                "required": ["name"]
            }
        },
        {
            "name": "update_contact",
            "description": "Update an existing contact's phone number or name in phonebook",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "name": {
                        "type": "STRING",
                        "description": "Name of the person"
                    },
                    "new_phone": {
                        "type": "STRING",
                        "description": "New phone number of the person"
                    },
                    "new_name": {
                        "type": "STRING",
                        "description": "New name of the person"
                    }
                },
                "required": ["name"]
            }
        },
        {
            "name": "get_contact",
            "description": "Get a contact from phonebook",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "name": {"type": "STRING",  "description": "Name of the person"}
                },
                "required": ["name"]
            }
        },
        {
            "name": "get_all_contacts",
            "description": "Get all contacts from phonebook"
        },
        {
            "name": "get_contact_by_id",
            "description": "Get a specific contact from phonebook by their unique ID",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "id": {"type": "STRING", "description": "Unique ID of the contact"}
                },
                "required": ["id"]
            }
        },
        {
            "name": "delete_contact_by_id",
            "description": "Delete a specific contact from phonebook by their unique ID",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "id": {"type": "STRING", "description": "Unique ID of the contact"}
                },
                "required": ["id"]
            }
        },
        {
            "name": "update_contact_by_id", 
            "description": "Update a specific contact from phonebook by their unique ID",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "id": {"type": "STRING", "description": "Unique ID of the contact"},
                    "new_name": {"type": "STRING", "description": "New name of the contact"},
                    "new_phone": {"type": "STRING", "description": "New phone number of the contact"}
                },
                "required": ["id"]
            }
        }
    ]
}]
