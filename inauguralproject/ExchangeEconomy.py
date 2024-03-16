import numpy as np
from types import SimpleNamespace

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
    

        