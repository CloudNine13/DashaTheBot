import asyncio
import cloudinary

from asyncio import gather
from io import BytesIO
from aiohttp import ClientSession
from telegram import InputMediaPhoto


def download_images(image_url_list_as_string: str):
    image_url_list = image_url_list_as_string.split(", ")
    image_url_list = [cloudinary.utils.cloudinary_url(image)[0] for image in
                      image_url_list]  # ('...cloudinary.com/.../4e5d...', {})
    event_loop = asyncio.new_event_loop()
    task = get_session_data(image_url_list)
    images = event_loop.run_until_complete(task)
    return images


async def get_session_data(image_list: list[str]):
    async with ClientSession() as session:
        tasks = [fetch_images(session, image_url) for image_url in image_list]
        image_data = await gather(*tasks)
        return image_data


async def fetch_images(session, image_url):
    async with session.get(image_url) as response:
        data = await response.read()
        if data:
            return InputMediaPhoto(media=BytesIO(data))
