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

#Utility for 3
model.find_equilibrium(p_low = 0.93, p_high = 0.95)
p1=0.94
X1A_opg3, X2A_opg3 = model.demand_A(p1)
X1B_opg3, X2B_opg3 = model.demand_B(p1)


#utility for 4
p1_values = list(0.5 + 2 * (i / 75) for i in range(76))
p1_values_array = np.array(p1_values)

utility_best = -np.inf 
bedst_p1 = np.nan

# Iterate over each value of p1
for p1 in p1_values_array:
    # Calculate agent A's demand and B's demand for goods 1 and 2 at price p1
    X1A, X2A = model.demand_A(p1)  # Use agent A's demand
    X1B, X2B = model.demand_B(p1)  # Use agent B's demand

    # Calculate the utility for agent A using the given formula
    utilityA = model.utility_A(1-X1B, 1-X2B)
    utilityB = model.utility_B(X1B, X2B)
    
    # Update the best utility and corresponding p1 if the current utility is higher
    if utilityA > utility_best:
        utility_bestA = utilityA
        utility_bestB = utilityB
        bedst_p1 = p1
        best_arguments = (X1A, X1B)  # Save demands directly
print(utility_bestA)
print(utility_bestB)

p1_values_array = np.linspace(0.0001,10,100000)

utility_best = -np.inf 
bedst_p1 = np.nan

for p1 in p1_values_array:
    # Calculate agent A's demand and B's demand for goods 1 and 2 at price p1
    X1A, X2A = model.demand_A(p1)  # Use agent A's demand
    X1B, X2B = model.demand_B(p1)  # Use agent B's demand

    # Calculate the utility for agent A using the given formula
    utility4A = model.utility_A(1-X1B, 1-X2B)
    utility4B = model.utility_B(X1B, X2B)
    # Update the best utility and corresponding p1 if the current utility is higher
    if utility4A > utility_best:
        utility_best4A = utility4A
        utility_best4B = utility4B  
        bedst_p1 = p1
        best_arguments = (X1A, X1A)  # Save demands directly

print(f'Best utility is {utility_best:.8f} at p1 = {bedst_p1:.8f}')




#3
print(model.utility_A(X1A, X2A)+model.utility_B(X1B, X2B))
#4a
print(utility_bestA+utility_bestB)
#4b
print(utility_best4A+utility_best4B)