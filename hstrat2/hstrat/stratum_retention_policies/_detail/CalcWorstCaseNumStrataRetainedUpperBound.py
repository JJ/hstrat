import typing

from .PolicyCouplerBase import PolicyCouplerBase


class CalcWorstCaseNumStrataRetainedUpperBound:
    def __init__(
        self: "CalcWorstCaseNumStrataRetainedUpperBound",
        policy_spec: typing.Optional[typing.Any] = None,
    ) -> None:
        pass

    def __eq__(
        self: "CalcWorstCaseNumStrataRetainedUpperBound",
        other: typing.Any,
    ) -> bool:
        return isinstance(other, self.__class__)

    def __call__(
        self: "CalcWorstCaseNumStrataRetainedUpperBound",
        policy: typing.Optional[PolicyCouplerBase],
        num_strata_deposited: int,
    ) -> int:
        """At most, how many strata are retained after n deposted? Inclusive."""

        return num_strata_deposited
