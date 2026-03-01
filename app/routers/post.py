from .. import models, schemas, oauth2
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlmodel import Session
from ..database import get_session
from typing import List, Optional
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

# @router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
async def get_posts(db: Session = Depends(get_session), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # curr.execute("""SELECT * FROM posts""")
    # posts = curr.fetchall()
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).offset(skip).limit(limit).all()

    results = db.query(models.Post).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).with_entities(models.Post, func.count(models.Vote.post_id).label("votes")).filter(models.Post.title.contains(search)).offset(skip).limit(limit).all()

    return results

#Without using Pydantic Model

# @app.post("/create-post")
# async def create_post(payload: dict = Body(...) ):
#     print(payload)
#     return {"tile": f"{payload['title']}",
#             "content": f"{payload['content']}"}

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_session), current_user: int = Depends(oauth2.get_current_user)):
    # post_dict = post.dict()
    # curr.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,(post.title, post.content, post.published))

    # conn.commit()

    # new_post = curr.fetchone()
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=schemas.PostOut)
async def get_post(id: int, response: Response, db: Session = Depends(get_session), current_user: int = Depends(oauth2.get_current_user)):
    # curr.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    # post = curr.fetchone()

    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).with_entities(models.Post, func.count(models.Vote.post_id).label("votes")).filter(models.Post.id == id).first()
    if not post:    
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    return post

@router.put("/{id}", response_model=schemas.Post)
async def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_session), current_user: int = Depends(oauth2.get_current_user)):
    # curr.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    # post = curr.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} was not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post_query.update(updated_post.dict(exclude_unset=True), synchronize_session=False)

    db.commit()

    return post_query.first()

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_session), current_user: int = Depends(oauth2.get_current_user)):
    # curr.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # post = curr.fetchone()
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} was not found")
    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)