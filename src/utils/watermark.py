from io import BytesIO
from urllib.request import urlopen

import cloudinary.uploader
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


async def watermark(url: str, user_nickname: str) -> str:
    img = Image.open(urlopen(url)).convert('RGBA')
    txt = Image.new('RGBA', img.size, (255, 255, 255, 0))
    fnt = ImageFont.truetype(font="arial.ttf", size=80)
    d = ImageDraw.Draw(txt)
    d.text((10, 10), f"{user_nickname}", font=fnt, fill=(255, 255, 255, 128))
    out = Image.alpha_composite(img, txt)
    out_buffer = BytesIO()
    out.save(out_buffer, "PNG")
    out_buffer.seek(0)
    picture_name = url.split('/')[-1].replace('%', ' ')
    public_id_pillow = f"Project_Web_images/Watermark/{picture_name}"
    upl = cloudinary.uploader.upload(out_buffer, public_id=public_id_pillow, overwrite=True)
    pillow_url = cloudinary.CloudinaryImage(public_id_pillow).build_url(version=upl.get("version"))
    return pillow_url
