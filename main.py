from aiohttp import web
import asyncio
import aiohttp_jinja2
import jinja2

from routes import routes
from setup import setup

#set event loop for asyncio
loop = asyncio.get_event_loop()
db = loop.run_until_complete(setup())

# AIO Web App
app = web.Application()
app['db'] = db

#set up for the jinja templating
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader("templates"))

# Pass the web app to setup routes
routes(app)

#run the web app
web.run_app(app)