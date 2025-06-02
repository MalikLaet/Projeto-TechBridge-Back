from fastapi import FastAPI

app = FastAPI()

# database = []


@app.get('/')
def read_root():
    return {'message': 'Olá Mundo!'}
