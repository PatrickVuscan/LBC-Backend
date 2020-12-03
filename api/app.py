"""Main app."""
from fastapi import FastAPI
import uvicorn

from api.database.db_initialize import ENGINE
from api.model.table_models import Base
from api.routes.users import ROUTER as user_router
from api.routes.comment import ROUTER as comment_router
from api.routes.post import ROUTER as post_router

app = FastAPI()

Base.metadata.create_all(bind=ENGINE)


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(user_router)
app.include_router(comment_router)
app.include_router(post_router)

if __name__ == "__main__":
    uvicorn.run(
        "api.app:app",
        host="127.0.0.1",
        port=5000,
    )
