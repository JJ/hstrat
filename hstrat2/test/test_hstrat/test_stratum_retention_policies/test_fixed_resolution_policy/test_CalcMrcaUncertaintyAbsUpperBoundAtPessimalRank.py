import numpy as np
import pytest

from hstrat2.hstrat import fixed_resolution_policy
from hstrat2.hstrat.stratum_retention_policies._detail import (
    CalcMrcaUncertaintyAbsUpperBoundPessimalRankBruteForce,
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
        np.random.default_rng(1).integers(
            10**2,
            size=10,
        ),
        np.random.default_rng(1).integers(
            10**3,
            size=10,
        ),
    ],
)
def test_policy_consistency(fixed_resolution, time_sequence):
    policy = fixed_resolution_policy.Policy(fixed_resolution)
    spec = policy.GetSpec()
    instance = (
        fixed_resolution_policy.CalcMrcaUncertaintyAbsUpperBoundAtPessimalRank(
            spec,
        )
    )
    for num_strata_deposited_a in time_sequence:
        for num_strata_deposited_b in (
            num_strata_deposited_a // 3,
            num_strata_deposited_a // 2,
            num_strata_deposited_a,
            num_strata_deposited_a + 1,
            num_strata_deposited_a + 10,
            num_strata_deposited_a + 100,
        ):
            if 0 in (num_strata_deposited_a, num_strata_deposited_b):
                continue
            for actual_mrca_rank in np.random.default_rng(1).integers(
                min(num_strata_deposited_a, num_strata_deposited_b),
                size=3,
            ):
                policy_requirement = policy.CalcMrcaUncertaintyAbsUpperBound(
                    num_strata_deposited_a,
                    num_strata_deposited_b,
                    CalcMrcaUncertaintyAbsUpperBoundPessimalRankBruteForce()(
                        policy,
                        num_strata_deposited_a,
                        num_strata_deposited_b,
                    ),
                )
                for which in (
                    instance,
                    fixed_resolution_policy.CalcMrcaUncertaintyAbsUpperBoundAtPessimalRank(
                        spec
                    ),
                ):
                    assert (
                        which(
                            policy,
                            num_strata_deposited_a,
                            num_strata_deposited_b,
                        )
                        == policy_requirement
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
def test_eq(fixed_resolution):
    policy = fixed_resolution_policy.Policy(fixed_resolution)
    spec = policy.GetSpec()
    instance = (
        fixed_resolution_policy.CalcMrcaUncertaintyAbsUpperBoundAtPessimalRank(
            spec
        )
    )

    assert instance == instance
    assert (
        instance
        == fixed_resolution_policy.CalcMrcaUncertaintyAbsUpperBoundAtPessimalRank(
            spec,
        )
    )
    assert instance is not None
