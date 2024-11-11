from unittest.mock import patch

import pytest

from app.apis.api_router.srv import main as mainmod_a


@pytest.fixture(scope="module")
def mock_randint():
    """Mock random.randint function."""

    with patch("random.randint", return_value=42, auto=True) as m:
        yield m


@pytest.mark.parametrize(
    ("seed", "output"),
    [(1, 42), (100, 42), (589, 42), (444, 42)],
)
def test_func_main_a(mock_randint, seed, output):
    # Act.
    result = mainmod_a.main_func(seed)

    # Assert.
    assert isinstance(result, dict) is True
    assert result["seed"] == seed
    assert result["random_first"] == output
    assert result["random_second"] == output

    mock_randint.assert_called_with(0, seed)
