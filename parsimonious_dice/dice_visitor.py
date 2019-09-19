import functools
import logging

from parsimonious.nodes import NodeVisitor

from .dice import Dice
from .grammar import dice_grammar


log = logging.getLogger(__name__)


def log_visit(func):
    @functools.wraps(func)
    def wrapper(self, node, *args, **kwargs):
        log.debug("%s: %r", func.__name__, node.text)
        return func(self, node, *args, **kwargs)
    return wrapper


class DiceVisitor(NodeVisitor):
    grammar = dice_grammar

    @log_visit
    def visit_number(self, node, visited_children):
        return int(node.text)

    @log_visit
    def visit_dice(self, node, visited_children):
        number, _, sides = visited_children
        dice = Dice(number, sides)
        roll = dice.roll()
        return sum(roll)

    @log_visit
    def visit_expression(self, node, node_children):
        v = node_children[0]
        for (op, value) in node_children[2]:
            if op == "*":
                v *= value
            elif op == "/":
                v /= value
        return v

    @log_visit
    def visit_statement(self, node, node_children):
        v = node_children[0]
        for (op, value) in node_children[2]:
            if op == "+":
                v += value
            elif op == "-":
                v -= value
        return v

    @log_visit
    def visit_nested(self, node, node_children):
        return node_children[2]

    @log_visit
    def visit_elem(self, node, visited_children):
        return visited_children[0]

    @log_visit
    def visit_add_op(self, node, visited_children):
        return visited_children[0][0].text, visited_children[2]

    @log_visit
    def visit_mul_op(self, node, visited_children):
        return visited_children[0][0].text, visited_children[2]

    @log_visit
    def generic_visit(self, node, node_children):
        return node_children or node
