from fastapi import FastAPI
from routers.commands import command_routes

app = FastAPI ()
app.include_router (router = command_routes)