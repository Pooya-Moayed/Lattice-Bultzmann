import numpy as np
from matplotlib import pyplot
import matplotlib.pyplot as plt
from IPython.display import display, clear_output
import time
import os

plot_every = 50
os.makedirs("frames", exist_ok=True)
dtype = np.float64

def distance(x1, y1, x2, y2):
  return np.sqrt((x2-x1)**2 + (y2-y1)**2)

def main():
  Nx = 400
  Ny = 100
  tao = 0.53
  Nt = 3000

  # lattice speeds and weights
  NL = 9
  cxs = np.array (
      [  0,   0,   0,   1,    1,    1,  -1,   -1,   -1]
  )
  cys = np.array (
      [  0,   1,  -1,   0,    1,   -1,   0,    1,   -1]
  )
  weights = np.array (
      [4/9, 1/9, 1/9, 1/9, 1/36, 1/36, 1/9, 1/36, 1/36] # sum to one
  )

  # initial conditions
  F = np.ones((Ny,Nx, NL)) + 0.01 * np.random.randn(Ny,Nx, NL)
  F[:, :, 3] = 2

  # Defining cylinder
  cylinder = np.full ((Ny, Nx), False)
  for y in range (0, Ny):
    for x in range (0, Nx):
      if distance(Nx//4, Ny//2, x, y)<13:
        cylinder[y] [x] = True
  # main loop
  for it in range(Nt):
    print(it)

    for i, cx, cy in zip(range(NL), cxs, cys):
      F[:, :, i] = np.roll(F[:, :, i], cx, axis=1)
      F[:, :, i] = np.roll(F[:, :, i], cy, axis=0)
    
    
  # Reflective boundaries
    bndryF = F[cylinder, :]
    bndryF = bndryF[:, [0, 2, 1, 6, 8, 7, 3, 5, 4]]

  # Fluid variables
    rho = np.sum (F, 2)
    ux = np.sum (F * cxs, 2) / rho
    uy = np.sum (F * cys, 2) / rho

    F[cylinder, :] = bndryF
    ux[cylinder] = 0
    uy[cylinder] = 0

  # Collision
    Feq = np.zeros(F.shape)
    for i, cx, cy, w in zip(range(NL), cxs, cys, weights):
      Feq[:, :, i] = rho * w * ( 1 + 3 * (cx*ux + cy*uy) + 9/2 * (cx * ux)**2 - 3/2 * (ux**2 + uy**2))

    F += -(1.0 / tao) * (F - Feq)

    #ploting

    if(it%plot_every == 0):
      pyplot.imshow(np.sqrt(ux**2 + uy**2))
      pyplot.pause(.01)
      pyplot.cla()
if __name__ == "__main__":
  main()