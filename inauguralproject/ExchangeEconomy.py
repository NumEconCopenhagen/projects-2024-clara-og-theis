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

    def find_pareto_improvements(self,N1,N2,do_print=True):
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

                # ii. utility
                #if p1*x1A + x2A <= IA: 
                    #uA_values[i,j] = self.utility_A(x1A,x2A)
                    #uB_values[i,j] = self.utility_B(1-X1A,1-X2A)
                #else: 
                    #uA_values[i,j] = self.utility_A(par.w1A,par.w2A)
                    #uB_values[i,j] = self.utility_B((1-par.w1A),(1-par.w2A))

                # i. check if best sofar
                if uA_values[i,j] > uA_endowment and uB_values[i,j] > uB_endowment:
                    pareto_improvements.append((x1A, x2A))

        return pareto_improvements

    def check_market_clearing(self,p1):
        """ cheack market clearing conditions """

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
    
    def find_equilibrium(self, p_low, p_high, do_grid_search = True,do_print = True):
        """ find market clearing price """
        
        par = self.par

        p1_values = list(0.5 + 2 * (i / 75) for i in range(76))
        p1_values_array = np.array(p1_values)

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
        
        print(f'\nEquilibrium is in interval [{p_low:.2f}, {p_high:.2f}]')

        # Find the equilibrium price
        p1_eq = optimize.brentq(self.excess, p_low, p_high)
        if do_print:
            print(f'\nMarket clearing price: {p1_eq:.2f}')

    def optimizer(self,do_print=True):
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
                u_best = uA

        # c. print solution
        if do_print:
            self.print_solution(X1A_best,X2A_best,u_best) 
    
        return X1A_best, X2A_best, u_best


    def solver(self,do_print=True):
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
            self.print_solution(x1A,x2A,uA)   

        return x1A, x2A, uA

    def print_solution(self,x1A,x2A,uA):
        """ print solution """

        print(f'x1A = {x1A:.4f}')
        print(f'x2A = {x2A:.4f}')
        print(f'uA  = {uA:.4f}')
   
    def solver_opg6(self,do_print=True):
        """ XX """

        par = self.par

        # a. objective function (to minimize) 
        obj = lambda x: -self.utility_A(x[0], x[1])-self.utility_B(1-x[0], 1-x[1])  # utility function

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
            self.print_solution(x1A,x2A,uA)   

        return x1A, x2A, uA

    def setw(self, s1,s2):
        """ create random set of endowments """

        # a. set seed
        np.random.seed(2000)

        # b. draw uniformly distributed endowments
        w1A = np.random.uniform(size=s1)
        w2A = np.random.uniform(size=s2)

        # c. create a random set of endowments
        W  = list(zip(w1A,w2A))
        
        return W
    

    def excessopg8(self,p1, N1):
        """ calculate excess demand for good 1 """
        par = self.par

        # a. Initialize tuples
        shape_tuple = (N1) #tuple of grid
        x1A_values = np.empty(shape_tuple)
        x2A_values = np.empty(shape_tuple)
        x1B_values = np.empty(shape_tuple)
        x2B_values = np.empty(shape_tuple)
        eps1_values = np.empty(shape_tuple)
        uA_values = np.empty(shape_tuple)
        uB_values = np.empty(shape_tuple)
        
        for w1A,w2A in self.setw(s1 = 50, s2 = 50):
            # b. define demand 
            x1A_values,x2A_values = self.demand_A(p1, w1A)
            x1B_values,x2B_values = self.demand_B(p1, w2A)
        
             # c. calculate market error for the market of good 1
            eps1_values = x1A-w1A + x1B-(1-w1A)

        return eps1_values
    
    def find_equilibrium_opg8(self, p_low, p_high, do_grid_search = True,do_print = True):
        """ find market clearing price """
        
        par = self.par

        p1_values = list(0.5 + 2 * (i / 75) for i in range(76))
        p1_values_array = np.array(p1_values)

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
        
        print(f'\nEquilibrium is in interval [{p_low:.2f}, {p_high:.2f}]')

        # Find the equilibrium price
        p1_eq = optimize.brentq(self.excess, p_low, p_high)
        if do_print:
            print(f'\nMarket clearing price: {p1_eq:.2f}')

 