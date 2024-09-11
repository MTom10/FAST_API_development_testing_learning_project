from pydantic import BaseModel  # Class that allows to define the model to validate the data


class UserPostIn(BaseModel):
    body: str


class UserPost(UserPostIn):
    id: int


# comment class, stores body, post id, and its own comment id
class CommentIn(BaseModel):
    body: str
    post_id: int


class Comment(CommentIn):
    id: int


"""
retrieve post with its comments, nesting models within models
{
    "post": {"id": 0, "body": "my post"}, 
    "comments": [{"id": 2, "post_id": 0, "body": "my comment"}],
}
"""


class UserPostWithComments(BaseModel):
    post: UserPost
    comments: list[Comment]

