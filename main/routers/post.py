"""
API router is a fast API app which can be included into an existing app instead of running on its own,
lets us using 'router' endpoints within an original app.
"""

from fastapi import APIRouter, HTTPException

from main.models.post import UserPost, UserPostIn, Comment, CommentIn, UserPostWithComments

# create FAST app
router = APIRouter()

# Database, dict for the moment, to be changed later on
post_table = {}
comment_table = {}


@router.get("/")
async def root():
    return {"message": "Hello !"}


# create the post
@router.post("/post", response_model=UserPost, status_code=201)
async def create_post(post: UserPostIn):
    data = post.model_dump()  # generate the dictionary representation
    last_record_id = len(post_table)
    new_post = {**data, "id": last_record_id}
    post_table[last_record_id] = new_post
    return new_post


# retrieve all posts
@router.get("/post", response_model=list[UserPost])  # response model uses python hinting
async def get_all_posts():
    return list(post_table.values())  # get all the values of dictionary and turn it into a list


# find a post by specifying the id
def find_post(post_id: int):
    return post_table.get(post_id)


# create comment, add error handling
@router.post("/comment", response_model=Comment, status_code=201)
async def create_comment(comment: CommentIn):
    post = find_post(comment.post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    data = comment.model_dump()  # generate the dictionary representation
    last_record_id = len(comment_table)
    new_comment = {**data, "id": last_record_id}
    comment_table[last_record_id] = new_comment
    return new_comment


# get comments on a post
@router.get("/post/{post_id}/comment", response_model=list[Comment])
async def get_comments_on_post(post_id: int):
    return [
        comment for comment in comment_table.values() if comment["post_id"] == post_id
    ]


# get post with comments
@router.get("/post/{post_id}", response_model=UserPostWithComments)
async def get_post_with_comments(post_id: int):
    post = find_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # await to ensure the post will be retrieved before loading the comments
    return {
        "post": post,
        "comments": await get_comments_on_post(post_id),
    }
