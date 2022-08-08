import typing

from .._impl import get_retained_ranks
from ..PolicySpec import PolicySpec

class CalcNumStrataRetainedExact:
    """Functor to provide member function implementation in Policy class."""

    def __init__(
        self: 'CalcNumStrataRetainedExact',
        policy_spec: typing.Optional[PolicySpec],
    ) -> None:
        pass

    def __eq__(
        self: 'CalcNumStrataRetainedExact',
        other: typing.Any,
    ) -> bool:
        return isinstance(other, self.__class__)

    def __call__(
        self: 'CalcNumStrataRetainedExact',
        policy: 'Policy',
        num_strata_deposited: int,
    ) -> int:
        """Exactly how many strata are retained after n deposted?"""

        spec = policy.GetSpec()
        return len(get_retained_ranks(
            spec._degree,
            spec._interspersal,
            num_strata_deposited,
        ))
