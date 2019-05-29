import numpy as np
import torch

import pyro
import pyro.infer
import pyro.optim
import pyro.distributions as dist

pyro.set_rng_seed(101)
m0c = 0

def MO():
  global m0c
  v0 = pyro.sample("v0", dist.Normal(0, 1))
  v1 = pyro.sample("v1", dist.Normal(0, 1))
  v2 = pyro.sample("v2", dist.Normal(0, 1))
  v3 = v0 + v1 + v2
  m0c += 1
  print("m0", v3.item(), m0c)
  return v3

def G():
  sigma = pyro.param("sigma", torch.tensor(1.))
  v = pyro.sample("v", dist.Normal(0, sigma))
  return v

def M2(guess):
  
pyro.clear_param_store()

svi = pyro.infer.SVI(
  model=MO,
  guide=G,
  optim=pyro.optim.SGD({"lr":0.01, "momentum":0.1}),
  loss=pyro.infer.Trace_ELBO())

losses, mu, sigma = [], [], []
num_steps = 2000
for t in range(num_steps):
  print("loss", svi.step())

print(pyro.param("sigma").item())

