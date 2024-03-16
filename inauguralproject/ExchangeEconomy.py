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
        X2A = (1-par.alpha)*(IA)
        return X1A,X2A

    def demand_B(self,p1):
        par = self.par

        #a. Income 
        IB = p1*(1-par.w1A)+(1-par.w2A)

        #b. Demand for good 1
        X1B = par.beta*(IB/p1)

        #c. Demand for good 2
        X2B = (1-par.beta)*(IB)
        return X1B,X2B


    #Find consumer optimum independent of price, evt. grid solve
    def find_pareto_improvements(self):
        # a. Initialize an array to store Pareto improvements
        pareto_improvements = []

        # loop through all possibilities
        for xA1 in range(N1):
            for xA2 in range(N2):
                
                if utilityA(x1A,x2A) >= utilityA(par.w1A,par.w2A) and utilityB((1-x1A),(1-x2A)) >= utilityA((1-par.w1A),(1-par.w2A)):
                    pareto_improvements.append((X1A,XA2))
    
        return pareto_improvements 

    def check_market_clearing(self,p1):

        par = self.par

        x1A,x2A = self.demand_A(p1)
        x1B,x2B = self.demand_B(p1)

        eps1 = x1A-par.w1A + x1B-(1-par.w1A)
        eps2 = x2A-par.w2A + x2B-(1-par.w2A)

        return eps1,eps2