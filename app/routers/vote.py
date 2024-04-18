from fastapi import status, Response, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from app import database, models, schemas
import oauth2

router = APIRouter(
    prefix='/votes',
    tags=['Vote']
)


@router.post('/orm', status_code=status.HTTP_201_CREATED)
async def vote_post(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: models.DBUser = Depends(oauth2.get_current_user)):
    # Check if post exists
    post = db.query(models.DBPost).filter(models.DBPost.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found.")
    
    vote_query = db.query(models.DBVote)\
        .filter(models.DBVote.post_id == vote.post_id, models.DBVote.user_id == current_user.id)
    found_vote = vote_query.first()
    if (vote.direction == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You already liked the post.")
        new_vote = models.DBVote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Liked the post."}
    elif (vote.direction == 0):
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote does not exist.")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Unliked the post."}