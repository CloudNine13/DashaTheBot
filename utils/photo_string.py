def make_photo_string(photo_tuple: list[str]) -> str:
    return str(photo_tuple).replace('[', '').replace(']', '').replace("'", "")