# main.py
from fastapi import FastAPI, WebSocket
from models import Room, Message
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise
from socketio import AsyncServer
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
import redis

app = FastAPI()
sio = AsyncServer(async_mode='asgi')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['models']},
    )
    await Tortoise.generate_schemas()
    app.redis = redis.StrictRedis(host='localhost', port=6379, db=0)

@app.on_event("shutdown")
async def shutdown():
    await Tortoise.close_connections()
    app.redis.close()

clients = {}

@app.websocket("/ws/{room}")
async def websocket_endpoint(room: str, websocket: WebSocket):
    await websocket.accept()
    clients[room] = clients.get(room, set())
    clients[room].add(websocket)

    try:
        while True:
            data = await websocket.receive_text()

            for client in clients[room]:
                await client.send_text(data)

            room_obj, created = await Room.get_or_create(name=room)

            if room_obj:
                message = Message(room=room_obj, sender="anonymous", content=data)
                await message.save()

                app.redis.lpush(f"messages:{room}", data)
    except Exception as e:
        print("WebSocket Error:", e)
    finally:
        clients[room].remove(websocket)

@app.get("/history/{room}")
async def get_chat_history(room: str):
    if app.redis.exists(f"messages:{room}"):
        messages = app.redis.lrange(f"messages:{room}", 0, -1)
        formatted_messages = [{"sender": "anonymous", "message": message.decode(), "timestamp": datetime.now()} for message in messages]
        return formatted_messages
    else:
        db_messages = await Message.filter(room__name=room).order_by('-timestamp').all()
        messages = [{"sender": message.sender, "message": message.content, "timestamp": message.timestamp} for message in db_messages]
        for message in messages:
            app.redis.lpush(f"messages:{room}", message['message'])
        return messages

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
