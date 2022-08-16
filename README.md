# hstrat

[
  ![PyPi](https://img.shields.io/pypi/v/hstrat.svg)
](https://pypi.python.org/pypi/hstrat)
[
  ![Travis CI](https://img.shields.io/travis/mmore500/hstrat.svg)
](https://travis-ci.com/mmore500/hstrat)
[
  ![Read The Docs](https://readthedocs.org/projects/hstrat/badge/?version=latest)
](https://hstrat.readthedocs.io/en/latest/?badge=latest)

hstrat enables phylogenetic inference on distributed digital evolution populations

* Free software: MIT license
* Documentation: <https://hstrat.readthedocs.io>

## Usage

```python3
from hstrat import hstrat

stratum_retention_policy = hstrat.geom_seq_nth_root_tapered_policy.Policy(
    parameterizer=hstrat.PropertyAtMostParameterizer(
        target_value=127,
        policy_evaluator \
            =hstrat.MrcaUncertaintyAbsExactPolicyEvaluator(
                at_num_strata_deposited=256,
                at_rank=0,
        ),
        param_lower_bound=1,
        param_upper_bound=1024,
    )
)

individual1 = hstrat.HereditaryStratigraphicColumn(
    stratum_retention_policy=stratum_retention_policy,
)
individual2 = hstrat.HereditaryStratigraphicColumn(
  stratum_retention_policy=stratum_retention_policy,
)

individual1_child1 = individual1.CloneDescendant()

individual1.HasAnyCommonAncestorWith(individual2) # -> False
individual1_child1.HasAnyCommonAncestorWith(individual2) # -> False

individual1_grandchild1 = individual1_child1.CloneDescendant()
individual1_grandchild2 = individual1_child1.CloneDescendant()

individual1_grandchild1.CalcRankOfMrcaBoundsWith(
  individual1_grandchild2,
) # -> (1, 2)
```


## How it Works

![](docs/assets/bitstring_inference.png)

![](docs/assets/stratigraph_inference.png)

![](docs/assets/pruning.png)

![](docs/assets/pruning_intensity.png)

![](docs/assets/pruning_distribution.png)

## Retention Drip Plot Visualization

| No History | Retained History | All History |
|------------|------------------|-------------|
| ![](docs/assets/a=stratum_retention_dripplot+extant_history=False+extinct_history=False+extinct_placeholders=True+num_generations=256+policy=tapered-depth-proportional-resolution-stratum-retention-policy-resolution-4+ext=.gif) | ![](docs/assets/a=stratum_retention_dripplot+extant_history=True+extinct_history=False+extinct_placeholders=True+num_generations=256+policy=tapered-depth-proportional-resolution-stratum-retention-policy-resolution-4+ext=.gif) | ![](docs/assets/a=stratum_retention_dripplot+extant_history=True+extinct_history=True+extinct_placeholders=False+num_generations=256+policy=tapered-depth-proportional-resolution-stratum-retention-policy-resolution-4+ext=.gif) |

## Available Policies

| Policy                                 | Space Complexity | MRCA Gen Uncertainty |
|----------------------------------------|------------------|----------------------|
| Fixed Resolution Policy                | `n/k`            | `k`                  |
| Recency Proportional Resolution Policy | `k * log(n)`     | `m/k`                |
| Depth Proportional Resolution Policy   | `k`              | `n/k`                |
| Geometric Sequence Nth Root Policy     | `k`              | `m * n^(1/k)`        |

### Depth Proportional Resolution Policy

| Sparse Parameterization | Dense Parameterization |
|-------------------------|------------------------|
| ![](docs/assets/a=policy_panel_plot+num_generations=256+policy=depth-proportional-resolution-stratum-retention-policy-resolution-2+ext=.gif) | ![](docs/assets/a=policy_panel_plot+num_generations=256+policy=depth-proportional-resolution-stratum-retention-policy-resolution-8+ext=.gif) |
| ![](docs/assets/num_generations=256+policy=depth-proportional-resolution-stratum-retention-policy-resolution-2+viz=stratum-retention-dripplot+ext=.png) | ![](docs/assets/num_generations=256+policy=depth-proportional-resolution-stratum-retention-policy-resolution-8+viz=stratum-retention-dripplot+ext=.png) |

| Dense Parameterization Detail | | |
| ------------------------------|-|-|
| ![](docs/assets/num_generations=256+policy=depth-proportional-resolution-stratum-retention-policy-resolution-8+viz=strata-retained-num-lineplot+ext=.png) | ![](docs/assets/num_generations=256+policy=depth-proportional-resolution-stratum-retention-policy-resolution-8+viz=mrca-uncertainty-absolute-barplot+ext=.png) | ![](docs/assets/num_generations=256+policy=depth-proportional-resolution-stratum-retention-policy-resolution-8+viz=mrca-uncertainty-relative-barplot+ext=.png) |

### Tapered Depth Proportional Resolution Policy

| Sparse Parameterization | Dense Parameterization |
|-------------------------|------------------------|
| ![](docs/assets/a=policy_panel_plot+num_generations=256+policy=tapered-depth-proportional-resolution-stratum-retention-policy-resolution-1+ext=.gif) | ![](docs/assets/a=policy_panel_plot+num_generations=256+policy=tapered-depth-proportional-resolution-stratum-retention-policy-resolution-7+ext=.gif) |
| ![](docs/assets/num_generations=256+policy=tapered-depth-proportional-resolution-stratum-retention-policy-resolution-1+viz=stratum-retention-dripplot+ext=.png) | ![](docs/assets/num_generations=256+policy=tapered-depth-proportional-resolution-stratum-retention-policy-resolution-7+viz=stratum-retention-dripplot+ext=.png) |

| Dense Parameterization Detail | | |
| ------------------------------|-|-|
| ![](docs/assets/num_generations=256+policy=tapered-depth-proportional-resolution-stratum-retention-policy-resolution-7+viz=strata-retained-num-lineplot+ext=.png) | ![](docs/assets/num_generations=256+policy=tapered-depth-proportional-resolution-stratum-retention-policy-resolution-7+viz=mrca-uncertainty-absolute-barplot+ext=.png) | ![](docs/assets/num_generations=256+policy=tapered-depth-proportional-resolution-stratum-retention-policy-resolution-7+viz=mrca-uncertainty-relative-barplot+ext=.png) |

### Fixed Resolution Policy

| Sparse Parameterization | Dense Parameterization |
|-------------------------|------------------------|
| ![](docs/assets/a=policy_panel_plot+num_generations=256+policy=fixed-resolution-stratum-retention-policy-resolution-128+ext=.gif) | ![](docs/assets/a=policy_panel_plot+num_generations=256+policy=fixed-resolution-stratum-retention-policy-resolution-32+ext=.gif) |
| ![](docs/assets/num_generations=256+policy=fixed-resolution-stratum-retention-policy-resolution-128+viz=stratum-retention-dripplot+ext=.png) | ![](docs/assets/num_generations=256+policy=fixed-resolution-stratum-retention-policy-resolution-32+viz=stratum-retention-dripplot+ext=.png) |

| Dense Parameterization Detail | | |
| ------------------------------|-|-|
![](docs/assets/num_generations=256+policy=fixed-resolution-stratum-retention-policy-resolution-32+viz=strata-retained-num-lineplot+ext=.png) | ![](docs/assets/num_generations=256+policy=fixed-resolution-stratum-retention-policy-resolution-32+viz=mrca-uncertainty-absolute-barplot+ext=.png) | ![](docs/assets/num_generations=256+policy=fixed-resolution-stratum-retention-policy-resolution-32+viz=mrca-uncertainty-relative-barplot+ext=.png) |

### Geometric Sequence Nth Root Policy

| Sparse Parameterization | Dense Parameterization |
|-------------------------|------------------------|
| ![](docs/assets/a=policy_panel_plot+num_generations=256+policy=nth-root-geometric-sequence-stratum-retention-policy-degree-6-interspersal-2+ext=.gif) | ![](docs/assets/a=policy_panel_plot+num_generations=256+policy=nth-root-geometric-sequence-stratum-retention-policy-degree-1024-interspersal-2+ext=.gif) |
| ![](docs/assets/num_generations=256+policy=nth-root-geometric-sequence-stratum-retention-policy-degree-6-interspersal-2+viz=stratum-retention-dripplot+ext=.png) | ![](docs/assets/num_generations=256+policy=nth-root-geometric-sequence-stratum-retention-policy-degree-1024-interspersal-2+viz=stratum-retention-dripplot+ext=.png) |

| Dense Parameterization Detail | | |
| ------------------------------|-|-|
| ![](docs/assets/num_generations=256+policy=nth-root-geometric-sequence-stratum-retention-policy-degree-1024-interspersal-2+viz=strata-retained-num-lineplot+ext=.png) | ![](docs/assets/num_generations=256+policy=nth-root-geometric-sequence-stratum-retention-policy-degree-1024-interspersal-2+viz=mrca-uncertainty-absolute-barplot+ext=.png) | ![](docs/assets/num_generations=256+policy=nth-root-geometric-sequence-stratum-retention-policy-degree-1024-interspersal-2+viz=mrca-uncertainty-relative-barplot+ext=.png) |

### Tapered Geometric Sequence Nth Root Policy

| Sparse Parameterization | Dense Parameterization |
|-------------------------|------------------------|
| ![](docs/assets/a=policy_panel_plot+num_generations=256+policy=tapered-nth-root-geometric-sequence-stratum-retention-policy-degree-1-interspersal-2+ext=.gif) | ![](docs/assets/a=policy_panel_plot+num_generations=256+policy=tapered-nth-root-geometric-sequence-stratum-retention-policy-degree-4-interspersal-2+ext=.gif)
| ![](docs/assets/num_generations=256+policy=tapered-nth-root-geometric-sequence-stratum-retention-policy-degree-1-interspersal-2+viz=stratum-retention-dripplot+ext=.png) | ![](docs/assets/num_generations=256+policy=tapered-nth-root-geometric-sequence-stratum-retention-policy-degree-4-interspersal-2+viz=stratum-retention-dripplot+ext=.png) |

| Dense Parameterization Detail | | |
| ------------------------------|-|-|
| ![](docs/assets/num_generations=256+policy=tapered-nth-root-geometric-sequence-stratum-retention-policy-degree-4-interspersal-2+viz=strata-retained-num-lineplot+ext=.png) | ![](docs/assets/num_generations=256+policy=tapered-nth-root-geometric-sequence-stratum-retention-policy-degree-4-interspersal-2+viz=mrca-uncertainty-absolute-barplot+ext=.png) | ![](docs/assets/num_generations=256+policy=tapered-nth-root-geometric-sequence-stratum-retention-policy-degree-4-interspersal-2+viz=mrca-uncertainty-relative-barplot+ext=.png) |

### Recency Proportional Resolution Policy

| Sparse Parameterization | Dense Parameterization |
|-------------------------|------------------------|
| ![](docs/assets/a=policy_panel_plot+num_generations=256+policy=recency-proportional-resolution-stratum-retention-policy-resolution-0+ext=.gif) | ![](docs/assets/a=policy_panel_plot+num_generations=256+policy=recency-proportional-resolution-stratum-retention-policy-resolution-6+ext=.gif) |
| ![](docs/assets/num_generations=256+policy=recency-proportional-resolution-stratum-retention-policy-resolution-0+viz=stratum-retention-dripplot+ext=.png) | ![](docs/assets/num_generations=256+policy=recency-proportional-resolution-stratum-retention-policy-resolution-6+viz=stratum-retention-dripplot+ext=.png) |

| Dense Parameterization Detail | | |
| ------------------------------|-|-|
| ![](docs/assets/num_generations=256+policy=recency-proportional-resolution-stratum-retention-policy-resolution-6+viz=strata-retained-num-lineplot+ext=.png) | ![](docs/assets/num_generations=256+policy=recency-proportional-resolution-stratum-retention-policy-resolution-6+viz=mrca-uncertainty-absolute-barplot+ext=.png) |  ![](docs/assets/num_generations=256+policy=recency-proportional-resolution-stratum-retention-policy-resolution-6+viz=mrca-uncertainty-relative-barplot+ext=.png) |

### Other Policies

* nominal resolution policy
* perfect resolution policy
* pseudostochastic policy
* stochastic policy

## Available Parameterizers

* `PropertyAtMostParameterizer`
* `PropertyAtLeastParameterizer`
* `PropertyExactlyParameterizer`


* `MrcaUncertaintyAbsExactPolicyEvaluator`
* `MrcaUncertaintyAbsUpperBoundPolicyEvaluator`
* `MrcaUncertaintyRelExactPolicyEvaluator`
* `MrcaUncertaintyRelUpperBoundPolicyEvaluator`
* `NumStrataRetainedExactPolicyEvaluator`
* `NumStrataRetainedUpperBoundPolicyEvaluator`

## Credits

This package was created with Cookiecutter and the `audreyr/cookiecutter-pypackage` project template.
