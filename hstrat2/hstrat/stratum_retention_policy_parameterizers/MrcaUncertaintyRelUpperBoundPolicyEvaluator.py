import numpy as np
import opytional as opyt
import typing


_policy_param_focalizer_t = typing.Callable[
    [typing.Type],
    typing.Callable[[int], 'Policy'],
]

class MrcaUncertaintyRelUpperBoundPolicyEvaluator:

    _threshold_uncertainty: float
    _at_num_strata_deposited: int
    _at_rank: typing.Optional[int]
    _policy_param_focalizer: _policy_param_focalizer_t

    def __init__(
        self: 'MrcaUncertaintyRelUpperBoundPolicyEvaluator',
        at_num_strata_deposited: int,
        at_rank: typing.Optional[int]=None,
        policy_param_focalizer: _policy_param_focalizer_t\
            =lambda policy_t: lambda i: policy_t(i),
    ) -> None:
        """Initialize functor to evaluate upper bound on relative MRCA
        uncertainty.

        Parameters
        ----------
        at_num_strata_deposited : int
            At what generation should we evaluate policy?
        at_rank : int, optional
            At what column position should we evaluate policy? If None, use
            pessimal position.
        policy_param_focalizer : callable
            Callable to create shim that constructs policy instance from
            parameter value. Default passes parameter value as sole argument to
            policy constructor.
        """
        self._at_num_strata_deposited = at_num_strata_deposited
        self._at_rank = at_rank
        self._policy_param_focalizer = policy_param_focalizer

    def __call__(
        self: 'MrcaUncertaintyRelUpperBoundPolicyEvaluator',
        policy_t: typing.Type,
        parameter_value: int,
    ) -> float:
        """Evaluate upper bound on relative MRCA uncertainty for policy with a particular parameter value."""
        policy_factory = self._policy_param_focalizer(policy_t)
        policy = policy_factory(parameter_value)
        at_rank = opyt.or_value(
            self._at_rank,
            policy.CalcMrcaUncertaintyRelUpperBoundPessimalRank(
                self._at_num_strata_deposited,
                self._at_num_strata_deposited,
            ),
        )
        return policy.CalcMrcaUncertaintyRelUpperBound(
            self._at_num_strata_deposited,
            self._at_num_strata_deposited,
            at_rank,
        )
