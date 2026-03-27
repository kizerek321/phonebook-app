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
            "description": "Create a new contact in phonebook. Each contact name must be unique.",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "name": {"type": "STRING", "description": "Name of the person (must be unique)"},
                    "phone": {"type": "STRING", "description": "Phone number of the person"}
                },
                "required": ["name", "phone"]
            }
        },
        {
            "name": "delete_contact",
            "description": "Delete a contact from phonebook by name",
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
                        "description": "Current name of the person"
                    },
                    "new_phone": {
                        "type": "STRING",
                        "description": "New phone number of the person"
                    },
                    "new_name": {
                        "type": "STRING",
                        "description": "New name of the person (must be unique)"
                    }
                },
                "required": ["name"]
            }
        },
        {
            "name": "get_contact",
            "description": "Get a contact from phonebook by name",
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
        }
    ]
}]
