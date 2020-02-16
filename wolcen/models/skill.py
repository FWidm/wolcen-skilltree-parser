from dataclasses import dataclass, field


@dataclass(init=True, repr=True)
class Skill:
    id: str
    name: str
    rarity: int
    category: str
    max_level: int
    angle: float
    pos: float
    previous_names: [str]
    effects: [str]
    neighbours: [str] = field(init=False)

    def __post_init__(self):
        self.neighbours = self.previous_names.split(',')

    def find_neighbours(self, skills: ['Skill']):
        return [skill for skill in skills if skill.name in self.neighbours]

    def reprJSON(self):
        return self.__dict__
