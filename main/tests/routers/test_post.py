import httpx
import pytest
from httpx import AsyncClient, ASGITransport


# function that calls the api and writes the post as we need it to test the posts
# just a python function, not a fixture
async def create_post(body: str, async_client: AsyncClient) -> dict:
    response = await async_client.post("/post", json={"body": body})
    return response.json()


# function that calls the api and writes the comment as we need it to test the posts
# just a python function, not a fixture
async def create_comment(body: str, post_id: int, async_client: AsyncClient) -> dict:
    response = await async_client.post("/comment", json={"body": body, "post_id": post_id})
    return response.json()


# create fixture tha uses the function
# calls the async_client from tests.testconfig file
@pytest.fixture()
async def created_post(async_client: AsyncClient):
    return await create_post("Test Post", async_client)


@pytest.fixture()
async def created_comment(async_client: AsyncClient, created_post: dict):
    return await create_comment("Test comment", created_post["id"], async_client)


# test creation of the post
@pytest.mark.anyio  # point that anyio framework need to be used for async tests
async def test_create_post(async_client: AsyncClient):
    body = "Test Post"

    response = await async_client.post(
        "/post",
        json={"body": body}
    )

    assert response.status_code == 201
    # what is expected <= json response ( <= makes the test more resiliant rather than =
    assert {"id": 0, "body": body}.items() <= response.json().items()


@pytest.mark.anyio
async def test_create_post_missing_data(async_client: AsyncClient):
    response = await async_client.post(
        "/post",
        json={}
    )

    assert response.status_code == 422


# use the post what is already created thanx to created_post function
@pytest.mark.anyio
async def test_get_all_posts(async_client: AsyncClient, created_post: dict):
    response = await async_client.get("/post")

    assert response.status_code == 200
    assert response.json() == [created_post]


# test comment is been created
@pytest.mark.anyio
async def test_create_comment(async_client: AsyncClient, created_post: dict):
    body = "Test Comment"

    response = await async_client.post(
        "/comment",
        json={"body": body, "post_id": created_post["id"]}
    )

    assert response.status_code == 201
    assert {
        "id": 0,
        "body": body,
        "post_id": created_post["id"]
    }.items() <= response.json().items()


# test get comment on a post
@pytest.mark.anyio
async def test_get_comments_on_post(
    async_client: AsyncClient, created_post: dict, created_comment:dict
):
    response = await async_client.get(f"/post/{created_post["id"]}/comment")

    assert response.status_code == 200
    assert response.json() == [created_comment]


# test no comments on post, empty json response
@pytest.mark.anyio
async def test_get_comments_on_post_empty(
    async_client: AsyncClient, created_post: dict,
):
    response = await async_client.get(f"/post/{created_post["id"]}/comment")

    assert response.status_code == 200
    assert response.json() == []


# get post with comment
@pytest.mark.anyio
async def test_get_post_with_comments(
    async_client: AsyncClient, created_post: dict, created_comment: dict
):
    response = await async_client.get(f"/post/{created_post["id"]}")

    assert response.status_code == 200
    assert response.json() == {
        "post": created_post,
        "comments": [created_comment]
    }


# get the post with comment but the post doesn't exits
@pytest.mark.anyio
async def test_get_missing_post_with_comments(
    async_client: AsyncClient, created_post: dict, created_comment: dict
):
    response = await async_client.get("/post/2")

    assert response.status_code == 404
