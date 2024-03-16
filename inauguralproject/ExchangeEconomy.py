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
        return x1B**par.alpha*x2B**(1-par.alpha)

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
        X1B = par.alpha*(IB/p1)

        #c. Demand for good 2
        X2B = (1-par.alpha)*(IB)
        return X1B,X2B

    def find_pareto_improvements(self):
        # a. Initialize an array to store Pareto improvements
        shape_tuple = (N1,N2) #tuple of grid
        x1_values = np.empty(shape_tuple)
        x2_values = np.empty(shape_tuple)
        uA_values = np.empty(shape_tuple)
        uB_values = np.empty(shape_tuple)

        # loop through all possibilities
        for i in range(N1):
            for j in range(N2):
                
                # i. x1A and x2A (chained assignment)
                x1A_values[i,j] = x1A = (i/(N1))
                x2A_values[i,j] = x2A = (j/(N2))

                # ii. utility
                if utility_A(x1A,x2A, alpha=alpha) >= utility_A(par.w1A,par.w2A, alpha=alpha) and utility_B((1-x1A),(1-x2A), beta=beta) >= utility_B((1-par.w1A),(1-par.w2A), beta=beta):
                    uA_values[i,j] = utility_A(x1A,x2A, alpha=alpha)
                    uB_values[i,j] = utility_B(x1B,x2B, beta=beta)
                else: 
                    uA_values[i,j] = utility_A(0,0, alpha=alpha)
                    uB_values[i,j] = utility_B(0,0, beta=beta)
    
        return 

        
    def check_market_clearing(self,p1):

        par = self.par

        x1A,x2A = self.demand_A(p1)
        x1B,x2B = self.demand_B(p1)

        eps1 = x1A-par.w1A + x1B-(1-par.w1A)
        eps2 = x2A-par.w2A + x2B-(1-par.w2A)

        return eps1,eps2