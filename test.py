import pytest
from app import square_root, add, validate_expression

# Tests for square_root function
def test_square_root_positive():
    assert square_root(4) == 2
    assert square_root(9) == 3
    assert square_root(0) == 0

def test_square_root_negative():
    with pytest.raises(ValueError):
        square_root(-1)

# Tests for add function
def test_add_integers():
    assert add(2, 3) == 5
    assert add(-2, 3) == 1
    assert add(-2, -3) == -5

def test_add_floats():
    assert add(2.5, 3.5) == 6.0
    assert add(-2.5, 3.5) == 1.0

def test_add_mixed():
    assert add(2, 3.5) == 5.5
    assert add(-2, 3.5) == 1.5

# Test cases for the mathematical expression validator
@pytest.mark.parametrize("expression, expected", [
    # Valid cases
    ("1 + 2", True),
    ("(1 + 2) * 3", True),
    ("(1 + (2 * 3))", True),
    ("1.5 + 2.75", True),
    ("(1 + 2) / 3", True),
    ("", True),  # Empty string is valid
    ("(1 + (2 - 3) * 4) / 5", True),

    # Invalid cases
    ("1 ++ 2", False),            # Consecutive operators
    ("1 +", False),               # Operator at the end
    ("+ 1", False),               # Operator at the start
    ("1 + 2)", False),            # Unbalanced parentheses
    ("(1 + 2", False),            # Unbalanced parentheses
    ("1 + (2 *)", False),         # Invalid operator position
    ("1 + 2a", False),            # Invalid character
    ("1 // 2", False),            # Invalid operator
    ("(1 + 2) 3", False),         # Missing operator
])
def test_validate_expression(expression, expected):
    """
    Test the validate_expression function for both valid and invalid cases.
    """
    result = validate_expression(expression)
    assert result == expected, f"Failed for expression: {expression}"