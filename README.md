# mcmas-multi-coalitions

MCMAS extension to consider multi coalitions. That is, mcmas is called for achieving the verification of a given ispl, but the coalitions of agents that make the formulae satisfied are returned to the user.

## Prerequisites

- MCMAS (https://vas.doc.ic.ac.uk/software/mcmas/)

## How to run

In what follows:
- path-to-mcmas: the path to the folder contain the mcmas executable
- mcmas-optional-parameters: the parameters to pass to mcmas when performing the verification (leave "" in case no parameters are needed)
- ispl-file: the ispl file on which to perform the verification

```bash
python mcmas-multi-coalitions.py path-to-mcmas mcmas-optional-parameters ispl-file
```

Note that, w.r.t. standard mcmas, here the ispl can be enriched to guide a parametric generation of the agents coalitions. Look the enhanced version of the dining_cryptographers ispl (modified w.r.t. the version available in mcmas).
Specifically, the Groups definition has changed as follows:
```
Groups
	g1 = {min: 2; max: 3; together: DinCrypt1~DinCrypt2; split: DinCrypt1~DinCrypt3};
end Groups
```
Instead of explicit reporting the agents of coalition g1, we can add requirements over the agent coalitions. The Python script will call mcmas and keep track of all the coalitions satisfying the listed requirements that are satisfied in the ispl model.
