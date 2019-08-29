from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor


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

class MAthVisitor(NodeVisitor):
    def visit_number(self, node, node_children):
        return int(node.text)

    def generic_visit(self, node, node_children):
        print(node)
        print(node_children)

mv = MAthVisitor()

tree = grammar.parse("9d6")
print(tree)

tree = grammar.parse("9")
mv.visit(tree)
print(tree)

tree = grammar.parse("9+9d6")
print(tree)

tree = grammar.parse("9+9d6+ 5")
print(tree)

tree = grammar.parse("9+9d6+ 5*6")
print(tree)
