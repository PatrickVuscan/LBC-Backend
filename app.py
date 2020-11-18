"""Main app."""
from typing import Optional

from fastapi import FastAPI
import uvicorn

from api.routes.comment import router as comment_router

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(comment_router)


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=5000,
    )
