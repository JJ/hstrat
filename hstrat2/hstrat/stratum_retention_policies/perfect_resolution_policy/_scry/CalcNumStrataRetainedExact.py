import typing

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
        return isinstance(other, CalcNumStrataRetainedExact)

    def __call__(
        self: 'CalcNumStrataRetainedExact',
        policy: typing.Optional['Policy'],
        num_strata_deposited: int,
    ) -> int:
        """Exactly how many strata are retained after n deposted?"""

        return num_strata_deposited
