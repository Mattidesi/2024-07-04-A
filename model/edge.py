from datetime import datetime
from dataclasses import dataclass

from model.sighting import Sighting


@dataclass
class Edge:
    s1: Sighting
    data1: datetime
    s2: Sighting
    data2: datetime