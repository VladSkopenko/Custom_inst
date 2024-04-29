import unittest

from unittest.mock import AsyncMock
from unittest.mock import MagicMock

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from src.database.models import Comment
from src.database.models import Image
from src.database.models import User
from src.repository.comments import create_comment
from src.repository.comments import edit_comment
from src.repository.comments import delete_comment
from src.schemas.comments import CommentSchema
from src.common import detail_message


class TestAsyncContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self) -> None:
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
        )

    async def test_create_contact(self):
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

    async def test_delete_comment_from_user_role(self):
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
        mocked_comment = MagicMock()
        mocked_comment.scalar_one_or_none.return_value = None
        self.session.execute.return_value = mocked_comment

        with self.assertRaises(HTTPException) as context:
            await delete_comment(1, self.session, self.user)

        self.assertEqual(context.exception.status_code, 404)
        self.assertEqual(context.exception.detail, detail_message.FILE_NOT_FOUND)


if __name__ == "__main__":
    unittest.main()