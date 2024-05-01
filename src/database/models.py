import enum
from datetime import date

from sqlalchemy import String, ForeignKey, DateTime, func, Enum, Boolean, Table, Column, Integer, Text, text
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.orm import Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Role(enum.Enum):
    admin: str = "admin"
    moderator: str = "moderator"
    user: str = "user"


class Gender(enum.Enum):
    male: str = "male"
    female: str = "female"
    other: str = "other"


class TagType(enum.Enum):
    sport: str = "sport"
    animals: str = "animals"
    nature: str = "nature"
    people: str = "people"
    architecture: str = "architecture"





class Image(Base):
    __tablename__ = "images"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    user: Mapped["User"] = relationship("User", backref="images", lazy="joined")
    title: Mapped[str] = mapped_column(String(50), nullable=True)
    base_url: Mapped[str] = mapped_column(String(255), nullable=True)
    transform_url: Mapped[str] = mapped_column(String(255), nullable=True)
    description: Mapped[text] = mapped_column(Text, nullable=True)
    qr_url: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[date] = mapped_column(
        "created_at", DateTime, default=func.now(), nullable=True
    )
    updated_at: Mapped[date] = mapped_column(
        "updated_at", DateTime, default=func.now(), onupdate=func.now(), nullable=True
    )
    tags = relationship("Tag", secondary="image_m2m_tag", back_populates="images", lazy="select")

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nickname: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[Enum] = mapped_column('role', Enum(Role), default=Role.user)
    refresh_token: Mapped[str] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column('is_active', Boolean, default=True)
    confirmed: Mapped[bool] = mapped_column('confirmed', Boolean, default=False)
    created_at: Mapped[date] = mapped_column('created_at', DateTime, default=func.now())
    updated_at: Mapped[date] = mapped_column('updated_at', DateTime, default=func.now(), onupdate=func.now(),
                                             nullable=True)


class Comment(Base):
    __tablename__ = 'comments'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=True)
    image_id: Mapped[int] = mapped_column(ForeignKey('images.id'), nullable=True)
    comment: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[date] = mapped_column('created_at', DateTime, default=func.now())
    updated_at: Mapped[date] = mapped_column('updated_at', DateTime, default=func.now(), onupdate=func.now(),
                                             nullable=True)
    answer: Mapped[str] = mapped_column(String(255), nullable=True)

    image: Mapped["Image"] = relationship("Image", backref="comments")
    user: Mapped["User"] = relationship("User", backref="comments")


class UserInfo(Base):
    __tablename__ = 'users_info'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    born_date: Mapped[date] = mapped_column('born_date', DateTime, nullable=True)
    avatar: Mapped[str] = mapped_column(String(255), nullable=True)
    gender: Mapped[Enum] = mapped_column('sex', Enum(Gender), nullable=True)
    created_at: Mapped[date] = mapped_column('created_at', DateTime, default=func.now())
    updated_at: Mapped[date] = mapped_column('updated_at', DateTime, default=func.now(), onupdate=func.now(),
                                             nullable=True)


class BanList(Base):
    __tablename__ = 'ban_list'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    banned_at: Mapped[date] = mapped_column('created_at', DateTime, default=func.now(), nullable=True)
    unbanned_at: Mapped[date] = mapped_column('updated_at', DateTime, default=func.now(), onupdate=func.now(),
                                              nullable=True)


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    tag_name: Mapped[str] = mapped_column(String(60), nullable=False)
    tag_type: Mapped[Enum] = mapped_column("tag_type", Enum(TagType), nullable=False)
    images = relationship("Image", secondary="image_m2m_tag", back_populates="tags", lazy="select")


class ImageLike(Base):
    __tablename__ = 'images_likes'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    image_id: Mapped[int] = mapped_column(ForeignKey('images.id'))
    grade: Mapped[int] = mapped_column(Integer, nullable=False)


image_m2m_tag = Table(
    "image_m2m_tag",
    Base.metadata,
    Column("image_id", Integer, ForeignKey("images.id")),
    Column("tag_id", Integer, ForeignKey("tags.id")),
)
