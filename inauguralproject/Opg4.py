import ExchangeEconomy

import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt # baseline module
from mpl_toolkits.mplot3d import Axes3D # for 3d figures

from matplotlib import cm # for colormaps
plt.rcParams.update({"axes.grid":True,"grid.color":"black","grid.alpha":"0.25","grid.linestyle":"--"})
plt.rcParams.update({'font.size': 14})

# Create an instance of the class
economy_instance = ExchangeEconomy()

# Use the instance to call utility_A with x1A=1 and x2A=1
utility_value = economy_instance.utility_A(1, 1)

print(utility_value)

