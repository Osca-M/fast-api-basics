from fastapi import FastAPI

from database import engine
from blog import models as blog_models
from user import models as user_models
from user.router import router as user_router
from blog.router import router as blog_router

blog_models.Base.metadata.create_all(bind=engine)
user_models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_router)
app.include_router(blog_router)




