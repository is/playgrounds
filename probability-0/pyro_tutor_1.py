import numpy as np
import torch
from torch.distributions import constraints

import pyro
import pyro.infer
import pyro.optim
import pyro.distributions as dist

pyro.set_rng_seed(101)

def scale(guess):
  weight = pyro.sample("weight", dist.Normal(guess, 1.0))
  return pyro.sample("measurement", dist.Normal(weight, 0.75))

conditioned_scale = pyro.condition(scale, data={"measurement":9.5})

def scale_parametrized_guide(guess):
  a = pyro.param("a", guess.clone())
  b = pyro.param("b", torch.tensor(1.), constraint=constraints.positive)
  return pyro.sample("weight", dist.Normal(a, b))

guess = torch.tensor(8.5)
pyro.clear_param_store()

svi = pyro.infer.SVI(
  model=conditioned_scale,
  guide=scale_parametrized_guide,
  optim=pyro.optim.SGD({"lr": 0.001, "momentum": 0.1}),
  loss=pyro.infer.Trace_ELBO())

losses, a, b = [], [], []
num_steps = 2500

for t in range(num_steps):
  losses.append(svi.step(guess))
  a.append(pyro.param("a").item())
  b.append(pyro.param("b").item())

print('a=%f' % pyro.param("a").item())
print('b=%f' % pyro.param("b").item())

