from fastapi import FastAPI

app = FastAPI()



@app.get('/')
async def get_all_users():
    return {'message': 'Hello World'}