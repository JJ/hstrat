"""Strata storage implementations for use with HereditaryStratigraphicColumn."""

from ._HereditaryStratumOrderedStoreDict import (
    HereditaryStratumOrderedStoreDict,
)
from ._HereditaryStratumOrderedStoreList import (
    HereditaryStratumOrderedStoreList,
)
from ._HereditaryStratumOrderedStoreTree import (
    HereditaryStratumOrderedStoreTree,
)

# adapted from https://stackoverflow.com/a/31079085
__all__ = [
    "HereditaryStratumOrderedStoreDict",
    "HereditaryStratumOrderedStoreList",
    "HereditaryStratumOrderedStoreTree",
]

from ..._auxiliary_lib import launder_impl_modules as _launder

_launder([eval(item) for item in __all__], __name__)
del _launder  # prevent name from leaking
