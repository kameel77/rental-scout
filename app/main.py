import logging

from fastapi import FastAPI

from app.api import auth, backoffice, public

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Rental Scout API", version="0.1.0")

app.include_router(auth.router)
app.include_router(public.router)
app.include_router(backoffice.router)
