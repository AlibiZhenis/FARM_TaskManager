from model import Todo
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient('mongodb://localhost:27017')
db = client.TodoList
collection = db.todo


async def fetch_one(title):
    document = await collection.find_one({"title": title})
    return document


async def fetch_all():
    todos = []
    cursor = collection.find({})
    async for document in cursor:
        todos.append(Todo(**document))
    return todos


async def create_one(todo):
    document = todo
    result = await collection.insert_one(document)
    return document


async def update_one(title, desc):
    await collection.update_one({"title": title}, {"$set": {"description": desc}})
    document = await collection.find_one({"title": title})
    return document


async def remove_one(title):
    await collection.delete_one({"title": title})
    return True
