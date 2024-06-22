import numpy as np
from types import SimpleNamespace
from scipy import optimize
import pandas as pd

class ProductionEconomyCO2Taxation:

    def __init__(self):
        """ setup model """

        self.par = SimpleNamespace()

        # a. Initialize parameters
        self.par.alpha = 0.5
        self.par.nu = 1.0
        self.par.epsilon = 0.5
        self.par.gamma = 0.5
        self.par.A = 1.0
        self.par.tau = 0.0
        self.par.T = 0.0
        self.par.w = 1.0  # numeraire
        self.par.p1 = 1.0
        self.par.p2 = 1.0

    def labor_demand(self, w, p_j):
        """ Calculate labor demand for firm j """
        par = self.par
        return (par.gamma * p_j * par.A / w) ** (1 / (1 - par.gamma))

    def output(self, w, p_j):
        """ Calculate output for firm j """
        par = self.par
        ell_j = self.labor_demand(w, p_j)
        return par.A * ell_j ** par.gamma

    def profit(self, w, p_j):
        """ Calculate profit for firm j """
        par = self.par
        ell_j = self.labor_demand(w, p_j)
        return (1 - par.gamma) * w * ell_j

    def utility(self, c1, c2, ell):
        """ Calculate utility for the consumer """
        par = self.par
        return np.log(c1 ** par.alpha * c2 ** (1 - par.alpha)) - par.nu * ell ** (1 + par.epsilon) / (1 + par.epsilon)

    def consumption(self, ell):
        """ Calculate optimal consumption """
        par = self.par
        income = par.w * ell + par.T + self.profit(par.w, par.p1) + self.profit(par.w, par.p2)
        c1 = par.alpha * income / par.p1
        c2 = (1 - par.alpha) * income / (par.p2 + par.tau)
        return c1, c2

    def optimal_labor(self):
        """ Calculate optimal labor supply """
        par = self.par
        obj = lambda ell: -(self.utility(*self.consumption(ell), ell))
        result = optimize.minimize_scalar(obj)
        return result.x

    def market_clearing(self):
        """ Market clearing conditions """
        par = self.par
        ell1 = self.labor_demand(par.w, par.p1)
        ell2 = self.labor_demand(par.w, par.p2)
        ell_star = self.optimal_labor()

        y1_star = self.output(par.w, par.p1)
        y2_star = self.output(par.w, par.p2)

        c1_star, c2_star = self.consumption(ell_star)

        return {
            'labor_market': ell_star - (ell1 + ell2),
            'good_market_1': c1_star - y1_star,
            'good_market_2': c2_star - y2_star
        }

    def check_market_clearing_conditions(self, threshold=0.5):
        """ Check market clearing conditions for p1 and p2 in given ranges """
        par = self.par
        p1_values = np.linspace(0.1, 2.0, 10)
        p2_values = np.linspace(0.1, 2.0, 10)
        results = []

        for p1 in p1_values:
            for p2 in p2_values:
                par.p1 = p1
                par.p2 = p2
                market_conditions = self.market_clearing()
                if (abs(market_conditions['labor_market']) < threshold and
                    abs(market_conditions['good_market_1']) < threshold and
                    abs(market_conditions['good_market_2']) < threshold):
                    results.append({
                        'p1': p1,
                        'p2': p2,
                        'labor_market': market_conditions['labor_market'],
                        'good_market_1': market_conditions['good_market_1'],
                        'good_market_2': market_conditions['good_market_2']
                    })

        return results

# Instantiate the class and check market clearing conditions with the threshold
economy = ProductionEconomyCO2Taxation()
market_clearing_results = economy.check_market_clearing_conditions(threshold=0.5)

# Display the results
df = pd.DataFrame(market_clearing_results)
print(df)
