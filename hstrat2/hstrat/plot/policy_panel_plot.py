from matplotlib import pyplot as plt
import typing

from ...helpers import ScalarFormatterFixedPrecision

from .mrca_uncertainty_absolute_barplot import mrca_uncertainty_absolute_barplot
from .mrca_uncertainty_relative_barplot import mrca_uncertainty_relative_barplot
from .strata_retained_frac_lineplot import strata_retained_frac_lineplot
from .strata_retained_num_lineplot import strata_retained_num_lineplot
from .stratum_retention_dripplot import stratum_retention_dripplot

def policy_panel_plot(
    stratum_retention_policy: typing.Any,
    num_generations: int,
    do_show: bool=True,
    fig: typing.Optional[plt.matplotlib.figure.Figure]=None,
) -> plt.matplotlib.figure.Figure:
    """Draw multipanel figure to holisticaly describe stratum retention policy
    at a particular generation.

    Parameters
    ----------
    stratum_retention_policy: any
        Object specifying stratum retention policy.
    num_generations: int
        Number of generations to plot.
    do_show : bool, optional
        Whether to show() the plot automatically.
    fig : matplotlib/pylab figure, optional
        If a valid matplotlib.figure.Figure instance, the plot is drawn in that
        Figure. By default (None), a new figure is created.
     """

    if fig is None:
        fig = plt.figure(figsize=(8, 6))
    elif not isinstance(fig, plt.matplotlib.figure.Figure):
        raise ValueError(f"Invalid argument for fig: {fig}")

    top_left_ax = fig.add_subplot(3, 2, 1)
    mid_left_ax = fig.add_subplot(3, 2, 3)
    bot_left_ax = fig.add_subplot(3, 2, 5)
    top_right_ax = fig.add_subplot(2, 2, 2)
    bot_right_ax = fig.add_subplot(2, 2, 4)
    fig.suptitle(str(stratum_retention_policy))

    # left column
    stratum_retention_dripplot(
        stratum_retention_policy=stratum_retention_policy,
        num_generations=num_generations,
        ax=top_left_ax,
        do_show=False,
    )
    mrca_uncertainty_absolute_barplot(
        stratum_retention_policy=stratum_retention_policy,
        num_generations=num_generations,
        ax=mid_left_ax,
        do_show=False,
    )
    mrca_uncertainty_relative_barplot(
        stratum_retention_policy=stratum_retention_policy,
        num_generations=num_generations,
        ax=bot_left_ax,
        do_show=False,
    )

    # right column
    strata_retained_num_lineplot(
        stratum_retention_policy=stratum_retention_policy,
        num_generations=num_generations,
        ax=top_right_ax,
        do_show=False,
    )

    strata_retained_frac_lineplot(
        stratum_retention_policy=stratum_retention_policy,
        num_generations=num_generations,
        ax=bot_right_ax,
        do_show=False,
    )

    #TODO bot_right_ax text panel with params etc

    top_left_ax.get_yaxis().set_label_coords(-0.15, 0.5)
    mid_left_ax.get_yaxis().set_label_coords(-0.15, 0.5)
    bot_left_ax.get_yaxis().set_label_coords(-0.15, 0.5)
    top_right_ax.set(xlabel=None)
    top_left_ax.set(xlabel=None)
    mid_left_ax.set(xlabel=None)
    fig.subplots_adjust(wspace=0.3)
    fig.subplots_adjust(hspace=0.3)

    # can't reuse single object due to side effects between plots
    def make_fixed_prec_sci_formatter():
        formatter = ScalarFormatterFixedPrecision()
        formatter.set_scientific(True)
        formatter.set_powerlimits((0,0))
        return formatter
    top_left_ax.yaxis.set_major_formatter(make_fixed_prec_sci_formatter())
    mid_left_ax.yaxis.set_major_formatter(make_fixed_prec_sci_formatter())
    bot_left_ax.yaxis.set_major_formatter(make_fixed_prec_sci_formatter())
    top_right_ax.yaxis.set_major_formatter(make_fixed_prec_sci_formatter())

    if do_show: plt.show()

    return fig
