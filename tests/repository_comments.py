import unittest
from unittest.mock import AsyncMock
from unittest.mock import MagicMock

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.common import detail_message
from src.database.models import Comment
from src.database.models import Image
from src.database.models import Role
from src.database.models import User
from src.repository.comments import create_comment
from src.repository.comments import delete_comment
from src.repository.comments import edit_comment
from src.repository.comments import get_comment
from src.repository.comments import get_comments_by_image
from src.schemas.comments import CommentSchema


class TestAsyncContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        """
        The setUp function is called before each test function.
        It creates a new user and image object, as well as an AsyncMock session object.

        :param self: Represent the instance of the class
        :return: Nothing
        :doc-author: Trelent
        """
        self.user = User(
            id=1,
            nickname="test_user",
            password="qwerty",
            confirmed="True",
            role="user",
        )

        self.session = AsyncMock(spec=AsyncSession)
        self.image = Image(
            id=1,
            user_id=1,
        )

    async def test_create_comment(self):
        """
        The test_create_comment function tests the create_comment function in the image.py file.
        It creates a comment object and then uses that to test if it is an instance of Comment,
        if its body matches what was created, if it has been refreshed once, committed once and
        if there is a result.

        :param self: Represent the instance of the object that is passed to the method
        :return: An instance of the comment class
        :doc-author: Trelent
        """
        body = CommentSchema(
            comment="test",
        )
        comment = Comment(**body.model_dump(exclude_unset=True), user=self.user)
        result = await create_comment(self.image.id, body, self.session, self.user)
        self.assertIsInstance(result, type(comment))
        self.assertEqual(body.comment, comment.comment)
        self.session.refresh.assert_called_once()
        self.session.commit.assert_called_once()
        self.assertIsNotNone(result)

    async def test_edit_comment(self):
        """
        The test_edit_comment function tests the edit_comment function in the comment.py file.
        The test_edit_comment function is a coroutine that takes in self as an argument and returns nothing.
        The test_edit_comment function creates a body variable that contains a CommentSchema object with
        a comment attribute set to &quot;new&quot;. The mocked comment variable is created by calling MagicMock() on
        the Comment class, which allows us to mock out its scalar one or none method so we can return our own value for it.
        We then call this method and pass it the return value of creating another Comment object with

        :param self: Access the attributes and methods of the class in python
        :return: An instance of the comment class
        :doc-author: Trelent
        """
        body = CommentSchema(
            comment="new_test",
        )
        mocked_comment = MagicMock()
        mocked_comment.scalar_one_or_none.return_value = Comment(
            id=1,
            user_id=1,
            image_id=1,
            comment="new",
        )
        self.session.execute.return_value = mocked_comment
        result = await edit_comment(1, body, self.session, self.user)
        self.assertIsInstance(result, Comment)
        self.session.refresh.assert_called_once()
        self.session.commit.assert_called_once()
        self.assertEqual(result.comment, body.comment)
        self.assertEqual(result.id, self.user.id)
        self.assertEqual(result.image_id, self.image.id)

    async def test_edit_comment_permission_error(self):
        """
        The test_edit_comment_permission_error function tests the edit_comment function to ensure that it raises a 403 error if the user attempting to edit a comment is not the author of that comment.


        :param self: Represent the instance of the object that is passed to a method or function when it is called
        :return: 403 and permission_error
        :doc-author: Trelent
        """
        wrong_user = User(
            id=2,
            nickname="test_user",
            password="qwerty",
            confirmed="True",
            role="user",
        )
        body = CommentSchema(
            comment="new_wrong",
        )
        mocked_comment = MagicMock()
        mocked_comment.scalar_one_or_none.return_value = Comment(
            id=1,
            user_id=1,
            image_id=1,
            comment="new",
        )
        self.session.execute.return_value = mocked_comment
        with self.assertRaises(HTTPException) as context:
            await edit_comment(1, body, self.session, wrong_user)

        self.assertEqual(context.exception.status_code, 403)
        self.assertEqual(context.exception.detail, detail_message.PERMISSION_ERROR)

    async def test_edit_nonexistent_comment(self):
        """
        The test_edit_nonexistent_comment function tests the edit_comment function in the comment.py file.
        The test_edit_nonexistent_comment function is a coroutine that takes in three arguments: self, body, and session.
        The test checks to see if an HTTPException is raised when a user tries to edit a comment that does not exist.

        :param self: Represent the instance of the class
        :return: 404 and file_not_found
        :doc-author: Trelent
        """
        body = CommentSchema(
            comment="new_test",
        )
        mocked_comment = MagicMock()
        mocked_comment.scalar_one_or_none.return_value = None
        self.session.execute.return_value = mocked_comment
        with self.assertRaises(HTTPException) as context:
            await edit_comment(1, body, self.session, self.user)

        self.assertEqual(context.exception.status_code, 404)
        self.assertEqual(context.exception.detail, detail_message.FILE_NOT_FOUND)

    async def test_delete_comment(self):
        """
        The test_delete_comment function tests the delete_comment function in the comments.py file.
        The test_delete_comment function creates a mocked admin user, and then creates a mocked comment object that is returned by
        the scalar_one_or_none method of the session object's execute method. The test then calls the delete comment function with
        the id of 1, which should return an instance of Comment (which it does). The test also asserts that when called with 1 as its
        id argument, both session objects' delete and commit methods are called once each.

        :param self: Represent the instance of the object that is using this method
        :return: An instance of the comment class
        :doc-author: Trelent
        """
        admin = User(
            id=1,
            nickname="test_user",
            password="qwerty",
            confirmed="True",
            role=Role.admin,
        )
        mocked_comment = MagicMock()
        mocked_comment.scalar_one_or_none.return_value = Comment(
            id=1,
            user_id=1,
            image_id=1,
            comment="new",
        )
        self.session.execute.return_value = mocked_comment
        result = await delete_comment(1, self.session, admin)
        self.assertIsInstance(result, Comment)
        self.session.delete.assert_called_once_with(
            mocked_comment.scalar_one_or_none.return_value
        )
        self.session.commit.assert_called_once()
        self.assertEqual(result, mocked_comment.scalar_one_or_none.return_value)

    async def test_delete_comment_from_wrong_role(self):
        """
        The test_delete_comment_from_wrong_role function tests the delete_comment function in the comment.py file.
        The test is testing that a user with an incorrect role cannot delete a comment from an image.

        :param self: Represent the instance of the class
        :return: 403 status code and detail message
        :doc-author: Trelent
        """
        mocked_comment = MagicMock()
        mocked_comment.scalar_one_or_none.return_value = Comment(
            id=1,
            user_id=1,
            image_id=1,
            comment="new",
        )
        self.session.execute.return_value = mocked_comment
        with self.assertRaises(HTTPException) as context:
            await delete_comment(1, self.session, self.user)

        self.assertEqual(context.exception.status_code, 403)
        self.assertEqual(context.exception.detail, detail_message.PERMISSION_ERROR)

    async def test_delete_nonexistent_comment(self):
        """
        The test_delete_nonexistent_comment function tests the delete_comment function in the comments.py file.
        The test_delete_nonexistent_comment function is a coroutine that takes three arguments: self, session, and user.
        The test checks to see if an HTTPException is raised when a comment with an id of 1 does not exist in the database.

        :param self: Represent the instance of the class
        :return: A 404 error message and a detail message
        :doc-author: Trelent
        """
        mocked_comment = MagicMock()
        mocked_comment.scalar_one_or_none.return_value = None
        self.session.execute.return_value = mocked_comment

        with self.assertRaises(HTTPException) as context:
            await delete_comment(1, self.session, self.user)

        self.assertEqual(context.exception.status_code, 404)
        self.assertEqual(context.exception.detail, detail_message.FILE_NOT_FOUND)

    async def test_get_comment(self):
        """
        The test_get_comment function tests the get_comment function in the comments.py file.
        It does this by creating a mocked comment object, and then using that to test whether or not
        the get_comment function returns an instance of Comment.

        :param self: Represent the instance of the object that is passed to the method when it is called
        :return: A comment object from the database
        :doc-author: Trelent
        """
        id_ = 1
        comment = Comment(id=1, comment="test", image_id=1, user_id=1)
        mocked_comment = MagicMock()
        mocked_comment.scalar_one_or_none.return_value = comment
        self.session.execute.return_value = mocked_comment
        result = await get_comment(id_, self.session)
        self.assertEqual(result, comment)
        self.assertIsInstance(result, Comment)

    async def test_get_nonexistent_comment(self):
        """
        The test_get_nonexistent_comment function tests the get_comment function in the comments.py file.
        The test_get_nonexistent_comment function is a coroutine that takes two arguments: self and id_.
        The test uses an assertRaises context manager to check if an HTTPException is raised when trying to
        retrieve a comment with an ID that does not exist in the database. The status code of this exception should be 404,
        and its detail message should be FILE NOT FOUND.

        :param self: Represent the instance of the class
        :return: 404 status code and file_not_found detail message
        :doc-author: Trelent
        """
        id_ = 1
        mocked_comment = MagicMock()
        mocked_comment.scalar_one_or_none.return_value = None
        self.session.execute.return_value = mocked_comment
        with self.assertRaises(HTTPException) as context:
            await get_comment(id_, self.session)

        self.assertEqual(context.exception.status_code, 404)
        self.assertEqual(context.exception.detail, detail_message.FILE_NOT_FOUND)

    async def test_get_comment_by_image_id(self):

        """
    The test_get_comment_by_image_id function tests the get_comments_by_image function.
    It does this by mocking a list of comments and then comparing that to the result of calling
    get_comments_by image with an image id. If they are equal, then it passes.

    :param self: Represent the instance of the object that is passed to the method when it is called
    :return: A list of comments
    :doc-author: Trelent
    """
        image_id = 1
        comments = [
            Comment(id=1, comment="comment1", image_id=1, user_id=1),
            Comment(id=2, comment="comment2", image_id=1, user_id=2),
            Comment(id=3, comment="comment3", image_id=1, user_id=5),
            Comment(id=4, comment="comment4", image_id=1, user_id=8),
        ]
        mocked_comments = MagicMock()
        mocked_comments.scalars.return_value.all.return_value = comments
        self.session.execute.return_value = mocked_comments
        result = await get_comments_by_image(image_id, self.session)
        self.assertEqual(result, comments)
        self.session.execute.assert_called_once()

    async def test_get_nonexistent_comment_by_image_id(self):

        """
    The test_get_nonexistent_comment_by_image_id function tests the get_comments_by_image function.
    It does this by mocking a session object and then calling the get_comments_by_image function with an image id that is not in the database.
    The mocked session object returns an empty list when queried, which is what we expect to happen if there are no comments for a given image id.

    :param self: Represent the instance of the class
    :return: An empty list
    :doc-author: Trelent
    """
        image_id = 1
        mocked_comments = MagicMock()
        mocked_comments.scalars.return_value.all.return_value = []
        self.session.execute.return_value = mocked_comments
        result = await get_comments_by_image(image_id, self.session)
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
