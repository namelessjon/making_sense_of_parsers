import parsimonious.grammar

dice_grammar = parsimonious.grammar.Grammar(
    """
    statement   = expression ws add_op*
    expression  = elem ws mul_op*
    elem        = nested / dice / number
    nested      = '(' ws statement ws ')'
    dice        = number "d" number
    add_op      = ('+' / '-') ws expression ws
    mul_op      = ('*' / '/') ws elem ws
    number      = ~"[1-9][0-9]*"
    ws          = ~"\s*"
    """
)