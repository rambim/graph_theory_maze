from fastapi import FastAPI
from api.routers.commands import command_routes

api = FastAPI ()
api.include_router (router = command_routes)