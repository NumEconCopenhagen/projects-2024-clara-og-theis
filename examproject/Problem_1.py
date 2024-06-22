import numpy as np
from types import SimpleNamespace
from scipy import optimize
import pandas as pd
import matplotlib.pyplot as plt

class ProductionEconomyCO2Taxation:
    def __init__(self):
        """Setting up the Production economy"""
        par = self.par = SimpleNamespace()

        # Firms
        par.A = 1.0
        par.gamma = 0.5
        
        # Households
        par.alpha = 0.3
        par.nu = 1.0
        par.epsilon = 2.0
        
        # Government
        par.tau = 0.0
        par.T = 0.0
        par.kappa = 0.1  # Social cost of carbon
        
        # Numeraire
        par.w = 1.0

    def labor_demand(self, w, p_j):
        """Calculate labor demand for firm j"""
        par = self.par
        return (par.gamma * p_j * par.A / w) ** (1 / (1 - par.gamma))

    def output(self, w, p_j):
        """Calculate output for firm j"""
        par = self.par
        ell_j = self.labor_demand(w, p_j)
        return par.A * ell_j ** par.gamma

    def profit(self, w, p_j):
        """Calculate profit for firm j"""
        par = self.par
        ell_j = self.labor_demand(w, p_j)
        return (1 - par.gamma) / par.gamma * w * ell_j

    def utility(self, c1, c2, ell):
        """Calculate utility for the consumer"""
        par = self.par
        return np.log(c1 ** par.alpha * c2 ** (1 - par.alpha)) - par.nu * ell ** (1 + par.epsilon) / (1 + par.epsilon)

    def consumption(self, ell):
        """Calculate optimal consumption"""
        par = self.par
        income = par.w * ell + par.T + self.profit(par.w, par.p1) + self.profit(par.w, par.p2)
        c1 = par.alpha * income / par.p1
        c2 = (1 - par.alpha) * income / (par.p2 + par.tau)
        return c1, c2

    def optimal_labor(self):
        """Calculate optimal labor supply"""
        par = self.par
        obj = lambda ell: -(self.utility(*self.consumption(ell), ell))
        result = optimize.minimize_scalar(obj, bounds=(0, 10), method='bounded')
        return result.x

    def check_market_clearing(self, p1, p2):
        """Check market clearing conditions"""
        par = self.par
        par.p1 = p1
        par.p2 = p2
        
        # Optimal labor supply
        ell_star = self.optimal_labor()
        
        # Firm 1 and Firm 2 outputs and labor demands
        ell1 = self.labor_demand(par.w, p1)
        y1 = self.output(par.w, p1)
        ell2 = self.labor_demand(par.w, p2)
        y2 = self.output(par.w, p2)
        
        # Consumer consumption
        c1_star, c2_star = self.consumption(ell_star)
        
        # Calculate the market errors
        labor_market_error = ell_star - (ell1 + ell2)
        good_market_1_error = c1_star - y1
        good_market_2_error = c2_star - y2

        return labor_market_error, good_market_1_error, good_market_2_error

    def find_equilibrium(self):
        """Find the equilibrium prices using Walras' law"""
        par = self.par
        obj = lambda p: np.sum(np.abs(self.check_market_clearing(p[0], p[1])[:2]))
        result = optimize.minimize(obj, [1.0, 1.0], bounds=((0.1, 2.0), (0.1, 2.0)), method='SLSQP')
        return result.x

    def social_welfare(self, tau):
        """Calculate social welfare for a given tau"""
        par = self.par
        par.tau = tau
        
        # Find equilibrium prices
        p1_eq, p2_eq = self.find_equilibrium()
        par.p1 = p1_eq
        par.p2 = p2_eq
        
        # Calculate optimal labor supply
        ell_star = self.optimal_labor()
        
        # Calculate outputs and utility
        y1_star = self.output(par.w, par.p1)
        y2_star = self.output(par.w, par.p2)
        c1_star, c2_star = self.consumption(ell_star)
        
        # Government budget balance condition
        par.T = tau * c2_star
        
        # Recalculate consumption with updated T
        c1_star, c2_star = self.consumption(ell_star)
        
        # Calculate utility and social welfare
        U = self.utility(c1_star, c2_star, ell_star)
        SWF = U - par.kappa * y2_star
        return SWF

    def find_optimal_tax(self):
        """Find the optimal tau and T to maximize social welfare"""
        result = optimize.minimize_scalar(lambda tau: -self.social_welfare(tau), bounds=(0, 10), method='bounded')
        optimal_tau = result.x
        self.par.tau = optimal_tau
        self.par.T = optimal_tau * self.output(self.par.w, self.par.p2)  # Calculate the corresponding T
        return optimal_tau, self.par.T
    
    def plot_swf(self):
        """Plot Social Welfare Function (SWF) against tau"""
        par = self.par
        
        # Range of tau values
        tau_values = np.linspace(0, 10, 100)
        swf_values = [self.social_welfare(tau) for tau in tau_values]
        
        # Find optimal tau
        optimal_tau, _ = self.find_optimal_tax()
        
        # Plot
        plt.figure(figsize=(10, 6))
        plt.plot(tau_values, swf_values, label='Social Welfare Function')
        plt.axvline(optimal_tau, color='r', linestyle='--', label=f'Optimal tau = {optimal_tau:.4f}')
        plt.xlabel('tau')
        plt.ylabel('Social Welfare Function')
        plt.title('Social Welfare Function vs tau')
        plt.legend()
        plt.grid(True)
        plt.show()

# Instantiate the class
economy = ProductionEconomyCO2Taxation()

# Question 1: Check market clearing conditions
p1_values = np.linspace(0.1, 2.0, 10)
p2_values = np.linspace(0.1, 2.0, 10)
market_clearing_results = []

for p1 in p1_values:
    for p2 in p2_values:
        labor_market_error, good_market_1_error, good_market_2_error = economy.check_market_clearing(p1, p2)
        market_clearing_results.append({
            'p1': p1,
            'p2': p2,
            'labor_market': labor_market_error,
            'good_market_1': good_market_1_error,
            'good_market_2': good_market_2_error
        })

# Display the results
df = pd.DataFrame(market_clearing_results)
print(df)

# Question 2: Find the equilibrium prices
p1_eq, p2_eq = economy.find_equilibrium()

# Display the equilibrium prices
print(f'Equilibrium prices: p1 = {p1_eq:.4f}, p2 = {p2_eq:.4f}')

# Question 3: Find the optimal tax tau and lump-sum transfer T
optimal_tau, optimal_T = economy.find_optimal_tax()

# Display the optimal tau and T
print(f'Optimal tax tau: {optimal_tau:.4f}')
print(f'Optimal lump-sum transfer T: {optimal_T:.4f}')

# Plot SWF
economy.plot_swf()
