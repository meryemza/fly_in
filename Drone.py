from typing import List, Optional
from Zone import Hub


class Drone:

    def __init__(self, id: int, current_zone: str) -> None:
        self.id = id
        self.current_zone = current_zone
        self.finished = False
        self.current_index = 0
        self.in_transit = False
        self.next_zone: Optional[Hub] = None
        self.remaining_turns = 0
        self.path: List[str] = []

    # def __repr__(self):
    #     return f"(id={self.id}, current_zone={self.current_zone})"
