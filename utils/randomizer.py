from random import randrange


def random_emoji():
    random_int = randrange(0, 9)
    if random_int == 0:
        return "🥨"
    if random_int == 1:
        return "🍖"
    if random_int == 2:
        return "🍕"
    if random_int == 3:
        return "🥘"
    if random_int == 4:
        return "🥗"
    if random_int == 5:
        return "🥓"
    if random_int == 6:
        return "🥞"
    if random_int == 7:
        return "🍝"
    if random_int == 8:
        return "🍰"
    if random_int == 9:
        return "🍣"


def random_heart():
    random_int = randrange(0, 14)
    if random_int == 0:
        return "🧡"
    if random_int == 1:
        return "💛"
    if random_int == 2:
        return "💚"
    if random_int == 3:
        return "💙"
    if random_int == 4:
        return "💜"
    if random_int == 5:
        return "🤎"
    if random_int == 6:
        return "🖤"
    if random_int == 7:
        return "🤍"
    if random_int == 8:
        return "🧡"
    if random_int == 9:
        return "💗"
    if random_int == 10:
        return "💖"
    if random_int == 11:
        return "💕"
    if random_int == 12:
        return "💓"
    if random_int == 13:
        return "💝"
    if random_int == 14:
        return "❤️‍🔥"
