import pytest

from hstrat2.hstrat import pseudostochastic_policy


@pytest.mark.parametrize(
    'random_seed',
    [
        1,
        2,
        3,
        7,
        42,
        100,
    ],
)
def test_eq(random_seed):
    spec = pseudostochastic_policy.PolicySpec(random_seed)
    assert spec == spec
    assert spec == pseudostochastic_policy.PolicySpec(random_seed)
    assert not spec == pseudostochastic_policy.PolicySpec(random_seed + 1)

@pytest.mark.parametrize(
    'random_seed',
    [
        1,
        2,
        3,
        7,
        42,
        100,
    ],
)
def test_init(random_seed):
    spec = pseudostochastic_policy.PolicySpec(random_seed)
    assert spec._random_seed == random_seed
