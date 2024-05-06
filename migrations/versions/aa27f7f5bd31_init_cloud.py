""" init cloud

Revision ID: aa27f7f5bd31
Revises: 
Create Date: 2024-05-06 16:18:16.709161

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aa27f7f5bd31'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('image_m2m_tag_image_id_fkey', 'image_m2m_tag', type_='foreignkey')
    op.drop_constraint('image_m2m_tag_tag_id_fkey', 'image_m2m_tag', type_='foreignkey')
    op.create_foreign_key(None, 'image_m2m_tag', 'images', ['image_id'], ['id'])
    op.create_foreign_key(None, 'image_m2m_tag', 'tags', ['tag_id'], ['id'])
    op.drop_column('image_m2m_tag', 'id')
    op.create_unique_constraint(None, 'images_likes', ['user_id', 'image_id'])
    op.drop_column('images_likes', 'id')
    op.drop_constraint('tags_tag_name_key', 'tags', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('tags_tag_name_key', 'tags', ['tag_name'])
    op.add_column('images_likes', sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False))
    op.drop_constraint(None, 'images_likes', type_='unique')
    op.add_column('image_m2m_tag', sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False))
    op.drop_constraint(None, 'image_m2m_tag', type_='foreignkey')
    op.drop_constraint(None, 'image_m2m_tag', type_='foreignkey')
    op.create_foreign_key('image_m2m_tag_tag_id_fkey', 'image_m2m_tag', 'tags', ['tag_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('image_m2m_tag_image_id_fkey', 'image_m2m_tag', 'images', ['image_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###