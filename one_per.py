from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor
from dataclasses import dataclass
from random import randint
import logging
from functools import wraps


grammar = Grammar(
    """
    statement   = addition / subtraction / expression
    expression  = multiplication / division / elem
    addition    = expression '+' statement
    subtraction  = expression '-' statement
    multiplication  = elem '*' statement
    division     = elem '/' statement
    mul_expr    = '*' elem
    div_expr    = '/' elem
    elem        = nested / dice / number
    nested      = '(' ws statement ws ')'
    dice        = number? "d" number
    number      = ~"[1-9][0-9]*"
    ws          = ~"[ \t]*"
    """
)

print(grammar.parse("2+1+3*2*(1+2)"))