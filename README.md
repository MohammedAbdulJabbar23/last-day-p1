# testapi-day2-pp2
Real-Time Chat Application with SocketIo, FastAPI, TortoiseORM
Overview

This project implements a real-time chat application using FastAPI, WebSocket, and Tortoise ORM for database operations. Users can connect to different chat rooms via WebSocket and socketio and exchange messages. Chat history is stored in a SQLite database.

Installation

Install the required dependencies:

Linux: python3 -m venv env

source env/bin/activate

pip install fastapi tortoise-orm python-socketio uvicorn fastapi.middleware.cors pytest starlette websocket

bash

Running the Server

Start the server by running:

bash

source env/bin/activate

uvicorn main:app --host 0.0.0.0 --port 8000

Functionality

    WebSocket Endpoint (/ws/{room}):
        Connects users to specific chat rooms.
        Echoes received messages to all users in the same room.
        Stores messages in the database.
    Socket.IO Events:
        Handles client connections and disconnections.
    API Endpoint (/history/{room}):
        Retrieves chat history for a specific room from the database as : 
        {
          sender: string, 
          message: string,
          timestamp: string
        }

Database Setup

The application uses a SQLite database. The database file db.sqlite3 will be created in the project directory upon initialization.

Additional Notes

    CORS Middleware: Enables cross-origin resource sharing to allow requests from any origin.

Usage

    Connect to the WebSocket endpoint /ws/{room} to join a chat room.
    Send messages to communicate with other users in the same room.
    Retrieve chat history for a specific room using the API endpoint /history/{room}.
