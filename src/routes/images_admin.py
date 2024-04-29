import cloudinary.uploader
from fastapi import APIRouter, Depends, HTTPException, status, Path
from fastapi import (
    UploadFile,
    File,
)
from sqlalchemy.ext.asyncio import AsyncSession

from src.conf.config import config
from src.database.db import get_db
from src.database.models import Image, User
from src.repository import images
from src.schemas.images import ImageSchema, ImageResponseSchema
from src.services.auth import auth_service


router = APIRouter(prefix='/images', tags=['images'])
cloudinary.config(
    cloud_name=config.CLOUDINARY_NAME,
    api_key=config.CLOUDINARY_API_KEY,
    api_secret=config.CLOUDINARY_API_SECRET,
    secure=True,
)


@router.post('/', response_model=ImageResponseSchema, status_code=status.HTTP_201_CREATED)
async def load_image(body: ImageSchema = Depends(),
                     file: UploadFile = File(...),
                     db: AsyncSession = Depends(get_db),
                     current_user: User = Depends(auth_service.get_current_user)
):

    public_id = f"Project_Web_images/{body.title}"
    upl = cloudinary.uploader.upload(file.file, public_id=public_id, owerite=True)
    base_url = cloudinary.CloudinaryImage(public_id).build_url(
            width=500, height=800, crop="fill", version=upl.get("version")
        )
    print(base_url)

    image = await images.create_image(body, base_url, db, current_user)
    return image


@router.get('/{image_id}', response_model=ImageResponseSchema)
async def get_image(image_id: int = Path(ge=1), db: AsyncSession = Depends(get_db)):
    image = await images.get_image(image_id, db)
    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Image with id {image_id} not found')
    return image


@router.put('/{image_id}', response_model=ImageResponseSchema)
async def update_image(image_id: int = Path(ge=1),
                       body: ImageSchema = Depends(),
                       db: AsyncSession = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)
):
    image = await images.update_image(image_id, body, db, current_user)
    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Image with id {image_id} not found')
    return image


@router.delete('/{image_id}', response_model=ImageResponseSchema)
async def delete_image(image_id: int = Path(ge=1),
                       db: AsyncSession = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)
):
    image = await images.delete_image(image_id, db, current_user)
    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Image with id {image_id} not found')
    return image
