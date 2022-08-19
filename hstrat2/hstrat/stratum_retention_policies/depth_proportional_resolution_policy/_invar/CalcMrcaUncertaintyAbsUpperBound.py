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
        """At most, how much absolute uncertainty to estimate rank of MRCA?
        Inclusive."""

        spec = policy.GetSpec()

        res = (
            max(
                first_num_strata_deposited,
                second_num_strata_deposited,
            )
            // spec._guaranteed_depth_proportional_resolution
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
