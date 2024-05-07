import pickle
from datetime import datetime
from datetime import timedelta
from typing import Optional

import pytz
import redis
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose import JWTError
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from src.common import detail_message
from src.conf.config import config
from src.database.db import get_db
from src.repository import users as repository_users


class Auth:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY = config.SECRET_KEY_JWT
    ALGORITHM = config.ALGORITHM

    cache = redis.Redis(host=config.REDIS_DOMAIN, port=config.REDIS_PORT, password=config.REDIS_PASSWORD, db=0)

    def verify_password(self, plain_password, hashed_password):
        """
        The verify_password function takes a plain-text password and the hashed version of that password,
            and returns True if they match, False otherwise. This is used to verify that the user's login
            credentials are correct.
        
        :param self: Represent the instance of the class
        :param plain_password: Store the password that is entered by the user
        :param hashed_password: Compare the hashed password in the database with the plain text password entered by user
        :return: A boolean value
        :doc-author: Trelent
        """
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str):
        """
        The get_password_hash function takes a password as input and returns the hash of that password.
            The function uses the pwd_context object to generate a hash from the given password.
        
        :param self: Represent the instance of the class
        :param password: str: Pass in the password that you want to hash
        :return: A string that is the hashed version of the password
        :doc-author: Trelent
        """
        return self.pwd_context.hash(password)

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

    async def create_access_token(
        self, data: dict, expires_delta: Optional[float] = None
    ):
        """
        The create_access_token function creates a new access token.
            Args:
                data (dict): The data to be encoded in the JWT.
                expires_delta (Optional[float]): A timedelta object representing how long the token should last for. Defaults to 15 minutes if not specified.
     
        :param self: Represent the instance of the class
        :param data: dict: Pass the data that will be encoded into the token
        :param expires_delta: Optional[float]: Set the expiration time for the access token
        :return: A token that is encoded with the data you pass to it
        :doc-author: Trelent
        """

        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(pytz.UTC) + timedelta(seconds=expires_delta)
        else:
            expire = datetime.now(pytz.UTC) + timedelta(minutes=15)
        to_encode.update(
            {"iat": datetime.now(pytz.UTC), "exp": expire, "scope": "access_token"}
        )
        encoded_access_token = jwt.encode(
            to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM
        )
        return encoded_access_token

    async def create_refresh_token(
        self, data: dict, expires_delta: Optional[float] = None
    ):
        """
        Create refresh token.

        :param data: data
        :param expires_delta: expiration time
        :return: refresh token
        """

        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(pytz.UTC) + timedelta(seconds=expires_delta)
        else:
            expire = datetime.now(pytz.UTC) + timedelta(days=7)
        to_encode.update(
            {"iat": datetime.now(pytz.UTC), "exp": expire, "scope": "refresh_token"}
        )
        encoded_refresh_token = jwt.encode(
            to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM
        )
        return encoded_refresh_token

    async def decode_refresh_token(self, refresh_token: str):
        """

        The decode_refresh_token function is used to decode the refresh token.
            The function will raise an HTTPException if the token is invalid or has expired.
            If the token is valid, it will return a string with the email address of 
            user who owns that refresh_token.
        
        :param self: Represent the instance of a class
        :param refresh_token: str: Pass in the refresh token that is sent to the server
        :return: The email address of the user who requested a new access token
        :doc-author: Trelent
        """

        try:
            payload = jwt.decode(
                refresh_token, self.SECRET_KEY, algorithms=[self.ALGORITHM]
            )
            if payload["scope"] == "refresh_token":
                email = payload["sub"]
                return email
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=detail_message.INVALI_SCOPE_FOR_TOKEN
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=detail_message.COULD_NOT_VALIDATE_CREDENTIALS
            )

    async def get_current_user(
        self, token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
    ):
        """

        The get_current_user function is a dependency that will be used in the
            protected endpoints. It takes a token and returns the user object if it's valid,
            otherwise raises an HTTPException with status code 401 (Unauthorized).
        
        :param self: Denote that the get_current_user function is a member of the user class
        :param token: str: Get the token from the request header
        :param db: AsyncSession: Get the database session
        :return: A user object, which is used in the following function:
        :doc-author: Trelent
        """

        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail_message.COULD_NOT_VALIDATE_CREDENTIALS,
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload["scope"] == "access_token":
                email = payload["sub"]
                if email is None:
                    raise credentials_exception
            else:
                raise credentials_exception
        except JWTError as e:
            raise credentials_exception

        user_hash = str(email)

        user = self.cache.get(user_hash)

        if user is None:
            user = await repository_users.get_user_by_email(email, db)
            if user is None:
                raise credentials_exception
            self.cache.set(user_hash, pickle.dumps(user))
            self.cache.expire(user_hash, 300)
        else:            
            user = pickle.loads(user)
        return user

    def create_email_token(self, data: dict):
        """
        Create email token.

        :param data: data
        :return: email token
        """

        to_encode = data.copy()
        expire = datetime.now(pytz.UTC) + timedelta(days=1)
        to_encode.update({"iat": datetime.now(pytz.UTC), "exp": expire})
        token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return token

    async def get_email_from_token(self, token: str):
        """

        The get_email_from_token function takes a token as an argument and returns the email address associated with that token.
        The function uses the jwt library to decode the token, which is then used to retrieve the email address from within it.
        
        :param self: Represent the instance of the class
        :param token: str: Pass the token from the user to this function
        :return: The email associated with the token
        :doc-author: Trelent
        """

        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            email = payload["sub"]
            return email
        except JWTError as e:            
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=detail_message.INVALID_TOKEN_EMAIL_VERIFYCATION
            )


auth_service = Auth()
