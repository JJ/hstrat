import typing

from ..PolicySpec import PolicySpec

class CalcNumStrataRetainedUpperBound:
    """Functor to provide member function implementation in Policy class."""

    def __init__(
        self: 'CalcNumStrataRetainedUpperBound',
        policy_spec: typing.Optional[PolicySpec]=None,
    ) -> None:
        pass

    def __eq__(
        self: 'CalcNumStrataRetainedUpperBound',
        other: typing.Any,
    ) -> bool:
        return isinstance(other, CalcNumStrataRetainedUpperBound)

    def __call__(
        self: 'CalcNumStrataRetainedUpperBound',
        policy: 'Policy',
        num_strata_deposited: typing.Optional[int],
    ) -> int:
        """At most, how many strata are retained after n deposted? Inclusive."""

        spec = policy.GetSpec()

        return spec._guaranteed_depth_proportional_resolution * 2 + 1
