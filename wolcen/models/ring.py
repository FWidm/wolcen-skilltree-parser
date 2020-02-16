from dataclasses import dataclass
from wolcen.models.skill import Skill


@dataclass
class Ring:
    id: str
    name: str
    number: int
    skills: [Skill]

    def __repr__(self):
        return f'Ring({self.name}, {self.number})'

    def reprJSON(self):
        return self.__dict__
