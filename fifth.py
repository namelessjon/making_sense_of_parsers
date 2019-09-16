from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor
from dataclasses import dataclass
from random import randint
import logging


grammar = Grammar(
    """
    statement   = expression ws add_op*
    expression  = elem ws mul_op*
    elem        = nested / dice / number
    nested      = '(' ws statement ws ')'
    dice        = number "d" number
    add_op      = ('+' / '-') ws expression ws
    mul_op      = ('*' / '/') ws elem ws
    number      = ~"[1-9][0-9]*"
    ws          = (" " / "\t")*
    """
)


log = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)

@dataclass
class Dice:
    n: int
    sides: int

    def roll(self) -> int:
        log.debug("Rolling %s", self)
        r = [randint(1, self.sides) for i in range(self.n)]
        log.debug("rolls: %r", r)
        return r

    def __str__(self):
        return f"{self.n}d{self.sides}"


logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)

from parsimonious.nodes import NodeVisitor

class DiceVisitor(NodeVisitor):
    grammar = grammar
    def visit_number(self, node, visited_children):
        return int(node.text)

    def visit_dice(self, node, visited_children):
        number, _, sides = visited_children
        dice = Dice(number, sides)
        roll = dice.roll()
        return sum(roll)

    def generic_visit(self, node, visited_children):
        return visited_children or node

    def visit_expression(self, node, node_children):
        v = node_children[0]
        for (op, value) in node_children[2]:
            if op == "*":
                v *= value
            elif op == "/":
                v /= value
        return v

    def visit_statement(self, node, node_children):
        v = node_children[0]
        for (op, value) in node_children[2]:
            if op == "+":
                v += value
            elif op == "-":
                v -= value
        return v

    def visit_nested(self, node, node_children):
        return node_children[2]

      #  print(node_children)

    def visit_elem(self, node, visited_children):
        return visited_children[0]

    def visit_add_op(self, node, visited_children):
        return visited_children[0][0].text, visited_children[2]

    def visit_mul_op(self, node, visited_children):
        return visited_children[0][0].text, visited_children[2]


    def generic_visit(self, node, node_children):
        return node_children or node
       # print(node)
       #print(node_children)

if __name__ == "__main__":

    mv = DiceVisitor()


#    print(grammar.parse("2+3*1d1+2+4+5+6"))
#    print(DiceVisitor().parse("2+3*1d1+2+4+5+6"))

    print(grammar.parse("2d6+3"))

#     tree = grammar.parse("1 + 2")
#    # print(mv.visit(tree))



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
