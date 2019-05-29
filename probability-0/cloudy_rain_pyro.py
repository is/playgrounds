import numpy as np
import torch

import pyro
import pyro.infer
import pyro.optim
import pyro.distributions as dist

pyro.set_rng_seed(101)

def rain():
  cloudy = pyro.sample('cloudy', dist.Bernoulli(0.3))
  if (cloudy == 0):
    p = 0.1
  else:
    p = 0.8
  rain = pyro.sample('rain', dist.Bernoulli(p)) 
  return cloudy, rain.item()

conditioned_rain = pyro.condition(rain, {'cloudy': 0})

def rain_guide():
  a = pyro.param("a", torch.tensor(0.5))
  return pyro.sample('rain', dist.Bernoulli(a))

pyro.clear_param_store()
svi = pyro.infer.SVI(
  model=conditioned_rain,
  guide=rain_guide,
  optim=pyro.optim.SGD({"lr": 0.001, "momentum":0.1}),
  loss=pyro.infer.Trace_ELBO())

losses, a  = [], []
num_steps = 2500
for t in range(num_steps):
    losses.append(svi.step())
    a.append(pyro.param("a").item())

print('a = ', pyro.param('a').item())
