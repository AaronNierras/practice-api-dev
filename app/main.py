from fastapi import FastAPI
# from fastapi.params import Body

from app import models
from app.database import engine
from app.config import settings

# models.Base.metadata.create_all(bind=engine) # generate database without alembic

app = FastAPI()

# ------------------- INIT ------------------------

from app.routers import post, user, auth, vote

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get('/')
async def get_all_users():
    return {'message': 'Hello World!'}