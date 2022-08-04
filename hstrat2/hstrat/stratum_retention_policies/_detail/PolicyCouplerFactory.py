import opytional as opyt
import typing

from . import CalcWorstCaseMrcaUncertaintyUpperBound
from . import CalcWorstCaseNumStrataRetainedUpperBound


class _CurryPolicy:
    """Helper class to enable the policy coupler to insert itself as the
    first argument to calls to implementation functors."""

    _policy: 'PolicyCoupler'
    _ftor: typing.Callable

    def __init__(
        self: 'CurryPolicy',
        policy: 'PolicyCoupler',
        ftor: typing.Callable,
    ) -> None:
        self._policy = policy
        self._ftor = ftor

    def __eq__(self: '_CurryPolicy', other: typing.Any) -> bool:
        if isinstance(other, _CurryPolicy):
            # don't compare policy to prevent infinite recursion
            return self._ftor == other._ftor
        else:
            return False

    def __call__(self: '_CurryPolicy', *args, **kwargs) -> typing.Any:
        return self._ftor(self._policy, *args, **kwargs)

class _PolicyCouplerBase:
    """Dummy class to faciliate recognition of instantiations of the
    PolicyCoupler class across different calls to the PolicyCoupler factory."""

    pass

_ftor_type = typing.Callable[
    [typing.Any], # policy spec
    typing.Callable, # functor
]

def PolicyCouplerFactory(
    *,
    policy_spec_t: typing.Any,
    # enactment
    gen_drop_ranks_ftor_t: _ftor_type,
    # invariants
    calc_mrca_uncertainty_upper_bound_ftor_t: _ftor_type \
        =CalcWorstCaseMrcaUncertaintyUpperBound,
    calc_num_strata_retained_upper_bound_ftor_t: _ftor_type \
        =CalcWorstCaseNumStrataRetainedUpperBound,
    # scrying
    calc_mrca_uncertainty_exact_ftor_t: typing.Optional[_ftor_type]=None,
    calc_num_strata_retained_exact_ftor_t: typing.Optional[_ftor_type]=None,
    calc_rank_at_column_index_ftor_t: typing.Optional[_ftor_type]=None,
    iter_retained_ranks_ftor_t: typing.Optional[_ftor_type]=None,
):

    class PolicyCoupler(
        _PolicyCouplerBase,
    ):

        _policy_spec: policy_spec_t

        # invariants
        CalcMrcaUncertaintyUpperBound: typing.Callable
        CalcNumStrataRetainedUpperBound: typing.Callable

        # scrying
        CalcMrcaUncertaintyExact: typing.Optional[typing.Callable]
        CalcNumStrataRetainedExact: typing.Optional[typing.Callable]
        CalcRankAtColumnIndex: typing.Optional[typing.Callable]
        IterRetainedRanks: typing.Optional[typing.Callable]

        # enactment
        GenDropRanks: typing.Callable

        def __init__(
            self: 'PolicyCoupler',
            *args,
            policy_spec=None,
            **kwargs,
        ):
            self._policy_spec = opyt.or_else(
                policy_spec,
                lambda: policy_spec_t(*args, **kwargs),
            )
            if policy_spec is not None:
                assert len(args) == len(kwargs) == 0

            # enactment
            self.GenDropRanks = gen_drop_ranks_ftor_t(self._policy_spec)

            # invariants
            self.CalcMrcaUncertaintyUpperBound = _CurryPolicy(
                self,
                calc_mrca_uncertainty_upper_bound_ftor_t(self._policy_spec),
            )
            self.CalcNumStrataRetainedUpperBound = _CurryPolicy(
                self,
                calc_num_strata_retained_upper_bound_ftor_t(self._policy_spec),
            )

            # scrying
            self.CalcMrcaUncertaintyExact = opyt.apply_if(
                calc_mrca_uncertainty_exact_ftor_t,
                lambda x: _CurryPolicy(self, x(self._policy_spec)),
            )
            self.CalcNumStrataRetainedExact = opyt.apply_if(
                calc_num_strata_retained_exact_ftor_t,
                lambda x: _CurryPolicy(self, x(self._policy_spec)),
            )
            self.CalcRankAtColumnIndex = opyt.apply_if(
                calc_rank_at_column_index_ftor_t,
                lambda x: _CurryPolicy(self, x(self._policy_spec)),
            )
            self.IterRetainedRanks = opyt.apply_if(
                iter_retained_ranks_ftor_t,
                lambda x: _CurryPolicy(self, x(self._policy_spec)),
            )

        def __eq__(
            self: 'PolicyCoupler',
            other: typing.Any,
        ) -> bool:
            if issubclass(
                other.__class__,
                _PolicyCouplerBase,
            ):
                return (
                    self._policy_spec,
                    self.GenDropRanks,
                    self.CalcMrcaUncertaintyUpperBound,
                    self.CalcNumStrataRetainedUpperBound,
                    self.CalcMrcaUncertaintyExact,
                    self.CalcNumStrataRetainedExact,
                    self.CalcRankAtColumnIndex,
                    self.IterRetainedRanks,
                ) == (
                    other._policy_spec,
                    other.GenDropRanks,
                    other.CalcMrcaUncertaintyUpperBound,
                    other.CalcNumStrataRetainedUpperBound,
                    other.CalcMrcaUncertaintyExact,
                    other.CalcNumStrataRetainedExact,
                    other.CalcRankAtColumnIndex,
                    other.IterRetainedRanks,
                )
            else:
                return False

        def GetSpec(self: 'PolicyCoupler') -> policy_spec_t:
            return self._policy_spec

        def WithoutCalcRankAtColumnIndex(
            self: 'PolicyCoupler',
        ) -> 'PolicyCoupler':
            type_ = PolicyCouplerFactory(
                policy_spec_t=policy_spec_t,
                # enactment
                gen_drop_ranks_ftor_t=gen_drop_ranks_ftor_t,
                # invariants
                calc_mrca_uncertainty_upper_bound_ftor_t\
                    =calc_mrca_uncertainty_upper_bound_ftor_t,
                calc_num_strata_retained_upper_bound_ftor_t\
                    =calc_num_strata_retained_upper_bound_ftor_t,
                # scrying
                calc_mrca_uncertainty_exact_ftor_t\
                    =calc_mrca_uncertainty_exact_ftor_t,
                calc_num_strata_retained_exact_ftor_t\
                    =calc_num_strata_retained_exact_ftor_t,
                calc_rank_at_column_index_ftor_t=None,
                iter_retained_ranks_ftor_t\
                    =iter_retained_ranks_ftor_t,
            )
            return type_(
                policy_spec=self._policy_spec,
            )


    return PolicyCoupler
