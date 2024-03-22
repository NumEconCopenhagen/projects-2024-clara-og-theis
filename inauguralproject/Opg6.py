import numpy as np
from types import SimpleNamespace 
from scipy import optimize
from matplotlib import pyplot as plt
from ExchangeEconomy import ExchangeEconomyClass

#a

# Initialize the economy
model = ExchangeEconomyClass()

model.solver_opg6()


#b 

#Utility of 3
model.find_equilibrium(p_low = 0.93, p_high = 0.95)
p1=0.94
X1A, X2A = model.demand_A(p1)
X1B, X2B = model.demand_B(p1)
Utility_opg3=model.utility_A(X1A, X2A)+model.utility_B(X1B, X2B)
print(Utility_opg3)

