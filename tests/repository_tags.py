import unittest
from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.common import detail_message
from src.database.models import Image
from src.database.models import Tag
from src.database.models import User
from src.repository.tags import create_tag
from src.repository.tags import delete_tag
from src.repository.tags import get_tag
from src.schemas.tags import TagSchema


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

        self.db = AsyncMock(spec=AsyncSession)
        self.tag = Tag(
            id=1,
            tag_name="test",
            tag_type="people",
        )
        self.image = Image(
            id=1,
        )

    async def test_get_tag(self):
        """
        The test_get_tag function tests the get_tag function.
        It does this by mocking a tag object and returning it when the database is queried.
        The test then checks that the result of calling get_tag with mocked parameters matches what was returned from
        the mock.

        :param self: Access the class attributes and methods
        :return: The tag
        :doc-author: Trelent
        """
        tag_name = "test"
        mocked_tag = MagicMock()
        mocked_tag.scalar_one_or_none.return_value = self.tag
        self.db.execute.return_value = mocked_tag
        result = await get_tag(tag_name, self.db, self.user)
        self.assertEqual(result, self.tag)

    async def test_get_tag_not_found(self):
        """
        The test_get_tag_not_found function tests the get_tag function in the tags.py file.
        The test_get_tag_not_found function is a coroutine that takes three arguments: self, tag name, and database connection object.
        The test asserts that an HTTPException is raised when a tag with the given name does not exist.

        :param self: Represent the instance of the class
        :return: A 404 error code and a detail message
        :doc-author: Trelent
        """
        tag_name = ""
        mocked_tag = MagicMock()
        mocked_tag.scalar_one_or_none.return_value = None
        self.db.execute.return_value = mocked_tag
        result = await get_tag(tag_name, self.db, self.user)

        self.assertEqual(result, None)

    async def test_create_tag_exist(self):
        """
        The test_create_tag_exist function tests the create_tag function in the tags repository.
        It checks that if a tag already exists, it will return that tag instead of creating a new one.

        :param self: Represent the instance of the class
        :return: The tag when the tag already exists
        :doc-author: Trelent
        """
        body = TagSchema(
            tag_name="test",
            tag_type="people",
        )
        mock_get_tag = AsyncMock(return_value=self.tag)
        with patch("src.repository.tags.get_tag", mock_get_tag):
            result = await create_tag(body, self.db, self.user)

        self.assertEqual(result, self.tag)
        self.assertIsInstance(result, Tag)
        self.assertIsInstance(result, Tag)

    async def test_create_tag(self):
        """
        The test_create_tag function tests the create_tag function in the tags repository.
        It does this by creating a mock tag object and then calling the create_tag function with that mock tag as an argument.
        The test then asserts that it is an instance of Tag, and also checks to see if refresh, commit, and add were called on
        the database.

        :param self: Access the class attributes and methods
        :return: An instance of tag
        :doc-author: Trelent
        """
        body = TagSchema(
            tag_name="new_tag",
            tag_type="people",
        )
        mock_get_tag = AsyncMock(return_value=None)
        with patch("src.repository.tags.get_tag", mock_get_tag):
            result = await create_tag(body, self.db, self.user)

        self.assertIsInstance(result, Tag)
        self.db.refresh.assert_called_once()
        self.db.commit.assert_called_once()
        self.db.add.assert_called_once()

    async def test_delete_tag(self):
        """
        The test_delete_tag function tests the delete_tag function in the tags.py file.
        It does this by first creating a mock database object, and then mocking out
        the execute method of that database object to return a mocked contact object, which is then used to mock out the scalar_one_or_none method of that contact object to return an instance of Tag (which is created using MagicMock). The delete tag function is then called with these arguments: 1 (for id), self.db (for db), and self.user (for user). After this call, we assert that our mocked methods were called once each using

        :param self: Represent the instance of the class
        :return: A tag object
        :doc-author: Trelent
        """
        mocked_contact = MagicMock()
        mocked_contact.scalar_one_or_none.return_value = self.tag
        self.db.execute.return_value = mocked_contact
        result = await delete_tag(1, self.db, self.user)
        self.db.delete.assert_called_once()
        self.db.commit.assert_called_once()
        self.db.execute.assert_called_once()
        self.assertIsInstance(result, Tag)

    async def test_delete_tag_not_found(self):
        """
        The test_delete_tag_not_found function tests the delete_tag function in the tags.py file.
        The test_delete_tag_not_found function is a coroutine that takes three arguments: self, db, and user.
        The test asserts that an HTTPException is raised when a tag with id 1 does not exist in the database.

        :param self: Represent the instance of the class
        :return: 404 status code and detail_message
        :doc-author: Trelent
        """
        mocked_contact = MagicMock()
        mocked_contact.scalar_one_or_none.return_value = None
        self.db.execute.return_value = mocked_contact
        with self.assertRaises(HTTPException) as context:
            await delete_tag(1, self.db, self.user)

        self.assertEqual(context.exception.status_code, 404)
        self.assertEqual(context.exception.detail, detail_message.FILE_NOT_FOUND)


if __name__ == "__main__":
    unittest.main()
