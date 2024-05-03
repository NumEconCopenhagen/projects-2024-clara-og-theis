from scipy import optimize
from types import SimpleNamespace
import sympy as sm

class NashBargainingClass:
    
    def __init__(self):
        """ setup model """

        par = self.par = SimpleNamespace()
        val = self.val = SimpleNamespace()

        # model parameters for analytical solution
        par.w = sm.symbols('w')
        par.theta = sm.symbols('theta')
        par.d1 = sm.symbols('d1')
        par.d2 = sm.symbols('d2') 
        par.alpha = sm.symbols('alpha')

        # model parameter values for numerical solution
        val.theta = 60
        val.d1 = 10
        val.d2 = 0
        val.alpha = 1/3

    def analyticalsolution(self):
        " solve the one shot Nash bargaining problem analytically "
    
        par = self.par

        u1 = par.w
        u2 = par.theta - par.w
        objective = ((u1-par.d1)**par.alpha)*(u2)**(1-par.alpha)
        foc = sm.diff(objective,par.w)
        sol = sm.solve(foc,par.w)[0]

        sol_collected = sm.collect(sol, par.d1)
    
        return sol_collected
    
    def utility_1(self,w):
        """ calculate utility of worker """

        val = self.val
        return w
    
    def utility_2(self,w):
        """ calculate utility of worker """

        val = self.val
        return val.theta - w
    
    def numericalsolution(self):
        " solve the one shot Nash bargaining problem numerically"
    
        val = self.val

        # a. Objective function
        obj = lambda w: -((self.utility_1(w)**val.alpha)*(self.utility_2(w)**(1-val.alpha)))  

        # b. initial guess and bounds
        bounds = [(val.d1, val.theta)]
        initial_guess = val.d1

        #. b. Maximize surplus
        result = optimize.minimize(obj, initial_guess, bounds=bounds, method='Nelder-Mead') 
        #OBS overvej optimizer, fejl
    
        return result