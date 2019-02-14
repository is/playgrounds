import torch
import torch.nn as nn
import numpy as np

# ===
x = torch.tensor(1., requires_grad=True)
w = torch.tensor(2., requires_grad=True)
b = torch.tensor(3., requires_grad=True)

y = w * x + b
y.backward()

print(x.grad, w.grad, b.grad)


# ===
x = torch.randn(10, 3)
y = torch.randn(10, 2)

linear = nn.Linear(3, 2)
print ('w:', linear.weight)
print ('b:', linear.bias)

criterion = nn.MSELoss()
optimizer = torch.optim.SGD(linear.parameters(), lr=0.01)
pred = linear(x)
loss = criterion(pred, y)
print('loss: ', loss.item())

loss.backward()
print('dL/dw: ', linear.weight.grad)
print('dL/db: ', linear.bias.grad)
optimizer.step()

# Print out the loss after 1-step gradient descent.
pred = linear(x)
loss = criterion(pred, y)
print('loss after 1 step optimization: ', loss.item())
