from pgmpy.factors.discrete import DiscreteFactor, TabularCPD

# =================================================================
# probability distribution p.25
# =================================================================
dist = DiscreteFactor(
    variables=["X"],
    cardinality=[3],
    values=[0.45, 0.3, 0.25],
    state_names={"X": ["1", "2", "3"]},
)
print(dist)
# +------+----------+
# | X    |   phi(X) |
# +======+==========+
# | X(1) |   0.4500 |
# +------+----------+
# | X(2) |   0.3000 |
# +------+----------+
# | X(3) |   0.2500 |
# +------+----------+

# =================================================================
# joint probability and conditional probability p.25
# =================================================================
# this assumes we know the conditional probabilities P(X=x, Y=y)
joint = DiscreteFactor(
    variables=["X", "Y"],
    cardinality=[3, 2],
    values=[0.25, 0.2, 0.2, 0.1, 0.15, 0.1],
    state_names={"X": ["1", "2", "3"], "Y": ["0", "1"]},
)
print(joint)
# +------+------+------------+
# | X    | Y    |   phi(X,Y) |
# +======+======+============+
# | X(1) | Y(0) |     0.2500 |
# +------+------+------------+
# | X(1) | Y(1) |     0.2000 |
# +------+------+------------+
# | X(2) | Y(0) |     0.2000 |
# +------+------+------------+
# | X(2) | Y(1) |     0.1000 |
# +------+------+------------+
# | X(3) | Y(0) |     0.1500 |
# +------+------+------------+
# | X(3) | Y(1) |     0.1000 |
# +------+------+------------+

# show the marginal distributions
print(joint.marginalize(variables=["Y"], inplace=False))
# +------+----------+
# | X    |   phi(X) |
# +======+==========+
# | X(1) |   0.4500 |
# +------+----------+
# | X(2) |   0.3000 |
# +------+----------+
# | X(3) |   0.2500 |
# +------+----------+

print(joint.marginalize(variables=["X"], inplace=False))
# +------+----------+
# | Y    |   phi(Y) |
# +======+==========+
# | Y(0) |   0.6000 |
# +------+----------+
# | Y(1) |   0.4000 |
# +------+----------+

# =================================================================
# conditional probability distribution p. 28
# =================================================================
# P(Y|X) = P(X,Y) / P(X)
print(joint / dist)
# +------+------+------------+
# | X    | Y    |   phi(X,Y) |
# +======+======+============+
# | X(1) | Y(0) |     0.5556 |
# +------+------+------------+
# | X(1) | Y(1) |     0.4444 |
# +------+------+------------+
# | X(2) | Y(0) |     0.6667 |
# +------+------+------------+
# | X(2) | Y(1) |     0.3333 |
# +------+------+------------+
# | X(3) | Y(0) |     0.6000 |
# +------+------+------------+
# | X(3) | Y(1) |     0.4000 |
# +------+------+------------+

# specified explicitly as a table
PYgivenX = TabularCPD(
    variable="Y",
    variable_card=2,
    values=[[0.25 / 0.45, 0.2 / 0.3, 0.15 / 0.25], [0.2 / 0.45, 0.1 / 0.3, 0.1 / 0.25]],
    evidence=["X"],
    evidence_card=[3],
    state_names={"X": list("123"), "Y": list("01")},
)
print(PYgivenX)
# +------+--------------------+---------------------+------+
# | X    | X(1)               | X(2)                | X(3) |
# +------+--------------------+---------------------+------+
# | Y(0) | 0.5555555555555556 | 0.6666666666666667  | 0.6  |
# +------+--------------------+---------------------+------+
# | Y(1) | 0.4444444444444445 | 0.33333333333333337 | 0.4  |
# +------+--------------------+---------------------+------+

# =================================================================
# probabilty distributions
# =================================================================
import math

import torch
from pyro.distributions import Bernoulli, Categorical, Gamma, Normal

# show prob distributions
print(Categorical(probs=torch.tensor([0.45, 0.3, 0.25])))
print(Normal(loc=0.0, scale=1.0))
print(Bernoulli(probs=0.4))
print(Gamma(concentration=1.0, rate=2.0))

prob = 0.4
bern = Bernoulli(probs=prob)
# capture the log probability with log_prob
lprob = bern.log_prob(torch.tensor(1.0))
# confirming that lprob is the log probabilty as expected
print(lprob, math.log(prob))
# log_prob returns the original probability when exponentiated
print(prob, round(math.exp(lprob), 2))

# =================================================================
# simulating random variables p.40
# =================================================================
# pgmpy - generate n samples, retruns pd.DataFrame
dist.sample(n=5)
joint.sample(n=5)

# pyro - generate samples
cat = Categorical(probs=torch.tensor([0.45, 0.3, 0.25]))
cat.sample()  # return a single sample
cat.sample((1, 10))  # return a (n,m) tensors

# =================================================================
# creating a random process in pgmpy & pyro p.42
# =================================================================
from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.sampling import BayesianModelSampling

# P(x,y,z) = P(z)P(x|z)P(y|x,z)
# simplify w. assumption Y is conditionally independent of Z given X
# P(x,y,z) = P(z)P(x|z)P(y|x)

PZ = TabularCPD(
    variable="Z",
    variable_card=2,
    values=[[0.65], [0.35]],
    state_names={"Z": list("01")},
)

PXgivenZ = TabularCPD(
    variable="X",
    variable_card=2,
    values=[[0.8, 0.6], [0.2, 0.4]],
    evidence=["Z"],
    evidence_card=[2],
    state_names={"X": list("01"), "Z": list("01")},
)

PYgivenX = TabularCPD(
    variable="Y",
    variable_card=3,
    values=[[0.1, 0.8], [0.2, 0.1], [0.7, 0.1]],
    evidence=["X"],
    evidence_card=[2],
    state_names={"X": list("01"), "Y": list("123")},
)

# arguments are the edges of a directed graph
model = DiscreteBayesianNetwork([("Z", "X"), ("X", "Y")])
# add conditional probabilities to model
model.add_cpds(PZ, PXgivenZ, PYgivenX)

# create the sampling obj
generator = BayesianModelSampling(model)
generator.forward_sample(size=10)  # -> pd.DataFrame
