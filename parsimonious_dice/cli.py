import argparse

from parsimonious.exceptions import ParseError

from .dice_visitor import DiceVisitor
from .cmd import DiceCmd


def cli(args=None):
    desc = """\
Dice roller for standard dice rolls

To roll dice, dice expressions like XdN can be provided on the command line.
Math on dice results is supported.

e.g 1d8, 2d6 + 3, (1d4+2)*2

If no arguments are provided, an interactive shell is started
    """

    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("dice", help="Dice to roll", nargs='*')

    parsed = parser.parse_args(args)

    for dice in parsed.dice:
        try:
            result = DiceVisitor().parse(dice)
            print(f"Rolling {dice} => {result}")
        except ParseError as e:
            print(f"Problem parsing dice roll: {e}")

    if not parsed.dice:
        cmd = DiceCmd()
        cmd.cmdloop()

