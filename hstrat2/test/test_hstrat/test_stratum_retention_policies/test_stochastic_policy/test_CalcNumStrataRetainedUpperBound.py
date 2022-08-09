import numpy as np
import pytest
import random

from hstrat2.hstrat import HereditaryStratigraphicColumn
from hstrat2.hstrat import stochastic_policy


@pytest.mark.parametrize(
    'replicate',
    range(5),
)
def test_policy_consistency(replicate):
    random.seed(replicate)
    policy = stochastic_policy.Policy()
    spec = policy.GetSpec()
    instance = stochastic_policy.CalcNumStrataRetainedUpperBound(spec)
    column = HereditaryStratigraphicColumn(
        stratum_retention_policy=policy,
    )
    for num_strata_deposited in range(1, 10**3):
        policy_requirement = column.GetNumStrataRetained()
        for which in (
            instance,
            stochastic_policy.CalcNumStrataRetainedUpperBound(spec),
        ):
            assert which(
                policy,
                num_strata_deposited,
            ) >= policy_requirement

@pytest.mark.parametrize(
    'replicate',
    range(5),
)
def test_eq(replicate):
    random.seed(replicate)
    policy = stochastic_policy.Policy()
    spec = policy.GetSpec()
    instance = stochastic_policy.CalcNumStrataRetainedUpperBound(spec)

    assert instance == instance
    assert instance == stochastic_policy.CalcNumStrataRetainedUpperBound(
        spec,
    )
    assert not instance == None
