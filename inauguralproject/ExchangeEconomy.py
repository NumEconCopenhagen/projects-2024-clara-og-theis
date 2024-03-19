import numpy as np
from types import SimpleNamespace
from scipy import optimize

class ExchangeEconomyClass:

    def __init__(self):

        par = self.par = SimpleNamespace()

        # a. preferences
        par.alpha = 1/3
        par.beta = 2/3

        # b. endowments
        par.w1A = 0.8
        par.w2A = 0.3

    def utility_A(self,x1A,x2A):
        par = self.par
        return x1A**par.alpha*x2A**(1-par.alpha)

    def utility_B(self,x1B,x2B):
        par = self.par
        return x1B**par.beta*x2B**(1-par.beta)

    def demand_A(self,p1):
        par = self.par

        #a. Income
        IA = p1*par.w1A+par.w2A

        #b. Demand for good 1
        X1A = par.alpha*(IA/p1)

        #c. Demand for good 2
        X2A = (1-par.alpha)*IA
        return X1A,X2A

    def demand_B(self,p1):
        par = self.par

        #a. Income 
        IB = p1*(1-par.w1A)+(1-par.w2A)

        #b. Demand for good 1
        X1B = par.beta*(IB/p1)

        #c. Demand for good 2
        X2B = (1-par.beta)*IB
        return X1B,X2B

    def find_pareto_improvements(self,N1,N2,do_print=True):
        par = self.par

        # a. Initialize an array to store Pareto improvements
        shape_tuple = (N1,N2) #tuple of grid
        x1A_values = np.empty(shape_tuple)
        x2A_values = np.empty(shape_tuple)
        uA_values = np.empty(shape_tuple)
        uB_values = np.empty(shape_tuple)

        # a. Initialize lists to store Pareto improvements
        pareto_improvements = []

         # b. start from guess of x1=x2=0
        x1A_endowment = par.w1A
        x2A_endowment = par.w2A
        uA_endowment = self.utility_A(par.w1A,par.w2A)
        uB_endowment = self.utility_B((1-par.w1A),(1-par.w2A))

        # loop through all possibilities
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

                # iii. check if best sofar
                if uA_values[i,j] > uA_endowment and uB_values[i,j] > uB_endowment:
                    pareto_improvements.append((x1A, x2A))

                    #x1A_best = x1A_values[i,j]
                    #x2A_best = x2A_values[i,j] 
                    #uA_best = uA_values[i,j]
                    #uB_best = uA_values[i,j]

        return pareto_improvements

    def check_market_clearing(self,p1):
        par = self.par

        x1A,x2A = self.demand_A(p1)
        x1B,x2B = self.demand_B(p1)

        eps1 = x1A-par.w1A + x1B-(1-par.w1A)
        eps2 = x2A-par.w2A + x2B-(1-par.w2A)

        return eps1,eps2
    
    # Equilibrium
    def excess(self,p1):
        par = self.par
        x1A,x2A = self.demand_A(p1)
        x1B,x2B = self.demand_B(p1)
        eps1 = x1A-par.w1A + x1B-(1-par.w1A)

        return eps1
    
    def find_equilibrium_wage(self, p_low, p_high, do_grid_search = True,do_print = True):
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

        # Find the equilibrium wage
        p1_eq = optimize.brentq(self.excess, p_low, p_high)
        if do_print:
            print(f'\nMarket clearing price: {p1_eq:.2f}')


    def solver(self, N1, N2):
        #Grid search over kombinationer i pareto_improvements

        par = self.par

        obj = lambda x: -self.utility_A(x[0], x[1])  # utility function

        const = ({'type':'ineq','fun':lambda x: self.find_pareto_improvements(x[0],x[1],par)})

        x0 = np.array([par.w1A , par.w2A])  # Initial guess

        res = optimize.minimize(obj, x0=x0, constraints={'type': 'eq', 'fun': const}, method='SLSQP')

        return res

     def optimiser(self,N1,N2,do_print=True):
    
        # a. Initialize an array to store Pareto improvements
        shape_tuple = (N1,N2) #tuple of grid
        x1A_values = np.empty(shape_tuple)
        x2A_values = np.empty(shape_tuple)
        uA_values = np.empty(shape_tuple)
        uB_values = np.empty(shape_tuple)

         # b. start from guess 
        x1A_endowment = par.w1A
        x2A_endowment = par.w2A
        uA_endowment = self.utility_A(par.w1A,par.w2A)
        uB_endowment = self.utility_B((1-par.w1A),(1-par.w2A))

        # c. loop through all possibilities
        for i,j in self.find_pareto_improvements():
            
            # i. x1 and x2 (chained assignment)
            x1_values[i,j] = x1 = self.demand_A.X1A(self,p1)
            x2_values[i,j] = x2 = self.demand_A.X2A(self,p1)

            # iii. check if best sofar
            if u_values[i,j] > u_best:
                x1_best = x1_values[i,j]
                x2_best = x2_values[i,j] 
                u_best = u_values[i,j]
    
        # d. print
        if do_print:
            print_solution(x1_best,x2_best,u_best,I,p1,p2)

        return x1_best,x2_best,u_best,x1_values,x2_values,u_values
        

    