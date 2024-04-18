from fastapi import status, Response, HTTPException, Depends, APIRouter

from sqlalchemy.orm import Session

import oauth2
from .. import models, schemas, database
from ..database import conn, cursor


router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


# ------------------- ORM ------------------------


@router.get('/orm', response_model=list[schemas.PostResponse])
async def get_all_posts_orm(db: Session = Depends(database.get_db), current_user: models.DBUser = Depends(oauth2.get_current_user), limit: int = 10, offset: int = 0, search: str | None = ''):
    posts = db.query(models.DBPost).filter(models.DBPost.title.contains(search)).limit(limit).offset(offset).all()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"posts was not found")
    print('status: SqlAlchemy success!')
    return posts


@router.get('/orm/my_posts', response_model=list[schemas.PostResponse])
async def get_all_posts_mine_orm(db: Session = Depends(database.get_db), current_user: models.DBUser = Depends(oauth2.get_current_user)):
    posts = db.query(models.DBPost).filter(models.DBPost.user_id == current_user.id).all()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"posts was not found")
    return posts


@router.get('/orm/{id}', response_model=schemas.PostResponse)
async def get_post_orm(id: int, db: Session = Depends(database.get_db), current_user: models.DBUser = Depends(oauth2.get_current_user)):
    post = db.query(models.DBPost).filter(models.DBPost.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return post


@router.post('/orm', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
async def create_post_orm(new_post: schemas.PostCreate, db: Session = Depends(database.get_db), current_user: models.DBUser = Depends(oauth2.get_current_user)):
    post = models.DBPost(**new_post.model_dump(), user_id=current_user.id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.put('/orm/{id}', response_model=schemas.PostResponse)
async def update_post(id: int, post: schemas.PostUpdate, db: Session = Depends(database.get_db), current_user: models.DBUser = Depends(oauth2.get_current_user)):
    post_query = db.query(models.DBPost).filter(models.DBPost.id == id)
    post_result = post_query.first()
    if not post_result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    if post_result.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()


@router.delete('/orm/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post_orm(id: int, db: Session = Depends(database.get_db), current_user: models.DBUser = Depends(oauth2.get_current_user)):
    post_query = db.query(models.DBPost).filter(models.DBPost.id == id)
    post = post_query.first()
    if not post_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# ------------------- SQL ------------------------


@router.get('/', response_model=list[schemas.PostResponse])
async def get_all_posts(current_user: models.DBUser = Depends(oauth2.get_current_user)):
    query = "SELECT * FROM posts ORDER BY id ASC"
    cursor.execute(query)
    posts = cursor.fetchall()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"posts was not found")
    fixed_posts = [{} for _ in range(len(posts))]
    for i, post in enumerate(posts):
        query = "SELECT * FROM users WHERE id = %s"
        cursor.execute(query, (str(post[5]))) # query only accepts strings
        user = cursor.fetchone()
        fixed_posts[i].update(
            {
            'id': post[0], 'title': post[1], 'contents': post[2], 'created_at': post[4], 'user_id': post[5], 'handle': {'id': user[0], 'email': user[1]}
            }
        )
    return fixed_posts


@router.get('/latest', response_model=schemas.PostResponse)
async def get_latest_post(current_user: models.DBUser = Depends(oauth2.get_current_user)):
    query = "SELECT * FROM posts WHERE id in (SELECT id FROM posts ORDER BY created_at DESC LIMIT 1)"
    cursor.execute(query)
    post = cursor.fetchone()
    query = "SELECT * FROM users WHERE id = %s"
    cursor.execute(query, (str(post[5]))) # query only accepts strings
    user = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    fixed_post = {}
    fixed_post.update(
        {
        'id': post[0], 'title': post[1], 'contents': post[2], 'created_at': post[4], 'user_id': post[5], 'handle': {'id': user[0], 'email': user[1]}
        }
    )
    return fixed_post


@router.get('/{id}', response_model=schemas.PostResponse)
async def get_post(id: int, current_user: models.DBUser = Depends(oauth2.get_current_user)):
    query = "SELECT * FROM posts WHERE id = %s AND user_id = %s"
    cursor.execute(query, (str(id), str(current_user.id))) # query only accepts strings
    post = cursor.fetchone()
    query = "SELECT * FROM users WHERE id = %s"
    cursor.execute(query, (str(post[5]))) # query only accepts strings
    user = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    fixed_post = {}
    fixed_post.update(
        {
        'id': post[0], 'title': post[1], 'contents': post[2], 'created_at': post[4], 'user_id': post[5], 'handle': {'id': user[0], 'email': user[1]}
        }
    )
    return fixed_post


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
async def create_post(new_post: schemas.Post, current_user: models.DBUser = Depends(oauth2.get_current_user)):
    query = '''INSERT INTO posts (title, contents, published, user_id) VALUES (%s, %s, %s, %s) RETURNING *'''
    cursor.execute(query,(new_post.title, new_post.contents, new_post.published, current_user.id))
    post = cursor.fetchone()
    fixed_post = {}
    fixed_post.update(
        {
        'id': post[0], 'title': post[1], 'contents': post[2], 'created_at': post[4]
        }
    )
    conn.commit()
    return fixed_post


@router.put('/{id}', response_model=schemas.PostResponse)
async def update_post(id: int, post: schemas.Post, current_user: models.DBUser = Depends(oauth2.get_current_user)):
    query = '''UPDATE posts SET title = %s, contents = %s, published = %s WHERE id = %s AND user_id = %s RETURNING *'''
    cursor.execute(query,(post.title, post.contents, post.published, str(id), str(current_user.id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    fixed_post = {}
    fixed_post.update(
        {
        'id': post[0], 'title': post[1], 'contents': post[2], 'created_at': post[4]
        }
    )
    conn.commit()
    return fixed_post


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, current_user: models.DBUser = Depends(oauth2.get_current_user)):
    query = "DELETE FROM posts WHERE id = %s AND user_id = %s RETURNING *"
    cursor.execute(query, (str(id), str(current_user.id))) # query only accepts strings
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    fixed_post = {}
    fixed_post.update(
        {
        'id': post[0], 'title': post[1], 'contents': post[2], 'created_at': post[4]
        }
    )
    conn.commit()
    return fixed_post

