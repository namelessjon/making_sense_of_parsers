import pytest


@pytest.mark.parametrize("test_input,expected", [
                         ("1+2", 3),
                         ("1+2*3", 7),
                         ("(1+2)*3", 9),
                         ("(   1     +  2   )", 3),
                         ("(   1     /  2   )", 0.5),
                         ("(   1     -  2   )", -1),
                         ("(   1     *  2   )", 2),
                         ("(   1     *  2   )*3*(1+2+3)", 36),
                         ("1+2*3+4+5-1", 1+2*3+4+5-1)
                         ])
def test_simple_math_works(test_input, expected):
    from parsimonious_dice.dice_visitor import DiceVisitor
    mv = DiceVisitor()
    assert mv.parse(test_input) == expected
