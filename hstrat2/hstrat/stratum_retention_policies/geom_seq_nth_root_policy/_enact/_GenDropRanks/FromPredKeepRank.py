import typing

from ...._detail import GenDropRanksFromPredKeepRank

from ...PolicySpec import PolicySpec
from ..._impl import get_retained_ranks

class _PredKeepRank:
    """Functor to implement the approximate space-filling MRCA-recency-
    proportional resolution stratum retention policy, for use with
    HereditaryStratigraphicColumn.

    This functor enacts the approximate space-filling MRCA-recency-
    proportional resolution stratum retention policy by specifying the set of
    strata ranks that should be purged from a hereditary stratigraphic column
    when the nth stratum is deposited.
    """

    def __init__(
        self: '_PredKeepRank',
        policy_spec: typing.Optional[PolicySpec],
    ) -> None:
        pass

    def __eq__(
        self: '_PredKeepRank',
        other: typing.Any,
    ) -> bool:
        return isinstance(other, self.__class__)

    def __call__(
        self: '_PredKeepRank',
        policy: 'Policy',
        num_stratum_depositions_completed: int,
        stratum_rank: int,
    ) -> bool:
        """Decide if a stratum within the stratagraphic column should be
        retained or purged.

        Every time a new stratum is deposited, this method is called on each
        stratum present in a HereditaryStratigraphicColumn to determine whether
        it should be retained. Strata that return False are immediately purged
        from the column, meaning that for a stratum to persist it must earn a
        True result from this method each and every time a new stratum is
        deposited.

        Parameters
        ----------
        policy: Policy
            Policy this functor enacts.
        stratum_rank : int
            The number of strata that were deposited before the stratum under
            consideration for retention.
        num_stratum_depositions_completed : int
            The number of strata that have already been deposited, not
            including the latest stratum being deposited which prompted the
            current purge operation.

        Returns
        -------
        bool
            True if the stratum should be retained, False otherwise.

        See Also
        --------
        depth_proportional_resolution_tapered_policy:
            For details on the rationale, implementation, and guarantees of the
            depth-proprtional resolution stratum retention policy.
        """
        spec = policy.GetSpec()

        return stratum_rank in get_retained_ranks(
            spec._degree,
            spec._interspersal,
            # +1 because of in-progress deposition
            num_stratum_depositions_completed + 1,
        )

FromPredKeepRank = GenDropRanksFromPredKeepRank(_PredKeepRank)
