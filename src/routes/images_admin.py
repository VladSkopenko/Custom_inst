import cloudinary.uploader
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import (
    UploadFile,
    File,
)
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.ext.asyncio import AsyncSession

from src.conf.config import config
from src.database.db import get_db
from src.repository import images_admin
from src.schemas.images import ImageSchema, ImageResponseSchema

router = APIRouter(prefix='/images', tags=['images'])
cloudinary.config(
    cloud_name=config.CLD_NAME,
    api_key=config.CLD_API_KEY,
    api_secret=config.CLD_API_SECRET,
    secure=True,
)


@router.post('/', response_model=ImageResponseSchema, status_code=status.HTTP_201_CREATED)
async def load_image(body: ImageSchema, file: UploadFile = File(), db: AsyncSession = Depends(get_db)):
    # public_id = f"Py_Web/test"
    # upl = cloudinary.uploader.upload(file.file, public_id=public_id, owerite=True)
    # base_url = cloudinary.CloudinaryImage(public_id).build_url(
    #         width=500, height=800, crop="fill", version=upl.get("version")
    #     )
    # # print(type(base_url))
    # print(base_url)
    base_url = "https://res.cloudinary.com/dir0ipjit/image/upload/c_fill,h_800,w_500/v1714318623/Py_Web/test"
    if base_url:
        image = await images_admin.create_image(body, base_url, db)
        return image

# @router.post('/')
# async def load_image(file: UploadFile = File(), db: AsyncSession = Depends(get_db)):
#
#     public_id = f"Py_Web/test"
#     upl = cloudinary.uploader.upload(file.file, public_id=public_id, owerite=True)
#     base_url = cloudinary.CloudinaryImage(public_id).build_url(
#             width=500, height=800, crop="fill", version=upl.get("version")
#         )
#     print(base_url)
#     return {"massage": "image uploaded"}
