import math
import numpy as np
import torch.nn as nn
import torch

SAMPLE_SIZE = 5000000
VARIABLE_NUMBER = 3
BIN_NUMBER = 200
C = BIN_NUMBER // 2
EPOCH_NUMBER = 100000

def hist(a, bn):
  amin = np.min(a)
  amax = np.max(a)
  if np.abs(amin) < amax:
    b0 = amax
  else:
    b0 = np.abs(amin)
  return np.histogram(a, bn, range=(-b0, b0))
    


random_variables = np.random.randn(SAMPLE_SIZE, VARIABLE_NUMBER)
rv1 = np.random.randn(SAMPLE_SIZE)
rv2 = np.random.randn(SAMPLE_SIZE)
rv3 = np.random.randn(SAMPLE_SIZE)
sum_variable = rv1 + rv2 + rv3
#sum_variable = np.random.randn(SAMPLE_SIZE)
#hist, edges = np.histogram(sum_variable, BIN_NUMBER)
hist, edges = hist(sum_variable, BIN_NUMBER)
bin_width = edges[2] - edges[1]
x = torch.from_numpy(edges.astype(np.float32))
y = torch.from_numpy((hist/SAMPLE_SIZE).astype(np.float32))
#ys = torch.sum(y)
#print(ys)

sigma = torch.tensor(1.25, requires_grad=True)
mu = torch.tensor(0., requires_grad=True)

optimizer = torch.optim.SGD([sigma, mu], lr=0.01)
criterion = nn.MSELoss(reduction='sum')


for epoch in range(EPOCH_NUMBER):
  pred_edge = 1/(np.sqrt(2 * np.pi)*sigma)*torch.exp(-0.5/(sigma**2) * ((x - mu)**2))
  pred = (pred_edge[:-1] + pred_edge[1:]) / 2 * bin_width
  loss = criterion(pred, y)
  optimizer.zero_grad()
  loss.backward()
  optimizer.step()

  if epoch % 1000 != 0:
    continue
  print('epoch:{}, loss:{}, mu={}, sigma={} - {}/{}'
    .format(epoch, loss.item(), mu, sigma, torch.sum(pred), torch.sum(y)))

