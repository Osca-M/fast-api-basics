from functools import lru_cache

from fastapi import FastAPI, HTTPException
from blog import schemas as blog_schemas, models as blog_models
from database import engine
import config

blog_models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Add blog entry
@app.get(path='/create-blog')
def create_blog(blog: blog_schemas.Blog):
    print(blog, 'blog')
    raise HTTPException(status_code=400, detail="X-Token header invalid")
