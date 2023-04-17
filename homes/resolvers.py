from typing import List
from .types import Home, LGA, Location
from .models import StateType

def get_homes() -> List[Home]:
    homes: List[Home] = []
    state_1 = StateType(id=1, name="This", lgas=[])
    lga_1 = LGA(id=1, name="My LGA", state=state_1)
    loc_1 = Location(id=1, state=state_1, lga=lga_1)
    loc_2 = Location(id=2, state=state_1, lga=lga_1)
    home_1 = Home(id=1, location=loc_1, room_count=0, images=[])
    home_2 = Home(id=2, location=loc_2, room_count=2, images=[])
    homes.append(home_1)
    homes.append(home_2)
    return homes
