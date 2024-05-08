from io import BytesIO
from typing import Optional

import cloudinary.uploader
import qrcode
from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import HTTPException
from fastapi import Path
from fastapi import Query
from fastapi import status
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from src.conf.config import config
from src.database.db import get_db
from src.database.models import User
from src.repository import images as images_repository
from src.repository.tags_images import get_data_image
from src.schemas.images import ImageResponseSchema
from src.schemas.images import ImageSchema
from src.services.auth import auth_service
from src.utils.logger import handler
from src.utils.logger import logger
from src.utils.watermark import watermark

logger.addHandler(handler)


router = APIRouter(prefix="/images", tags=["images"])
cloudinary.config(
    cloud_name=config.CLOUDINARY_NAME,
    api_key=config.CLOUDINARY_API_KEY,
    api_secret=config.CLOUDINARY_API_SECRET,
    secure=True,
)


@router.post(
    "/", response_model=ImageResponseSchema, status_code=status.HTTP_201_CREATED
)
async def load_image(
    body: ImageSchema = Depends(),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The load_image function creates a new image in the database.

    :param body: ImageSchema: Get the data from the request body
    :param file: UploadFile: Upload the image
    :param db: AsyncSession: Pass the database session
    :param current_user: User: Get the current user
    :return: A JSON response with the image data
    """

    public_id = f"Project_Web_images/{body.title}"
    upl = cloudinary.uploader.upload(file.file, public_id=public_id, owerite=True)
    base_url = cloudinary.CloudinaryImage(public_id).build_url(
        version=upl.get("version")
    )
    logger.info(body)
    logger.info(file)
    image = await images_repository.create_image(body, base_url, db, current_user)
    return image


@router.get("/all", status_code=status.HTTP_200_OK)
async def get_all_images(
    page: Optional[int] = Query(None, ge=1),
    per_page: Optional[int] = Query(None, ge=1),
    db: AsyncSession = Depends(get_db),
):
    """
    The get_all_images function returns a list of all images in the database.

    :param page: Optional[int]: Specify the page number
    :param per_page: Optional[int]: Limit the number of images returned
    :param db: AsyncSession: Pass the database session
    :return: A list of images
    """

    images = await images_repository.get_all_images(db)
    if images is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Images not found"
        )

    if page is None or per_page is None:
        all_image_data = []
        for image in images:
            data_image = await get_data_image(image.id, db)
            all_image_data.append(data_image)
        return all_image_data

    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    paginated_images = images[start_index:end_index]

    paginated_image_data = []
    for image in paginated_images:
        data_image = await get_data_image(image.id, db)
        paginated_image_data.append(data_image)

    return paginated_image_data

@router.get("/search_images")
async def search_images(keyword: str, db: AsyncSession = Depends(get_db)):
    images = await images_repository.search_images(keyword, db)
    return images


@router.get("/{image_id}", status_code=status.HTTP_200_OK)
async def get_image(image_id: int = Path(ge=1), db: AsyncSession = Depends(get_db)):
    """
    The get_image function returns the image with the specified id.

    :param image_id: int: Get the image id from the url
    :param db: AsyncSession: Pass the database session
    :return: A single image object
    """

    data_image = await get_data_image(image_id, db)
    if data_image is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Image with id {image_id} not found",
        )
    return data_image


@router.put(
    "/{image_id}", response_model=ImageResponseSchema, status_code=status.HTTP_200_OK
)
async def update_image(
    image_id: int = Path(ge=1),
    body: ImageSchema = Depends(),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The update_image function updates an image in the database.

    :param image_id: int: Specify the image id
    :param body: ImageSchema: Get the data from the request body
    :param db: AsyncSession: Pass the database session
    :param current_user: User: Get the current user
    :return: An image JSON response
    """

    image = await images_repository.update_image(image_id, body, db, current_user)
    if image is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Image with id {image_id} not found",
        )
    return image


@router.delete(
    "/{image_id}", response_model=ImageResponseSchema, status_code=status.HTTP_200_OK
)
async def delete_image(
    image_id: int = Path(ge=1),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The delete_image function deletes an image from the database.

    :param image_id: int: Specify the image id
    :param db: AsyncSession: Pass the database session
    :param current_user: User: Get the current user
    :return: An image JSON response which was deleted
    """

    image = await images_repository.delete_image(image_id, db, current_user)
    if image is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Image with id {image_id} not found",
        )
    return image


@router.post(
    "/transform/grayscale/{image_id}",
    response_model=ImageResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def create_transform_image(
    image_id: int = Path(ge=1),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The create_transform_image function transforms an image to grayscale.

    :param image_id: int: Specify the image id
    :param db: AsyncSession: Pass the database session
    :param current_user: User: Get the current user
    :return: An image JSON response with transformed url
    """

    base_url = await images_repository.get_base_url(image_id, db, current_user)
    list_base_url = base_url.split("/")
    public_id = f"{list_base_url[-2]}/{list_base_url[-1]}"
    transform = {"effect": "grayscale"}
    tr_url = cloudinary.CloudinaryImage(public_id).build_url(**transform)

    image = await images_repository.transform_image(image_id, tr_url, db, current_user)
    return image


@router.post(
    "/transform/sepia/{image_id}",
    response_model=ImageResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def create_transform_image(
    image_id: int = Path(ge=1),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The create_transform_image function transforms an image to sepia.

    :param image_id: int: Specify the image id
    :param db: AsyncSession: Pass the database session
    :param current_user: User: Get the current user
    :return: An image JSON response with transformed url
    """

    base_url = await images_repository.get_base_url(image_id, db, current_user)
    list_base_url = base_url.split("/")
    public_id = f"{list_base_url[-2]}/{list_base_url[-1]}"
    transform = {"effect": "sepia"}
    tr_url = cloudinary.CloudinaryImage(public_id).build_url(**transform)

    image = await images_repository.transform_image(image_id, tr_url, db, current_user)
    return image


@router.post("/transform/oil_paint/{image_id}", response_model=ImageResponseSchema)
async def create_transform_image(
    image_id: int = Path(ge=1),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The create_transform_image function transforms an image to oil paint.

    :param image_id: int: Specify the image id
    :param db: AsyncSession: Pass the database session
    :param current_user: User: Get the current user
    :return: An image JSON response with transformed url
    """

    base_url = await images_repository.get_base_url(image_id, db, current_user)
    list_base_url = base_url.split("/")
    public_id = f"{list_base_url[-2]}/{list_base_url[-1]}"
    transform = {"effect": "oil_paint"}
    tr_url = cloudinary.CloudinaryImage(public_id).build_url(**transform)

    image = await images_repository.transform_image(image_id, tr_url, db, current_user)
    return image


@router.post(
    "/transform/watermark/{image_id}",
    response_model=ImageResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def create_transform_image(
    image_id: int = Path(ge=1),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The create_transform_image function transforms an image to watermark.

    :param image_id: int: Specify the image id
    :param db: AsyncSession: Pass the database session
    :param current_user: User: Get the current user
    :return: An image JSON response with transformed url
    """

    url = await images_repository.get_transform_url(image_id, db, current_user)

    tr_url = await watermark(url, current_user.nickname)
    image = await images_repository.transform_image(image_id, tr_url, db, current_user)
    return image


@router.post(
    "/qr_code/{image_id}",
    response_model=ImageResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def create_qr_code(
    image_id: int = Path(ge=1),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The create_qr_code function creates a qr code for an image.

    :param image_id: int: Specify the image id
    :param db: AsyncSession: Pass the database session
    :param current_user: User: Get the current user
    :return: An image JSON response with qr code
    """

    transform_url = await images_repository.get_transform_url(
        image_id, db, current_user
    )

    qr_name = transform_url.split("/")[-1].replace("%", " ")
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

