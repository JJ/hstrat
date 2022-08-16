import typing

from ..PolicySpec import PolicySpec

class CalcMrcaUncertaintyAbsUpperBound:
    """Functor to provide member function implementation in Policy class."""

    def __init__(
        self: 'CalcMrcaUncertaintyAbsUpperBound',
        policy_spec: typing.Optional[PolicySpec],
    ) -> None:
        pass

    def __eq__(
        self: 'CalcMrcaUncertaintyAbsUpperBound',
        other: typing.Any,
    ) -> bool:
        return isinstance(other, self.__class__)

    def __call__(
        self: 'CalcMrcaUncertaintyAbsUpperBound',
        policy: 'Policy',
        first_num_strata_deposited: int,
        second_num_strata_deposited: int,
        actual_rank_of_mrca: typing.Optional[int],
    ) -> int:
        """At most, how much absolute uncertainty to estimate rank of MRCA?
        Inclusive."""

        spec = policy.GetSpec()

        least_last_rank = max(
            min(
                first_num_strata_deposited - 1,
                second_num_strata_deposited - 1,
            ),
            0,
        )

        return min(
            spec._fixed_resolution - 1,
            least_last_rank,
        )
