import uuid
from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Movie:
    """Датакласс для хранения считанных данных по каждому обновленному фильму"""

    id: uuid.UUID = field(default_factory=uuid.uuid4)
    title: str = field(default="")
    description: str = field(default="")
    rating: float = field(default=0.0)
    genres: List[str] = field(default_factory=list)
    director: str = field(default="")
    actors: List[Dict[str, str]] = field(default_factory=list)
    writers: List[Dict[str, str]] = field(default_factory=list)
