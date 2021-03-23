import motor.motor_asyncio
import docker


#set up database for the server
async def setup():
    client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
    db = client.docker_monitor
    return db