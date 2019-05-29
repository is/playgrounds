import numpy as np
import torch

import pyro
import pyro.infer
import pyro.optim
import pyro.distributions as dist

pyro.set_rng_seed(101)

def m(loc):
  z1 = pyro.sample("z1", dist.Normal(loc, 1))
  z2 = pyro.sample("z2", dist.Normal(loc, 3))
  return z1 + z2

def g(loc):
  a = pyro.param("a", loc.clone())
  b = pyro.param("b", torch.tensor(2.3))
  return pyro.sample("z1", dist.Normal(a, b))

pyro.clear_param_store()
svi = pyro.infer.SVI(
  model=m,
  guide=g,
  optim=pyro.optim.SGD({"lr": 0.001, "momentum": 0.1}),
  loss=pyro.infer.Trace_ELBO())

losses, a,b  = [], [], []
guess = torch.tensor(0.)
num_steps = 2500
for t in range(num_steps):
    losses.append(svi.step(guess))
    a.append(pyro.param("a").item())
    b.append(pyro.param("b").item())

print('a = ', pyro.param("a").item())
print('b = ', pyro.param("b").item())
