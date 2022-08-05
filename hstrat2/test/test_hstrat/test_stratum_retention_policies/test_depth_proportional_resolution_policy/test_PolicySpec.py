import pytest

from hstrat2.hstrat import depth_proportional_resolution_policy


@pytest.mark.parametrize(
    'depth_proportional_resolution',
    [
        1,
        2,
        3,
        7,
        42,
        97,
        100,
    ],
)
def test_eq(depth_proportional_resolution):
    spec = depth_proportional_resolution_policy.PolicySpec(depth_proportional_resolution)
    assert spec == spec
    assert spec == depth_proportional_resolution_policy.PolicySpec(depth_proportional_resolution)
    assert not spec == depth_proportional_resolution_policy.PolicySpec(depth_proportional_resolution + 1)

@pytest.mark.parametrize(
    'depth_proportional_resolution',
    [
        1,
        2,
        3,
        7,
        42,
        97,
        100,
    ],
)
def test_init(depth_proportional_resolution):
    spec = depth_proportional_resolution_policy.PolicySpec(depth_proportional_resolution)
    assert spec._guaranteed_depth_proportional_resolution == depth_proportional_resolution
