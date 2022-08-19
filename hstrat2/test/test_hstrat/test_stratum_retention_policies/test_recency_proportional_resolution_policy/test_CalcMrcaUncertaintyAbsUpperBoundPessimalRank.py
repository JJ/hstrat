import numpy as np
import pytest

from hstrat2.hstrat import recency_proportional_resolution_policy
from hstrat2.hstrat.stratum_retention_policies._detail import (
    CalcMrcaUncertaintyAbsUpperBoundPessimalRankBruteForce,
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
        np.random.default_rng(1).integers(
            10**2,
            size=10,
        ),
        np.random.default_rng(1).integers(
            10**3,
            size=10**2,
        ),
    ],
)
def test_policy_consistency(recency_proportional_resolution, time_sequence):
    policy = recency_proportional_resolution_policy.Policy(
        recency_proportional_resolution
    )
    spec = policy.GetSpec()
    instance = recency_proportional_resolution_policy.CalcMrcaUncertaintyAbsUpperBoundPessimalRank(
        spec,
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
                    recency_proportional_resolution_policy.CalcMrcaUncertaintyAbsUpperBoundPessimalRank(
                        spec
                    ),
                ):
                    assert (
                        policy.CalcMrcaUncertaintyAbsUpperBound(
                            num_strata_deposited_a,
                            num_strata_deposited_b,
                            which(
                                policy,
                                num_strata_deposited_a,
                                num_strata_deposited_b,
                            ),
                        )
                        == policy_requirement
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
def test_eq(recency_proportional_resolution):
    policy = recency_proportional_resolution_policy.Policy(
        recency_proportional_resolution
    )
    spec = policy.GetSpec()
    instance = recency_proportional_resolution_policy.CalcMrcaUncertaintyAbsUpperBoundPessimalRank(
        spec
    )

    assert instance == instance
    assert (
        instance
        == recency_proportional_resolution_policy.CalcMrcaUncertaintyAbsUpperBoundPessimalRank(
            spec,
        )
    )
    assert instance is not None
