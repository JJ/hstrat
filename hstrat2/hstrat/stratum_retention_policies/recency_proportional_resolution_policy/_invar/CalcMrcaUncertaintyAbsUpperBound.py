import typing

from ..._detail import (
    CalcWorstCaseMrcaUncertaintyAbsUpperBound,
    PolicyCouplerBase,
)
from ..PolicySpec import PolicySpec


class CalcMrcaUncertaintyAbsUpperBound:
    """Functor to provide member function implementation in Policy class."""

    def __init__(
        self: "CalcMrcaUncertaintyAbsUpperBound",
        policy_spec: typing.Optional[PolicySpec],
    ) -> None:
        pass

    def __eq__(
        self: "CalcMrcaUncertaintyAbsUpperBound",
        other: typing.Any,
    ) -> bool:
        return isinstance(other, self.__class__)

    def __call__(
        self: "CalcMrcaUncertaintyAbsUpperBound",
        policy: PolicyCouplerBase,
        first_num_strata_deposited: int,
        second_num_strata_deposited: int,
        actual_rank_of_mrca: int,
    ) -> int:
        """At most, how much uncertainty to estimate rank of MRCA? Inclusive."""

        # rectify negative-indexed actual_rank_of_mrca
        if actual_rank_of_mrca is not None and actual_rank_of_mrca < 0:
            least_last_rank = min(
                first_num_strata_deposited - 1,
                second_num_strata_deposited - 1,
            )
            actual_rank_of_mrca += least_last_rank
            assert actual_rank_of_mrca >= 0

        spec = policy.GetSpec()

        max_ranks_since_mrca = (
            max(
                first_num_strata_deposited,
                second_num_strata_deposited,
            )
            - actual_rank_of_mrca
        )
        if spec._guaranteed_mrca_recency_proportional_resolution == 0:
            return CalcWorstCaseMrcaUncertaintyAbsUpperBound()(
                policy,
                first_num_strata_deposited,
                second_num_strata_deposited,
                actual_rank_of_mrca,
            )

        res = (
            max_ranks_since_mrca
            // spec._guaranteed_mrca_recency_proportional_resolution
        )

        return min(
            res,
            CalcWorstCaseMrcaUncertaintyAbsUpperBound()(
                policy,
                first_num_strata_deposited,
                second_num_strata_deposited,
                actual_rank_of_mrca,
            ),
        )
