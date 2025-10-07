"""Domain models for fixtures."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Fixture:
    """Represents a single fixture."""

    date: datetime
    venue: str
    league: str
    home_team: str
    away_team: str


@dataclass
class FixturesUpdate:
    """Represents a fixtures update."""

    date: datetime
    venue: str
    fixtures: list[Fixture]
    source: str
