import typing

from .._impl import calc_provided_uncertainty
from ..PolicySpec import PolicySpec

class IterRetainedRanks:
    """Functor to provide member function implementation in Policy class."""

    def __init__(
        self: 'IterRetainedRanks',
        policy_spec: typing.Optional[PolicySpec],
    ) -> None:
        pass

    def __eq__(
        self: 'IterRetainedRanks',
        other: typing.Any,
    ) -> bool:
        return isinstance(other, IterRetainedRanks)

    def __call__(
        self: 'IterRetainedRanks',
        policy: typing.Optional['Policy'],
        num_strata_deposited: int,
    ) -> typing.Iterator[int]:
        """Iterate over retained strata ranks at `num_strata_deposited` in
        ascending order."""

        spec = policy.GetSpec()
        uncertainty = calc_provided_uncertainty(
            spec._guaranteed_depth_proportional_resolution,
            num_strata_deposited,
        )

        yield from range(0, num_strata_deposited, uncertainty)

        last_rank = num_strata_deposited - 1
        if last_rank > 0 and last_rank % uncertainty:
            yield last_rank
