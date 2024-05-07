from unittest.mock import patch

from main import app
from src.services.auth import auth_service

app.user_middleware = []


def test_get_comment_not_found(client, get_token):
    """
    The test_get_comment_not_found function tests the get_comment function in the comment_service.py file.
    The test is testing that if a user tries to access a comment that does not exist, they will receive an error message.

    :param client: Make a request to the flask application
    :param get_token: Get the token from the auth service
    :return: A 404 status code
    :doc-author: Trelent
    """
    with patch.object(auth_service, "cache") as redis_mock:
        redis_mock.get.return_value = None
        headers = {"Authorization": f"Bearer {get_token}"}
        response = client.get("api/comment/", headers=headers)
        assert response.status_code == 404, response.text


def test_create_comment_imagenotfound(client, get_token):
    """
    The test_create_comment_imagenotfound function tests the create comment endpoint.
        It checks if a user can create a comment on an image that does not exist.

    :param client: Make requests to the api
    :param get_token: Get the token from the auth service
    :return: A 404 status code when the image is not found
    :doc-author: Trelent
    """
    with patch.object(auth_service, "cache") as redis_mock:
        redis_mock.get.return_value = None
        headers = {"Authorization": f"Bearer {get_token}"}
        response = client.post(
            "api/comment/create/100",
            json={"text": "test comment"},
            headers=headers,
        )
        assert response.status_code == 404, response.text
