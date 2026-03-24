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
            "name": "update_phone",
            "description": "Update an existing contact's phone number in phonebook",
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
                    }
                },
                "required": ["name", "new_phone"]
            }
        },
        {
            "name": "update_name",
            "description": "Update an existing contact's name in phonebook",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "old_name": {
                        "type": "STRING",
                        "description": "Old name of the person"
                    },
                    "new_name": {
                        "type": "STRING",
                        "description": "New name of the person"
                    }
                },
                "required": ["old_name", "new_name"]
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
        }
    ]
}]
