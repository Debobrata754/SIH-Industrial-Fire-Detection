from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "SIH 26162 Backend is running!"
    }