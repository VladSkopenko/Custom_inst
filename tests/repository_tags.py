import unittest
from unittest.mock import AsyncMock
from unittest.mock import MagicMock

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.common import detail_message
from unittest.mock import patch
from src.database.models import Image
from src.database.models import Tag
from src.database.models import User
from src.repository.tags import delete_tag
from src.schemas.tags import TagSchema
from src.repository.tags import create_tag
from src.repository.tags import get_tag


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
        tag_name = "test"
        mocked_tag = MagicMock()
        mocked_tag.scalar_one_or_none.return_value = self.tag
        self.db.execute.return_value = mocked_tag
        result = await get_tag(tag_name, self.db, self.user)
        self.assertEqual(result, self.tag)

    async def test_get_tag_not_found(self):
        tag_name = ""
        mocked_tag = MagicMock()
        mocked_tag.scalar_one_or_none.return_value = None
        self.db.execute.return_value = mocked_tag
        with self.assertRaises(HTTPException) as context:
            await get_tag(tag_name, self.db, self.user)

        self.assertEqual(context.exception.status_code, 404)
        self.assertEqual(context.exception.detail, detail_message.FILE_NOT_FOUND)

    async def test_create_tag_exist(self):
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
        mocked_contact = MagicMock()
        mocked_contact.scalar_one_or_none.return_value = self.tag
        self.db.execute.return_value = mocked_contact
        result = await delete_tag(1, self.db, self.user)
        self.db.delete.assert_called_once()
        self.db.commit.assert_called_once()
        self.db.execute.assert_called_once()
        self.assertIsInstance(result, Tag)

    async def test_delete_tag_not_found(self):
        mocked_contact = MagicMock()
        mocked_contact.scalar_one_or_none.return_value = None
        self.db.execute.return_value = mocked_contact
        with self.assertRaises(HTTPException) as context:
            await delete_tag(1, self.db, self.user)

        self.assertEqual(context.exception.status_code, 404)
        self.assertEqual(context.exception.detail, detail_message.FILE_NOT_FOUND)


if __name__ == "__main__":
    unittest.main()
