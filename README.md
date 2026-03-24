# Project Overview

This project is a phonebook application that uses Google GenAI to interact with the phonebook.

## Features

- Add contacts
- Delete contacts
- Search contacts
- List contacts

## Tech Stack

- Python
- FastAPI
- SQLModel
- Google GenAI

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
uvicorn main:app --reload
```

## API Documentation

```bash
http://localhost:8000/docs
```

# INSTRUCTION:

Objective: Develop a web application that functions as a digital phone book, enabling users to manage contact records through natural language prompts.

Requirements:

* Functionality:
    - Implement features to add, edit, delete, and retrieve contact records. Each record should contain two fields: Name and Phone Number.
    - Utilize a Large Language Model (LLM) to interpret and execute natural language commands effectively.

* User Interface:
    - Design a simple and intuitive web interface that allows users to input commands easily.
    - Display the list of contacts in a clear and user-friendly format.

* Technical Stack:
    - Choose any web framework you prefer for development.
    - Store contact records in a relational database. You can select any suitable Database Management System (DBMS).

* Deliverables:
    - Host the source code on a public repository (e.g., GitHub).
    - Provide brief documentation that explains the application, its features, and instructions for use.

* Prompt Examples:
    - "Add to my phone book John. His phone number is 123456789."
    - "Please add a record for Joanna with the number 222333444."
    - "What is the phone number for Joanna?"


# EXECUTION FLOW:
1. User types "Add Joanna 222333444" on the frontend.

2. Frontend sends this string to a new FastAPI /chat endpoint.

3. FastAPI forwards the string to the LLM, attaching a JSON map of your CRUD tools.

4. The LLM analyzes the string and responds with a JSON instruction: {"tool": "create_contact", "args": {"name": "Joanna", "phone": "222333444"}}.

5. FastAPI backend intercepts this JSON, manually maps it to your create_contact function, passes the Session, and writes to the database.

6. FastAPI sends the result back to the frontend for display.