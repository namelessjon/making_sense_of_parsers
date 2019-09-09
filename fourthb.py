from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor
from dataclasses import dataclass
from random import randint
import logging
from functools import wraps


grammar = Grammar(
    """
    expression  = elem ws? add_op*
    elem        = dice / number
    dice        = number "d" number
    add_op      = ('+' / '-') ws? expression ws?
    number      = ~"[1-9][0-9]*"
    ws          = ~"[ \t]+"
    """
)


log = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)

@dataclass
class Dice:
    n: int
    sides: int

    def roll(self) -> int:
        log.debug("Rolling %dd%d", self.n, self.sides)
        r = [randint(1, self.sides) for i in range(self.n)]
        log.debug("rolls: %r", r)
        return r


logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)

def log_visitor(func):
    @wraps(func)
    def wrapper(self, node, *args, **kwargs):
        log.debug("%s: %r", func.__name__, node.text)
        return func(self, node, *args, **kwargs)
    return wrapper

from parsimonious.nodes import NodeVisitor

class DiceVisitor(NodeVisitor):
    grammar = grammar
    # other parts unchanged
    @log_visitor
    def visit_number(self, node, visited_children):
        return int(node.text)

    @log_visitor
    def visit_dice(self, node, visited_children):
        number, _, sides = visited_children
        dice = Dice(number, sides)
        roll = dice.roll()
        return sum(roll)

    @log_visitor
    def generic_visit(self, node, visited_children):
        return visited_children or node

    @log_visitor
    def visit_expression(self, node, children):
        # elem ws? add_op*
        left, _, right = children
        for (op, value) in right:
            if op == "+":
                left += value
            elif op == "-":
                left -= value
        return left

    @log_visitor
    def visit_elem(self, node, children):
        # elem / dice
        return children[0]

    @log_visitor
    def visit_add_op(self, node, children):
        # ('+' / '-') ws? expression ws?
        op, _, right, _ = children
        return op[0].text, right

    @log_visitor
    def generic_visit(self, node, node_children):
        return node_children or node
       # print(node)
       #print(node_children)

if __name__ == "__main__":

    mv = DiceVisitor().parse("2d6 + 3")
    print(mv)



#     tree = grammar.parse("9d6")
#   #  print(mv.visit(tree))
#     # print(tree)

#     tree = grammar.parse("(      (     ( 9 + 5 + (3+1)   ) )      )*2")
#     print(tree)
#     print(mv.visit(tree))


#     tree = grammar.parse("1+2*3*4+5")
#     #print(tree)
#   #  print(mv.visit(tree))
#     #print(tree)

#     tree = grammar.parse("3/4/5")
#     #print(tree)
#   #  print(mv.visit(tree))

#     # tree = grammar.parse("9+9d6")
#     # print(tree)

#     # tree = grammar.parse("9+9d6+ 5")
#     # print(tree)

#     tree = grammar.parse("9+2d6+ 5*6")
#  #   print(mv.visit(tree))
#     # print(tree)
