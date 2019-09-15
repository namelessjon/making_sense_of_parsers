import argparse

from .dice_visitor import DiceVisitor


def cli(args=None):
    desc = """\
Dice roller for standard dice rolls

To roll dice, input dice expressions like XdN
Math on dice results is supported.

e.g 1d8, 2d6 + 3, (1d4+2)*2
    """

    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("dice", help="Dice to roll")

    parsed = parser.parse_args(args)

    if parsed.dice:
        result = DiceVisitor().parse(parsed.dice)
        print(f"Rolling {parsed.dice} => {result}")

