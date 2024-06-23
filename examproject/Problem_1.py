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
        return ((par.gamma * p_j * par.A) / w) ** (1 / (1 - par.gamma))

    def output(self, w, p_j):
        """Calculate output for firm j"""
        par = self.par
        ell_j = self.labor_demand(w, p_j)
        return par.A * (ell_j)** par.gamma

    def profit(self, w, p_j):
        """Calculate profit for firm j"""
        par = self.par
        ell_j = self.labor_demand(w, p_j)
        return (1 - par.gamma) / par.gamma * w * ell_j

    def utility(self, c1, c2, ell):
        """Calculate utility for the consumer"""
        par = self.par
        return np.log(c1 ** par.alpha * c2 ** (1 - par.alpha)) - par.nu * ell ** (1 + par.epsilon) / (1 + par.epsilon)

    def consumption(self, ell, p1, p2):
        """Calculate optimal consumption"""
        par = self.par
        income = par.w * ell + par.T + self.profit(par.w, p1) + self.profit(par.w, p2)
        c1 = par.alpha * (income / p1)
        c2 = (1 - par.alpha) * (income / (p2 + par.tau))
        return c1, c2

    def optimal_labor(self, p1, p2):
        """Calculate optimal labor supply"""
        par = self.par
        obj = lambda ell: -(self.utility(*self.consumption(ell, p1, p2), ell))
        initial_guess = 1.0
        result = optimize.minimize(obj, initial_guess, method='SLSQP')
        return result.x[0]

    def check_market_clearing(self, p1, p2):
        """Check market clearing conditions"""
        par = self.par
        
        # Optimal labor supply
        ell_star = self.optimal_labor(p1, p2)
        
        # Firm 1 and Firm 2 outputs and labor demands
        ell1 = self.labor_demand(par.w, p1)
        y1 = self.output(par.w, p1)
        ell2 = self.labor_demand(par.w, p2)
        y2 = self.output(par.w, p2)
        
        # Consumer consumption
        c1_star, c2_star = self.consumption(ell_star, p1, p2)
        
        # Calculate the market errors
        labor_market_error = ell_star - (ell1 + ell2)
        good_market_1_error = c1_star - y1
        good_market_2_error = c2_star - y2

        return [labor_market_error, good_market_1_error, good_market_2_error]  

    def find_equilibrium(self):
        """Find the equilibrium prices using Walras' law"""
        par = self.par

        # Initial guess for prices
        initial_guess = [1.0, 1.0]

        # Objective function
        obj = lambda x: np.squeeze(self.check_market_clearing(x[0], x[1])[:2])

        # Optimizing
        result = optimize.root(obj, initial_guess, method='hybr')

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
        ell_star = self.optimal_labor(par.p1, par.p2)
        
        # Calculate outputs and utility
        y1_star = self.output(par.w,  par.p1)
        y2_star = self.output(par.w,  par.p2)
        c1_star, c2_star = self.consumption(ell_star, par.p1, par.p2) 

        # Government budget balance condition
        par.T = tau * c2_star
        
        # Recalculate consumption with updated T
        c1_star, c2_star = self.consumption(ell_star, par.p1, par.p2) 

        # Calculate utility and social welfare
        U = self.utility(c1_star, c2_star, ell_star)
        SWF = U - par.kappa * y2_star
        return SWF

    def find_optimal_tax(self):
        """Find the optimal tau and T to maximize social welfare"""

        par = self.par
        
        result = optimize.minimize_scalar(lambda tau: -self.social_welfare(tau), bounds=(0, 1), method='bounded')
        
        optimal_tau = result.x
        optimal_T = optimal_tau * self.output(par.w, par.p2)  # Calculate the corresponding T
        
        return optimal_tau, optimal_T
    
    def plot_swf(self):
        """Plot Social Welfare Function (SWF) against tau"""
        par = self.par

        # Find optimal tau
        optimal_tau, _ = self.find_optimal_tax()
        
        # Range of tau values
        tau_values = np.linspace(0, 1, 100)
        swf_values = [self.social_welfare(tau) for tau in tau_values]
        
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