from fastapi import FastAPI
from app.api.v1 import auth
from app.api.v1 import users
# to get a string like this run:
# openssl rand -hex 32

app = FastAPI(
    title="Aŭtofluo Backend",
    description="Backend service for Aŭtofluo application",
    version="0.1.0",
)

@app.on_event("startup")
def on_startup():
    from database import create_db_and_tables
    create_db_and_tables()
    print("Database and tables created.")

app.include_router(users.router)
app.include_router(auth.router)