from dataclasses import dataclass
from UTILITIES.ENUMS import EventType
from enum import Enum, auto


@dataclass
class AtBatToken:
    batter: object 
    pitcher: object


@dataclass
class AtBatResult:
    events: list[object]


@dataclass
class AtBatEvent:
    event_type: EventType
    event_code: Enum
    event_data: dict
