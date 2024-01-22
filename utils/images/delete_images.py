import cloudinary.api


def delete_images(image_list: list[str]):
    cloudinary.api.delete_resources(image_list)
