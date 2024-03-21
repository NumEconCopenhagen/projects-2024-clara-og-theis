import numpy as np
from types import SimpleNamespace 
from scipy import optimize
from matplotlib import pyplot as plt
from ExchangeEconomy import ExchangeEconomyClass

#a

# Initialize the economy
economy = ExchangeEconomyClass()

p1_values = list(0.5 + 2 * (i / 75) for i in range(76))
p1_values_array = np.array(p1_values)

print(p1_values_array)

utility_best = -np.inf 
bedst_p1 = np.nan

# Iterate over each value of p1
for p1 in p1_values_array:
    # Calculate agent A's demand and B's demand for goods 1 and 2 at price p1
    X1A, X2A = economy.demand_A(p1)  # Use agent A's demand
    X1B, X2B = economy.demand_B(p1)  # Use agent B's demand

    # Calculate the utility for agent A using the given formula
    utility = economy.utility_A(1-X1B, 1-X2B)
    
    # Update the best utility and corresponding p1 if the current utility is higher
    if utility > utility_best:
        utility_best = utility
        bedst_p1 = p1
        best_arguments = (X1A, X1B)  # Save demands directly

print(f'Best utility is {utility_best:.8f} at p1 = {bedst_p1:.8f}')
print(f' optimal allocation for A is as follows, x1: {1-X1B:.8f} and x2: {1-X2B:.8f}')


# b) same as in a but with where P>0
p1_values_array = np.linspace(0.0001,10,10000)

utility_best = -np.inf 
bedst_p1 = np.nan

for p1 in p1_values_array:
    # Calculate agent A's demand and B's demand for goods 1 and 2 at price p1
    X1A, X2A = economy.demand_A(p1)  # Use agent A's demand
    X1B, X2B = economy.demand_B(p1)  # Use agent B's demand

    # Calculate the utility for agent A using the given formula
    utility = economy.utility_A(1-X1B, 1-X2B)
    
    # Update the best utility and corresponding p1 if the current utility is higher
    if utility > utility_best:
        utility_best = utility
        bedst_p1 = p1
        best_arguments = (X1A, X1A)  # Save demands directly

print(f'Best utility is {utility_best:.8f} at p1 = {bedst_p1:.8f}')
