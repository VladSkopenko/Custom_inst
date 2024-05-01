import unittest
from unittest.mock import AsyncMock
from unittest.mock import MagicMock

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.common import detail_message

from src.database.models import Image
from src.database.models import Tag
from src.database.models import User
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
        result = await get_tag(tag_name, self.db, self.user)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
