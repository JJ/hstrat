import itertools as it

import numpy as np
import pytest

from hstrat._auxiliary_lib import all_same
from hstrat.hstrat import recency_proportional_resolution_algo


@pytest.mark.parametrize(
    "recency_proportional_resolution",
    [
        0,
        1,
        2,
        3,
        7,
        42,
        97,
        100,
    ],
)
@pytest.mark.parametrize(
    "time_sequence",
    [
        range(10**3),
        (i for i in range(10**2) for __ in range(2)),
        np.random.default_rng(1).integers(
            low=0,
            high=2**32,
            size=10,
        ),
        (2**32,),
    ],
)
def test_impl_consistency(recency_proportional_resolution, time_sequence):
    policy = recency_proportional_resolution_algo.Policy(
        recency_proportional_resolution
    )
    spec = policy.GetSpec()
    impls = [*recency_proportional_resolution_algo._GenDropRanks_impls]
    instances = [impl(spec) for impl in impls]
    for num_strata_deposited in time_sequence:
        assert all_same(
            it.chain(
                (
                    sorted(
                        impl(spec)(
                            policy,
                            num_strata_deposited,
                            policy.IterRetainedRanks(num_strata_deposited),
                        )
                    )
                    for impl in impls
                ),
                (
                    sorted(
                        instance(
                            policy,
                            num_strata_deposited,
                            policy.IterRetainedRanks(num_strata_deposited),
                        )
                    )
                    for instance in instances
                ),
            )
        )


@pytest.mark.parametrize(
    "impl",
    recency_proportional_resolution_algo._enact._GenDropRanks_.impls,
)
@pytest.mark.parametrize(
    "recency_proportional_resolution",
    [
        0,
        1,
        2,
        3,
        7,
        42,
        97,
        100,
    ],
)
@pytest.mark.parametrize(
    "time_sequence",
    [
        range(10**3),
        (i for i in range(10**2) for __ in range(2)),
        np.random.default_rng(1).integers(
            low=0,
            high=2**32,
            size=10,
        ),
        (2**32,),
    ],
)
def test_policy_consistency(
    impl, recency_proportional_resolution, time_sequence
):
    policy = recency_proportional_resolution_algo.Policy(
        recency_proportional_resolution
    )
    spec = policy.GetSpec()
    instance = impl(spec)
    for num_strata_deposited in time_sequence:
        policy_requirement = {
            *policy.IterRetainedRanks(
                num_strata_deposited,
            )
        } - {
            *policy.IterRetainedRanks(
                num_strata_deposited + 1,
            )
        }
        for which in (
            instance,
            impl(spec),
        ):
            assert sorted(
                which(
                    policy,
                    num_strata_deposited,
                    policy.IterRetainedRanks(num_strata_deposited),
                )
            ) == sorted(policy_requirement)


@pytest.mark.parametrize(
    "impl",
    recency_proportional_resolution_algo._enact._GenDropRanks_.impls,
)
@pytest.mark.parametrize(
    "recency_proportional_resolution",
    [
        0,
        1,
        2,
        3,
        7,
        42,
        97,
        100,
    ],
)
def test_eq(impl, recency_proportional_resolution):
    policy = recency_proportional_resolution_algo.Policy(
        recency_proportional_resolution
    )
    spec = policy.GetSpec()
    instance = impl(spec)

    assert instance == instance
    assert instance == impl(spec)
    assert instance is not None
