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


def test_dice_works(mocker):
    mocked_random = mocker.patch('random.randint')
    mocked_random.return_value = 4  # chosen by fair dice roll. https://xkcd.com/221/

    from parsimonious_dice.dice_visitor import DiceVisitor
    mv = DiceVisitor()
    assert mv.parse("2d6+3") == 11
    assert mocked_random.called_with((1, 6), (1, 6))


def test_more_dice_works(mocker):
    mocked_random = mocker.patch('random.randint')
    mocked_random.return_value = 4  # chosen by fair dice roll. https://xkcd.com/221/

    from parsimonious_dice.dice_visitor import DiceVisitor
    mv = DiceVisitor()
    assert mv.parse("2d6+3*1d4") == 20
    assert mocked_random.called_with((1, 6), (1, 6), (1, 4))


