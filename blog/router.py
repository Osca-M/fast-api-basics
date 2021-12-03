from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from . import schemas, models
from user import schema as user_schema, auth, models as user_models

router = APIRouter()


# Add blog entry
@router.post(path='/create-blog', status_code=status.HTTP_201_CREATED, tags=['blog'])
def create_blog(
        request: schemas.Blog,
        db: Session = Depends(get_db),
        current_user: user_schema.User = Depends(auth.get_current_user)
):
    user = db.query(user_models.User).filter(user_models.User.email == current_user.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect email or password')
    new_blog = (models.Blog(title=request.title, body=request.body, published=False, user_id=str(user.id)))
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


# Get all blogs
@router.get(path='/blogs', tags=['blog'])
def list_blogs(db: Session = Depends(get_db)):
    return db.query(models.Blog).all()


# Get blog
@router.get(path='/blogs/{pk}', tags=['blog'])
def get_blog(pk, db: Session = Depends(get_db), ):
    blog = db.query(models.Blog).filter(models.Blog.id == pk).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Blog not found')
    return blog


# Update blog
@router.put(path='/blogs/{pk}', status_code=status.HTTP_202_ACCEPTED, tags=['blog'])
def update_blog(pk, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == pk)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Blog not found')
    blog.update({'title': request.title, 'body': request.body, 'published': request.published})
    db.commit()
    return {'detail': 'Updated'}


# Delete blog
@router.delete(path='/blogs/{pk}', status_code=status.HTTP_204_NO_CONTENT, tags=['blog'])
def delete_blog(pk, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == pk)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Blog not found')
    blog.delete(synchronize_session=False)
    db.commit()
    return 'Deleted'
