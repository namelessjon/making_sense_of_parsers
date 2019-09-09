from parsimonious.grammar import Grammar


grammar = Grammar(
    """
    number = ~"[1-9][0-9]*"
    """
)

tree = grammar.parse("9")
print(tree)

tree = grammar.parse("99")
print(tree)

tree = grammar.parse("09")
print(tree)


from parsimonious.grammar import Grammar

grammar = Grammar(
    """
    number = ( '1' / '2' / '3' / '4' / '5' / '6' / '7' / '8' / '9' )
    """
)

tree = grammar.parse("9")
print(tree)