from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor
from dataclasses import dataclass
from random import randint
import logging
from functools import wraps


grammar = Grammar(
    """
    statement   = expression ( add_expr / min_expr )*
    expression  = elem ( mul_expr / div_expr  )*
    addition    = '+' expression
    min_expr    = '-' expression
    mul_expr    = '*' elem
    div_expr    = '/' elem
    elem        = nested / dice / number
    nested      = '(' ws statement ws ')'
    dice        = number? "d" number
    number      = ~"[1-9][0-9]*"
    ws          = ~"[ \t]*"
    """
)

@dataclass
class Dice:
    n: int
    sides: int

    def roll(self) -> int:
        r = [randint(1, self.sides) for i in range(self.n)]
        return r

class DiceVisitor(NodeVisitor):
    grammar = grammar
    def generic_visit(self, node, visited_children):
        return visited_children or node

    def visit_statement(self, node, visited_children):
        lhs, rhs = visited_children
        for r in rhs:
            op, expr = r[0]
            if op == '+':
                lhs += expr
            else:
                lhs -= expr
        return lhs

    def visit_expression(self, node, visited_children):
        lhs, rhs = visited_children
        for r in rhs:
            op, expr = r[0]
            if op == '*':
                lhs *= expr
            else:
                lhs /= expr
        return lhs

    def visit_number(self, node, visited_children):
        return int(node.text)

    def visit_elem(self, node, visited_children):
        return visited_children[0]
    
    def visit_add_expr(self, node, visited_children):
        op, expr = visited_children
        return op.text, expr
    def visit_min_expr(self, node, visited_children):
        op, expr = visited_children
        return op.text, expr
    def visit_mul_expr(self, node, visited_children):
        op, expr = visited_children
        return op.text, expr
    def visit_div_expr(self, node, visited_children):
        op, expr = visited_children
        return op.text, expr

    def visit_dice(self, node, visited_children):
        number, _, sides = visited_children
        dice = Dice(number[0], sides)
        roll = dice.roll()
        return sum(roll)

print(grammar.parse("2+3*1d1+2+4+5+6"))
print(DiceVisitor().parse("2+3*d1+2+4+5+6"))