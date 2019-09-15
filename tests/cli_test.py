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
def test_simple_math_works(test_input, expected, capsys):
    from parsimonious_dice.cli import cli
    cli([test_input])

    stdout, stderr = capsys.readouterr()
    assert "Rolling" in stdout
    assert test_input in stdout
    assert str(expected) in stdout