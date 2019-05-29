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
  r = pyro.sample('rain', dist.Bernoulli(p)) 
  return cloudy, r

for i in range(10):
  print(rain())

