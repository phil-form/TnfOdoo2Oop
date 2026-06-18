from calculs import addition
from calculs import division

def test_addition():
    assert addition(2, 3) == 5

def test_division_by_zero():
    try:
        division(50, 0)
    except Exception as e:
        assert isinstance(e, ValueError)
        assert "division by zero" in str(e)