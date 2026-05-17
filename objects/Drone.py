from typing import List, Optional
from .Zone import Hub


class Drone:

    def __init__(self, id: int, current_zone: str) -> None:
        self.id = id
        self.current_zone = current_zone
        self.path: List[str] = []
        self.finished = False
        self.current_index = 0
        self.in_transit = False
        self.next_zone: Optional[Hub] = None
        self.remaining_turns = 0

    def __repr__(self):
        return f"(id={self.id}, current_zone={self.current_zone})"

    # __repr__ is a special method in Python used to define how an object should be represented as a string when it is printed
    # By default, when you print an object, Python shows a generic message that includes the class name and a memory address,
    #  __repr__,  can control this output For exampl, instead of seeing something like <Drone object at 0x...>,
    # you can display Drone(id=1, zone=A),
