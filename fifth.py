from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor
from dataclasses import dataclass
import random
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


@dataclass
class Dice:
    num: int
    sides: int

    def roll(self) -> int:
        rolls = [random.randint(1, self.sides) for i in range(self.num)]
        return rolls


logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)


class MathVisitor(NodeVisitor):
    def visit_number(self, node, node_children):
        logger.debug("number: %s", node.text)
        return int(node.text)

    def visit_ws(self, *args):
        logger.debug("ws")
        return None

    def visit_dice(self, node, node_children):
        logger.debug("dice: %s", node.text)
        number, _, sides = node_children
        dice = Dice(number, sides)
        roll = dice.roll()
        return sum(roll)

    def visit_expression(self, node, node_children):
        logger.debug("expression: %s", node.text)
        v = node_children[0]
        for (op, value) in node_children[2]:
            if op == "*":
                v *= value
            elif op == "/":
                v /= value
        return v

    def visit_statement(self, node, node_children):
        logger.debug("statement: %s", node.text)
        v = node_children[0]
        for (op, value) in node_children[2]:
            if op == "+":
                v += value
            elif op == "-":
                v -= value
        return v

    def visit_nested(self, node, node_children):
        logger.debug("nested: %s", node.text)
        return node_children[2]

      #  print(node_children)

    def visit_elem(self, node, visited_children):
        logger.debug("elem: %s", node.text)
        return visited_children[0]

    def visit_add_op(self, node, visited_children):
        logger.debug("add_op: %s", node.text)
        return visited_children[0][0].text, visited_children[2]

    def visit_mul_op(self, node, visited_children):
        logger.debug("mul_op: %s", node.text)
        return visited_children[0][0].text, visited_children[2]


    def generic_visit(self, node, node_children):
        return node_children or node
       # print(node)
       #print(node_children)

if __name__ == "__main__":

    mv = MathVisitor()


    tree = grammar.parse("1 + 2")
    print(mv.visit(tree))



    tree = grammar.parse("9d6")
    print(mv.visit(tree))
    # print(tree)

    tree = grammar.parse("(      (     ( 9 + 5 + (3+1)   ) )      )*2")
    print(mv.visit(tree))


    tree = grammar.parse("1+2*3*4+5")
    #print(tree)
    print(mv.visit(tree))
    #print(tree)

    tree = grammar.parse("3/4/5")
    #print(tree)
    print(mv.visit(tree))

    # tree = grammar.parse("9+9d6")
    # print(tree)

    # tree = grammar.parse("9+9d6+ 5")
    # print(tree)

    tree = grammar.parse("9+2d6+ 5*6")
    print(mv.visit(tree))
    # print(tree)
