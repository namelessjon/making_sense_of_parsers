from dataclasses import dataclass
import logging
import random

log = logging.getLogger(__name__)

@dataclass
class Dice:
    n: int
    sides: int

    def roll(self) -> int:
        log.debug("Rolling %s", self)
        r = [random.randint(1, self.sides) for i in range(self.n)]
        log.debug("rolls: %r", r)
        return r

    def __str__(self):
        return f"{self.n}d{self.sides}"