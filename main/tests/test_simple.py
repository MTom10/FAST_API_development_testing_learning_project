"""
general overview of pytest
tests starts from test_

define the data test will work with,
call the function,
check if the result is what we expect

fixtures - a way sto share the data without duplicating it within our tests


import pytest
import httpx
from httpx import ASGITransport
from fastapi import FastAPI
from httpx import AsyncClient

# Assuming the FastAPI app and necessary routes are defined in 'myapp'
from main.main import app
from main.tests.routers.test_post import created_comment


# Example of creating a fixture for async_client using ASGITransport



# Example of a fixture to create a post that the comment will be associated with
@pytest.fixture
async def created_post(async_client: AsyncClient, created_comment: dict):
    body = "Test Comment"

    response = await async_client.post(
        "/posts",
        json={"body": body, "post_id": created_post["id"]},
    )
    return response.json()


# The test_create_comment function using the anyio marker
@pytest.mark.anyio
async def test_create_comments(async_client: AsyncClient, created_post: dict):
    body = "Test Comment"

    response = await async_client.post(
        "/comment",
        json={"body": body, "post_id": created_post["id"]}
    )

    # Assertions to verify the response
    assert response.status_code == 201
    assert {
        "id": 0,  # Adjust based on how your application handles IDs (e.g., auto-increment)
        "body": body,
        "post_id": created_post["id"]
    }.items() <= response.json().items()



def test_add_two():
    x = 1
    y = 2
    assert x + y == 3


# testing dictionaries
def test_dict():
    x = {"a": 1, "b": 2}

    expected = {"a": 1}

    assert expected.items() <= x.items()

"""