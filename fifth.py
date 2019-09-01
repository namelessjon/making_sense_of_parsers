from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor
from dataclasses import dataclass
import random


grammar = Grammar(
    """
    eqn    = expr ws add_op*
    expr   = elem ws mul_op*
    elem   = nested / dice / number
    nested = '(' ws eqn ws ')'
    dice   = number "d" number
    add_op = ('+' / '-') ws expr ws
    mul_op = ('*' / '/') ws elem ws
    number = ~"[1-9][0-9]*"
    ws     = ~"\s*"
    """
)

@dataclass
class Dice:
    num: int
    sides: int

    def roll(self) -> int:
        rolls = [random.randint(1, self.sides) for i in range(self.num)]
        return rolls


class MathVisitor(NodeVisitor):
    def visit_number(self, node, node_children):
        return int(node.text)

    def visit_ws(self, *args):
        return None

    def visit_dice(self, node, node_children):
        number, _, sides = node_children
        dice = Dice(number, sides)
        roll = dice.roll()
        return sum(roll)

    def visit_expr(self, node, node_children):
        v = node_children[0]
        for (op, value) in node_children[2]:
            if op == "*":
                v *= value
            elif op == "/":
                v /= value
        return v

    def visit_eqn(self, node, node_children):
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

mv = MathVisitor()

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
