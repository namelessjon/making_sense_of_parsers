from parsimonious.grammar import Grammar


grammar = Grammar(
    """
    eqn    = expr ws (mul_op ws expr)*
    expr   = elem ws (add_op ws elem)*
    elem   = dice / number
    dice   = number "d" number
    add_op = '+' / '-'
    mul_op = '*' / '/'
    number = ~"[1-9][0-9]*"
    ws     = ~"\s*"
    """
)

tree = grammar.parse("9d6")
print(tree)

tree = grammar.parse("9")
print(tree)

tree = grammar.parse("9+9d6")
print(tree)

tree = grammar.parse("9+9d6+ 5")
print(tree)

tree = grammar.parse("9+9d6+ 5*6")
print(tree)
