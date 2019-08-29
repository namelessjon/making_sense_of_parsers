from parsimonious.grammar import Grammar


grammar = Grammar(
    """
    expr   = elem (('+' / '-') elem)*
    elem   = dice / number
    dice   = number "d" number
    number = ~"[1-9][0-9]*"
    """
)

tree = grammar.parse("9d6")
print(tree)

tree = grammar.parse("9")
print(tree)

tree = grammar.parse("9+9d6")
print(tree)

tree = grammar.parse("9+9d6+5")
print(tree)
