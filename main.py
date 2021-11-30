from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session

from blog import schemas as blog_schemas, models as blog_models
from blog.passwords import Password
from database import engine, get_db

blog_models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Add blog entry
@app.post(path='/create-blog', status_code=status.HTTP_201_CREATED, tags=['blog'])
def create_blog(request: blog_schemas.Blog, db: Session = Depends(get_db)):
    new_blog = (blog_models.Blog(title=request.title, body=request.body, published=False))
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


# Get all blogs
@app.get(path='/blogs', tags=['blog'])
def list_blogs(db: Session = Depends(get_db)):
    return db.query(blog_models.Blog).all()


# Get blog
@app.get(path='/blogs/{pk}', tags=['blog'])
def get_blog(pk, db: Session = Depends(get_db), ):
    blog = db.query(blog_models.Blog).filter(blog_models.Blog.id == pk).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Blog not found')
    return blog


# Update blog
@app.put(path='/blogs/{pk}', status_code=status.HTTP_202_ACCEPTED, tags=['blog'])
def update_blog(pk, request: blog_schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(blog_models.Blog).filter(blog_models.Blog.id == pk)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Blog not found')
    blog.update({'title': request.title, 'body': request.body, 'published': request.published})
    db.commit()
    return {'detail': 'Updated'}


# Delete blog
@app.delete(path='/blogs/{pk}', status_code=status.HTTP_204_NO_CONTENT, tags=['blog'])
def delete_blog(pk, db: Session = Depends(get_db)):
    blog = db.query(blog_models.Blog).filter(blog_models.Blog.id == pk)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Blog not found')
    blog.delete(synchronize_session=False)
    db.commit()
    return 'Deleted'


# Create user
@app.post(path='/user', status_code=status.HTTP_201_CREATED, response_model=blog_schemas.ShowUser, tags=['user'])
def create_user(request: blog_schemas.User, db: Session = Depends(get_db)):
    user = (blog_models.User(name=request.name, email=request.email, password=Password(request.password).encrypt()))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
