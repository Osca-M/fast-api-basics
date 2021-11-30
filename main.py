from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from blog import schemas as blog_schemas, models as blog_models
from database import engine, get_db

blog_models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Add blog entry
@app.post(path='/create-blog')
def create_blog(request: blog_schemas.Blog, db: Session = Depends(get_db)):
    new_blog = (blog_models.Blog(title=request.title, body=request.body, published=False))
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog
