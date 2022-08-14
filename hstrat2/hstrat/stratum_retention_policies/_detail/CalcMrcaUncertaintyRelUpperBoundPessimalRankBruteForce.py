import numpy as np
import typing


class CalcMrcaUncertaintyRelUpperBoundPessimalRankBruteForce:

    def __init__(
        self: 'CalcMrcaUncertaintyRelUpperBoundPessimalRankBruteForce',
        policy_spec: typing.Optional[typing.Any]=None,
    ) -> None:
        pass

    def __eq__(
        self: 'CalcMrcaUncertaintyRelUpperBoundPessimalRankBruteForce',
        other: typing.Any,
    ) -> bool:
        return isinstance(other, self.__class__)

    def __call__(
        self: 'CalcMrcaUncertaintyRelUpperBoundPessimalRankBruteForce',
        policy: typing.Optional['Policy'],
        first_num_strata_deposited: int,
        second_num_strata_deposited: int,
    ) -> int:
        """Calculate pessimal rank for upper bound on absolute MRCA
        uncertainty by brute force."""

        least_num_strata_deposited = min(
            first_num_strata_deposited,
            second_num_strata_deposited,
        )

        if least_num_strata_deposited == 0:
            return 0

        pessimal_rank = max(
            (
                (
                    r,
                    policy.CalcMrcaUncertaintyRelUpperBound(
                        first_num_strata_deposited,
                        second_num_strata_deposited,
                        r
                    ),
                )
                for r in range(least_num_strata_deposited)
            ),
            key=lambda tup: tup[1],
        )[0]

        return pessimal_rank
