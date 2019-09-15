import cmd
import sys

from parsimonious.exceptions import ParseError

from .dice_visitor import DiceVisitor


class DiceCmd(cmd.Cmd):
    """
    Implements an interactive dice roller

    Dice expressions can be input and rolled at the prompt, then a new prompt
     will be generated
    """
    intro = 'Welcome to the parsimonious roller. '\
            'Input dice expressions to roll. '\
            'Type help or ? to list commands.'
    prompt = '> '

    def default(self, line):
        if line == 'EOF':
            self.do_quit()

        self.do_roll(line)

    def do_roll(self, line):
        """To roll dice, input dice expressions like XdN
Math and backets are supported

e.g
    1d8
    2d6 + 3
    (1d4+2)*2
"""
        try:
            roll = DiceVisitor().parse(line)
            print(roll)
        except ParseError as e:
            print(f"Problem parsing dice roll: {e}")

    def do_quit(self, line=None):
        """Exit the application"""
        print("bye!")
        sys.exit(0)
