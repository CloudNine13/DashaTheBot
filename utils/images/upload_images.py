import cloudinary.uploader
import utils.config as configurations


def upload_images():
    for photo in configurations.photo_list:
        if photo is None:
            continue
        cloudinary.uploader.upload(photo['file'], public_id=photo['public_id'])
        del photo
