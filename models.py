# models.py
from tortoise.models import Model
from tortoise import fields

class Room(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, unique=True)

class Message(Model):
    id = fields.IntField(pk=True)
    room = fields.ForeignKeyField('models.Room', related_name='messages', index=True)
    sender = fields.CharField(max_length=255)
    content = fields.TextField()
    timestamp = fields.DatetimeField(auto_now_add=True, index=True)
