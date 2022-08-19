import typing

from ._policy_param_focalizer_t import _policy_param_focalizer_t


class NumStrataRetainedUpperBoundPolicyEvaluator:

    _at_num_strata_deposited: int
    _policy_param_focalizer: _policy_param_focalizer_t

    def __init__(
        self: "NumStrataRetainedUpperBoundPolicyEvaluator",
        at_num_strata_deposited: int,
        policy_param_focalizer: _policy_param_focalizer_t = (
            lambda policy_t: lambda i: policy_t(i)
        ),
    ) -> None:
        """Initialize functor to evaluate upper bound on num strata retained.

        Parameters
        ----------
        at_num_strata_deposited : int
            At what generation should we evaluate policy?
        policy_param_focalizer : callable
            Callable to create shim that constructs policy instance from
            parameter value. Default passes parameter value as sole argument to
            policy constructor.
        """
        self._at_num_strata_deposited = at_num_strata_deposited
        self._policy_param_focalizer = policy_param_focalizer

    def __call__(
        self: "NumStrataRetainedUpperBoundPolicyEvaluator",
        policy_t: typing.Type,
        parameter_value: int,
    ) -> int:
        """Evaluate upper bound on num strata retained for policy with a
        particular parameter value."""
        policy_factory = self._policy_param_focalizer(policy_t)
        policy = policy_factory(parameter_value)
        return policy.CalcNumStrataRetainedUpperBound(
            self._at_num_strata_deposited,
        )

    def __repr__(self: "NumStrataRetainedUpperBoundPolicyEvaluator") -> str:
        return f"""{
            NumStrataRetainedUpperBoundPolicyEvaluator.__qualname__
        }(at_num_strata_deposited={
            self._at_num_strata_deposited
        !r}, policy_param_focalizer={
            self._policy_param_focalizer
        !r})"""

    def __str__(self: "NumStrataRetainedUpperBoundPolicyEvaluator") -> str:
        title = "Upper Bound Num Strata Retained Evaluator"
        return f"""{
            title
        } (at num strata deposited: {
            self._at_num_strata_deposited
        }, focalizer: {
            self._policy_param_focalizer
        })"""
