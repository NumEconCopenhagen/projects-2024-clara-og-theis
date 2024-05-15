import numpy as np
from types import SimpleNamespace
from scipy import optimize

class ExchangeEconomyClass:

    def __init__(self):
        """ setup model """

        par = self.par = SimpleNamespace()

        # a. preferences
        par.alpha = 1/3
        par.beta = 2/3

        # b. endowments
        par.w1A = 0.8
        par.w2A = 0.3

    def utility_A(self,x1A,x2A):
        """ calculate utility of consumer A """

        par = self.par
        return x1A**par.alpha*x2A**(1-par.alpha)

    def utility_B(self,x1B,x2B):
        """ calculate utility of consumer B """

        par = self.par
        return x1B**par.beta*x2B**(1-par.beta)

    def demand_A(self,p1):
        """ calculate demand of consumer A """

        par = self.par

        #a. Income
        IA = p1*par.w1A+par.w2A

        #b. Demand for good 1
        X1A = par.alpha*(IA/p1)

        #c. Demand for good 2
        X2A = (1-par.alpha)*IA
        return X1A,X2A

    def demand_B(self,p1):
        """ calculate demand of consumer B """

        par = self.par

        #a. Income 
        IB = p1*(1-par.w1A)+(1-par.w2A)

        #b. Demand for good 1
        X1B = par.beta*(IB/p1)

        #c. Demand for good 2
        X2B = (1-par.beta)*IB
        return X1B,X2B

    def find_pareto_improvements(self,N1,N2):
        """ find pareto improvements compared to initial endowment """

        par = self.par

        # a. Initialize tuples
        shape_tuple = (N1,N2) #tuple of grid
        x1A_values = np.empty(shape_tuple)
        x2A_values = np.empty(shape_tuple)
        uA_values = np.empty(shape_tuple)
        uB_values = np.empty(shape_tuple)

        # b. Initialize lists to store Pareto improvements
        pareto_improvements = []

        # c. start from guess of endowments
        x1A_endowment = par.w1A
        x2A_endowment = par.w2A
        uA_endowment = self.utility_A(par.w1A,par.w2A)
        uB_endowment = self.utility_B((1-par.w1A),(1-par.w2A))

        # d. loop through all possibilities
        for i in range(N1):
            for j in range(N2):
                
                # i. Define x1A, x1B and utilities for every loop
                x1A_values[i,j] = x1A = (i/N1)
                x2A_values[i,j] = x2A = (j/N2)

                uA_values[i,j] = uA = self.utility_A(x1A,x2A)
                uB_values[i,j] = uB = self.utility_B(1-x1A,1-x2A)

                # ii. check if best sofar
                if uA_values[i,j] > uA_endowment and uB_values[i,j] > uB_endowment:
                    pareto_improvements.append((x1A, x2A))

        return pareto_improvements

    def check_market_clearing(self,p1):
        """ check market clearing conditions """

        par = self.par

        # a. define demand 
        x1A,x2A = self.demand_A(p1)
        x1B,x2B = self.demand_B(p1)

        # b. calculate the market error
        eps1 = x1A-par.w1A + x1B-(1-par.w1A)
        eps2 = x2A-par.w2A + x2B-(1-par.w2A)

        return eps1,eps2
    
    def excess(self,p1):
        """ calculate excess demand for good 1 """
        par = self.par
        
        # a. define demand 
        x1A,x2A = self.demand_A(p1)
        x1B,x2B = self.demand_B(p1)
        
        # b. calculate market error for the market of good 1
        eps1 = x1A-par.w1A + x1B-(1-par.w1A)

        return eps1
    
    def find_equilibrium(self, do_grid_search = True,do_print = True):
        """ find market clearing price """
        
        par = self.par

        # a. define prices
        p1_values = list(0.5 + 2 * (i / 75) for i in range(76))
        p1_values_array = np.array(p1_values)

        # b. find price interval where the market error is close to zero
        if do_grid_search:
            found_bracket = False
            for i,p in enumerate(p1_values_array):
                excess = self.excess(p)
                if do_print:
                    print(f'p= {p:.2f}, excess = {excess:.2f}')

                # save the bracket that contains 0
                if excess < 0 and not found_bracket:
                    p_low = p1_values_array[i-1]
                    p_high = p1_values_array[i]
                    found_bracket = True
        
        # c. find the equilibrium price
        p1_eq = optimize.brentq(self.excess, p_low, p_high)

        if do_print:
            print(f'\nMarket clearing price: {p1_eq:.4f}')

        # d. check that the markets clear
        eps1, eps2 = self.check_market_clearing(p1_eq)

        if do_print:
            print(f'\nMarket clearing errors: eps1 = {eps1:.2f}, eps2 = {eps2:.2f}')
            return None

        return p1_eq
        

    def Utility_max_a(self,do_print=True):
        """ maximize utility of consumer A for prices P"""

        # a. Define initial conditions for best utility and corresponding price
        utility_best = -np.inf
        best_p1 = np.nan
        p1_values = list(0.5 + 2 * (i / 75) for i in range(76))
        p1_values_array = np.array(p1_values)

        # b. Iterate over each value of p1
        for p1 in p1_values_array:
            # i. calculate A's demand and B's demand for goods 1 and 2 at price p1
            x1A, x2A = self.demand_A(p1)  # Use agent A's demand
            x1B, x2B = self.demand_B(p1)  # Use agent B's demand

            # ii. Calculate the utility for agent A using the given formula
            utility = self.utility_A(1-x1B, 1-x2B)

            # iii. Update the best utility and corresponding p1 if the current utility is higher
            if utility > utility_best:
                utility_best = utility
                best_p1 = p1
                best_X1A = 1-x1B
                best_X2A = 1-x2B
        
        if do_print: 
            print(f'Consumer As maximised utility is {utility_best:.4f} at p1 = {best_p1:.4f}')
            print(f'The allocation is then X1A = {best_X1A:.4f} and X2A = {best_X2A:.4f}')
            return None

        return best_X1A, best_X2A 
            
    def Utility_max_b(self,do_print=True):
        # Define initial conditions for best utility and corresponding price

        par = self.par

        # a. objective function (to minimize) 
        obj = lambda x: -self.utility_A(1-self.demand_B(x[0])[0], 1-self.demand_B(x[0])[1])  # utility function

        # b. call solver, use SLSQP
        initial_guess = 1 

        res = optimize.minimize(obj, initial_guess, method='SLSQP')
    
        # c. unpack and print solution
        p1 = res.x[0]
        X1A = 1 - self.demand_B(p1)[0]
        X2A = 1 - self.demand_B(p1)[1]
        uA = self.utility_A(X1A, X2A)

        if do_print: 
            print(f'Consumer As maximised utility is {uA:.4f} at p1 = {p1:.4f}')
            print(f'The allocation is then X1A = {X1A:.4f} and X2A = {X2A:.4f}')
            return None
        
        return X1A, X2A

    def pareto_optimizer(self,do_print=True):
        """ maximize utility of consumer A in pareto improvements"""

        par = self.par

        # a. start from guess which is the initial endowment
        X1A_best = par.w1A
        X2A_best = par.w2A
        uA_best = self.utility_A(par.w1A,par.w2A)

        # b. loop through all the pareto improvements
        for X1A,X2A in self.find_pareto_improvements(N1=76,N2=76):
            
            # i. Utility
            uA = self.utility_A(X1A,X2A)

            # iii. check if best sofar
            if uA > uA_best:
                X1A_best = X1A
                X2A_best = X2A 
                uA_best = uA

        if do_print: 
            print(f'The allocation is X1A = {X1A_best:.4f} and X2A = {X2A_best:.4f} with utility of consumer A at {uA_best:.4f}')
            return None

        return X1A_best, X2A_best

    def marketmaker_solver(self,do_print=True):
        """ maximize utility of consumer A where A is market maker"""

        par = self.par

        # a. objective function (to minimize) 
        obj = lambda x: -self.utility_A(x[0], x[1])  # utility function

        # b. constraints and bounds
        const = ({'type': 'ineq', 'fun': lambda x: self.utility_B(1-x[0],1-x[1]) - self.utility_B((1-par.w1A),(1-par.w2A))})
        bounds = ((0,1),(0,1))

        # c. call solver, use SLSQP
        initial_guess = np.array([par.w1A , par.w2A])  # Initial guess

        res = optimize.minimize(obj, initial_guess, bounds=bounds, constraints=const, method='SLSQP')
    
        # d. unpack and print solution
        x1A = res.x[0]
        x2A = res.x[1]
        uA = self.utility_A(x1A, x2A)

        if do_print: 
            print(f'The allocation is X1A = {x1A:.4f} and X2A = {x2A:.4f} with utility of consumer A at {uA:.4f}')
            return None

        return x1A, x2A 

   
    def socialplanner_solver(self,do_print=True):
        """ maximize aggregate utility """

        par = self.par

        # a. objective function (to minimize) 
        obj = lambda x: -self.utility_A(x[0], x[1])-self.utility_B(1-x[0], 1-x[1])  # utility function

        # b. Bounds
        bounds = ((0,1),(0,1))

        # c. call solver, use SLSQP
        initial_guess = np.array([par.w1A , par.w2A])  # Initial guess

        res = optimize.minimize(obj, initial_guess, bounds=bounds, method='SLSQP')
    
        # d. unpack and print solution
        x1A = res.x[0]
        x2A = res.x[1]
        x1B = 1 - x1A
        x2B = 1 - x2A
        uA = self.utility_A(x1A, x2A)
        uB = self.utility_B(x1B, x2B)

        if do_print: 
            print(f'The allocation is X1A = {x1A:.4f}, X2A = {x2A:.4f}, X1B = {x1B:.4f} and X2B = {x2B:.4f}')
            print(f'The utility of consumer A is {uA:.4f} and the utility of consumer B is {uB:.4f}')
            return None

        return x1A, x2A

    def setw(self, s):
        """ create random set of endowments """

        # a. set seed
        np.random.seed(2000)

        # b. draw uniformly distributed endowments
        w1A = np.random.uniform(size=s)
        w2A = np.random.uniform(size=s)

        # c. create a random set of endowments
        W = []
        for i in range(s):
            W.append((w1A[i], w2A[i]))
        
        return W
    
    def equilibriumallocation(self):
        """ find the market equilibrium allocation """

        par = self.par

        allocation=[]

        for i in range(50):
            w1A, w2A = self.setw(s=50)[i]
            par.w1A=w1A
            par.w2A=w2A

            p1_eq = self.find_equilibrium(do_print=False)
            x1A, x2A = self.demand_A(p1_eq)

            allocation.append((x1A, x2A))

        return allocation


