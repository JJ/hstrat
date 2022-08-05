import typing

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

        yield from range(0, num_strata_deposited, spec._fixed_resolution)

        last_rank = num_strata_deposited - 1
        if last_rank > 0 and last_rank % spec._fixed_resolution:
            yield last_rank
