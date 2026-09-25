from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def root():
    return {
        "title": "lotus-backend",
        "version": "0.1.0",
        "status": "ok"
    }