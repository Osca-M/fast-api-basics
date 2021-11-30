from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session

from blog import schemas as blog_schemas, models as blog_models
from database import engine, get_db

blog_models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Add blog entry
@app.post(path='/create-blog', status_code=status.HTTP_201_CREATED)
def create_blog(request: blog_schemas.Blog, db: Session = Depends(get_db)):
    new_blog = (blog_models.Blog(title=request.title, body=request.body, published=False))
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


# Get all blogs
@app.get(path='/blogs')
def list_blogs(db: Session = Depends(get_db)):
    return db.query(blog_models.Blog).all()


# Get blog
@app.get(path='/blogs/{pk}')
def list_blogs(pk, db: Session = Depends(get_db), ):
    blog = db.query(blog_models.Blog).filter(blog_models.Blog.id == pk).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Blog not found')
    return blog
