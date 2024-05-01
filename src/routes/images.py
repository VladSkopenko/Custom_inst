from io import BytesIO

import cloudinary.uploader
import qrcode
from fastapi import APIRouter, Depends, HTTPException, status, Path
from fastapi import (
    UploadFile,
    File,
)
from sqlalchemy.ext.asyncio import AsyncSession

from src.conf.config import config
from src.database.db import get_db
from src.database.models import User
from src.repository import images as images_repository
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
    base_url = cloudinary.CloudinaryImage(public_id).build_url(version=upl.get("version"))
    print(base_url)

    image = await images_repository.create_image(body, base_url, db, current_user)
    return image


@router.get('/all', response_model=list[ImageResponseSchema], status_code=status.HTTP_200_OK)
async def get_all_images(db: AsyncSession = Depends(get_db)):
    images = await images_repository.get_all_images(db)
    if images is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Images not found")
    return images


@router.get('/{image_id}', response_model=ImageResponseSchema, status_code=status.HTTP_200_OK)
async def get_image(image_id: int = Path(ge=1), db: AsyncSession = Depends(get_db)):
    image = await images_repository.get_image(image_id, db)
    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Image with id {image_id} not found')
    return image


@router.put('/{image_id}', response_model=ImageResponseSchema, status_code=status.HTTP_200_OK)
async def update_image(image_id: int = Path(ge=1),
                       body: ImageSchema = Depends(),
                       db: AsyncSession = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)
                       ):
    image = await images_repository.update_image(image_id, body, db, current_user)
    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Image with id {image_id} not found')
    return image


@router.delete('/{image_id}', response_model=ImageResponseSchema, status_code=status.HTTP_200_OK)
async def delete_image(image_id: int = Path(ge=1),
                       db: AsyncSession = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)
                       ):
    image = await images_repository.delete_image(image_id, db, current_user)
    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Image with id {image_id} not found')
    return image


@router.post('/transform/grayscale/{image_id}', response_model=ImageResponseSchema, status_code=status.HTTP_200_OK)
async def create_transform_image(image_id: int = Path(ge=1),
                                 db: AsyncSession = Depends(get_db),
                                 current_user: User = Depends(auth_service.get_current_user)
                                 ):
    base_url = await images_repository.get_base_url(image_id, db, current_user)
    list_base_url = base_url.split('/')
    public_id = f"{list_base_url[-2]}/{list_base_url[-1]}"
    transform = {'effect': 'grayscale'}
    tr_url = cloudinary.CloudinaryImage(public_id).build_url(**transform)

    image = await images_repository.transform_image(image_id, tr_url, db, current_user)
    return image


@router.post('/transform/sepia/{image_id}', response_model=ImageResponseSchema, status_code=status.HTTP_200_OK)
async def create_transform_image(image_id: int = Path(ge=1),
                                 db: AsyncSession = Depends(get_db),
                                 current_user: User = Depends(auth_service.get_current_user)
                                 ):
    base_url = await images_repository.get_base_url(image_id, db, current_user)
    list_base_url = base_url.split('/')
    public_id = f"{list_base_url[-2]}/{list_base_url[-1]}"
    transform = {'effect': 'sepia'}
    tr_url = cloudinary.CloudinaryImage(public_id).build_url(**transform)

    image = await images_repository.transform_image(image_id, tr_url, db, current_user)
    return image


@router.post('/transform/oil_paint/{image_id}', response_model=ImageResponseSchema)
async def create_transform_image(image_id: int = Path(ge=1),
                                 db: AsyncSession = Depends(get_db),
                                 current_user: User = Depends(auth_service.get_current_user)
                                 ):
    base_url = await images_repository.get_base_url(image_id, db, current_user)
    list_base_url = base_url.split('/')
    public_id = f"{list_base_url[-2]}/{list_base_url[-1]}"
    transform = {'effect': 'oil_paint'}
    tr_url = cloudinary.CloudinaryImage(public_id).build_url(**transform)

    image = await images_repository.transform_image(image_id, tr_url, db, current_user)
    return image


@router.post('/qr_code/{image_id}', response_model=ImageResponseSchema, status_code=status.HTTP_200_OK)
async def create_qr_code(image_id: int = Path(ge=1),
                         db: AsyncSession = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)
                         ):
    transform_url = await images_repository.get_transform_url(image_id, db, current_user)

    qr_name = transform_url.split('/')[-1].replace('%', ' ')
    img = qrcode.make(transform_url)

    img_buffer = BytesIO()
    img.save(img_buffer, "PNG")
    img_buffer.seek(0)

    public_id = f"Project_Web_images/QR/{qr_name}"
    upl = cloudinary.uploader.upload(img_buffer, public_id=public_id, overwrite=True)
    qr_url = cloudinary.CloudinaryImage(public_id).build_url(version=upl.get("version"))
    print(qr_url)

    image = await images_repository.qr_code(image_id, qr_url, db, current_user)
    return image
