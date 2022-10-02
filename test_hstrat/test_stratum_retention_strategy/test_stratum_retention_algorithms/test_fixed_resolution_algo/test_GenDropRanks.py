import itertools as it

import numpy as np
import pytest

from hstrat._auxiliary_lib import all_same
from hstrat._testing import iter_ftor_shims, iter_no_calcrank_ftor_shims
from hstrat.hstrat import fixed_resolution_algo


@pytest.mark.parametrize(
    "fixed_resolution",
    [
        1,
        2,
        3,
        7,
        42,
        100,
    ],
)
@pytest.mark.parametrize(
    "time_sequence",
    [
        range(10**2),
        (i for i in range(10**2) for __ in range(2)),
        np.random.default_rng(1).integers(
            low=0,
            high=10**3,
            size=10**2,
        ),
    ],
)
def test_impl_consistency(fixed_resolution, time_sequence):
    policy = fixed_resolution_algo.Policy(fixed_resolution)
    spec = policy.GetSpec()
    impls = [*fixed_resolution_algo._GenDropRanks_impls]
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
    fixed_resolution_algo._enact._GenDropRanks_.impls,
)
@pytest.mark.parametrize(
    "fixed_resolution",
    [
        1,
        2,
        3,
        7,
        42,
        100,
    ],
)
@pytest.mark.parametrize(
    "time_sequence",
    [
        range(10**2),
        (i for i in range(10**2) for __ in range(2)),
        np.random.default_rng(1).integers(
            low=0,
            high=10**3,
            size=10**2,
        ),
    ],
)
def test_policy_consistency(impl, fixed_resolution, time_sequence):
    policy = fixed_resolution_algo.Policy(fixed_resolution)
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
    fixed_resolution_algo._enact._GenDropRanks_.impls,
)
@pytest.mark.parametrize(
    "fixed_resolution",
    [
        1,
        2,
        3,
        7,
        42,
        100,
    ],
)
def test_eq(impl, fixed_resolution):
    policy = fixed_resolution_algo.Policy(fixed_resolution)
    spec = policy.GetSpec()
    instance = impl(spec)

    assert instance == instance
    assert instance == impl(spec)
    assert instance is not None


@pytest.mark.parametrize(
    "fixed_resolution",
    [
        1,
        2,
        3,
        7,
        42,
        100,
    ],
)
@pytest.mark.parametrize(
    "time_sequence",
    [
        range(10**2),
        np.random.default_rng(1).integers(
            low=0,
            high=10**3,
            size=10**2,
        ),
    ],
)
def test_impl_consistency(fixed_resolution, time_sequence):
    policy = fixed_resolution_algo.Policy(fixed_resolution)
    spec = policy.GetSpec()

    for gen in time_sequence:
        assert (
            len(
                {
                    tuple(
                        sorted(
                            impl(spec)(
                                policy,
                                gen,
                                policy.IterRetainedRanks(gen),
                            )
                        )
                    )
                    for impl in it.chain(
                        fixed_resolution_algo._enact._GenDropRanks_.impls,
                        iter_ftor_shims(
                            lambda p: p.GenDropRanks,
                            fixed_resolution_algo._Policy_.impls,
                        ),
                        iter_no_calcrank_ftor_shims(
                            lambda p: p.GenDropRanks,
                            fixed_resolution_algo._Policy_.impls,
                        ),
                    )
                }
            )
            == 1
        )
