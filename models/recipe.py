from dataclasses import dataclass, field


@dataclass
class Recipe:
    index: int = 0
    max_index: int = 3
    name: str = field(init=False)
    recipe_type: int = field(init=False)
    description: str = field(init=False)
    photo_path: list = field(init=False)
