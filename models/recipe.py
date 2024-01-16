from dataclasses import dataclass, field


@dataclass
class Recipe:
    index: int = 0
    max_index: int = 3
    name: str = None
    recipe_type: str = None
    description: str = None
    photo_path: list[str] = field(default_factory=list)
