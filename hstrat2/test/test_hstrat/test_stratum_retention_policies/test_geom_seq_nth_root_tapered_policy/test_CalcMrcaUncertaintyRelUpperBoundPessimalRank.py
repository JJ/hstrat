import numpy as np
import pytest

from hstrat2.hstrat import geom_seq_nth_root_tapered_policy
from hstrat2.hstrat.stratum_retention_policies._detail \
    import CalcMrcaUncertaintyRelUpperBoundPessimalRankBruteForce


@pytest.mark.parametrize(
    'degree',
    [
        1,
        2,
        3,
        7,
        9,
        42,
        100,
    ],
)
@pytest.mark.parametrize(
    'interspersal',
    [
        1,
        2,
        5,
    ],
)
@pytest.mark.parametrize(
    'time_sequence',
    [
        range(10**2),
        np.random.default_rng(1).integers(
            10**3,
            size=10**2,
        )
    ],
)
def test_policy_consistency(degree, interspersal, time_sequence):
    policy = geom_seq_nth_root_tapered_policy.Policy(degree, interspersal)
    spec = policy.GetSpec()
    instance = geom_seq_nth_root_tapered_policy.CalcMrcaUncertaintyRelUpperBoundPessimalRank(
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
                policy_requirement = policy.CalcMrcaUncertaintyRelUpperBound(
                    num_strata_deposited_a,
                    num_strata_deposited_b,
                    CalcMrcaUncertaintyRelUpperBoundPessimalRankBruteForce()(
                        policy,
                        num_strata_deposited_a,
                        num_strata_deposited_b,
                    ),
                )
                for which in (
                    instance,
                    geom_seq_nth_root_tapered_policy.CalcMrcaUncertaintyRelUpperBoundPessimalRank(spec)
                ):
                    assert policy.CalcMrcaUncertaintyRelUpperBound(
                        num_strata_deposited_a,
                        num_strata_deposited_b,
                        which(
                            policy,
                            num_strata_deposited_a,
                            num_strata_deposited_b,
                        ),
                    ) == policy_requirement

@pytest.mark.parametrize(
    'degree',
    [
        1,
        2,
        3,
        7,
        9,
        42,
        100,
    ],
)
@pytest.mark.parametrize(
    'interspersal',
    [
        1,
        2,
        5,
    ],
)
def test_eq(degree, interspersal):
    policy = geom_seq_nth_root_tapered_policy.Policy(degree, interspersal)
    spec = policy.GetSpec()
    instance = geom_seq_nth_root_tapered_policy.CalcMrcaUncertaintyRelUpperBoundPessimalRank(spec)

    assert instance == instance
    assert instance == geom_seq_nth_root_tapered_policy.CalcMrcaUncertaintyRelUpperBoundPessimalRank(
        spec,
    )
    assert not instance == None
