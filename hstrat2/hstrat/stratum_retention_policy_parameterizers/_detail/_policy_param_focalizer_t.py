import typing

from ...stratum_retention_policies._detail import PolicyCouplerBase

policy_param_focalizer_t = typing.Callable[
    [typing.Type],
    typing.Callable[[int], PolicyCouplerBase],
]
