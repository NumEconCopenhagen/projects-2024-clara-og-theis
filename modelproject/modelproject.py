from scipy import optimize
from types import SimpleNamespace
import sympy as sm
import numpy as np
import matplotlib.pyplot as plt

class NashBargainingClass:
    
    def __init__(self):
        """ setup model """

        par = self.par = SimpleNamespace()
        val = self.val = SimpleNamespace()
        sim = self.sim = SimpleNamespace()

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
        val.alpha_vec = np.linspace(0,1,10)

        # parameter values for simulation
        sim.N = 10000
        sim.theta = np.random.normal(60, 10, sim.N)
        sim.d1 = 10
        sim.d2 = 0
        sim.alpha = 1/3

    def analyticalsolution(self):
        " solve the Nash bargaining problem analytically "
    
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
        obj = lambda w: -(((self.utility_1(w)-val.d1)**val.alpha)*((self.utility_2(w)-val.d2)**(1-val.alpha)))

        # b. initial guess and bounds
        bounds = [(val.d1, val.theta)]
        initial_guess = val.d1

        #. b. Maximize surplus
        result = optimize.minimize(obj, initial_guess, bounds=bounds, method='Nelder-Mead') 

        w =  f'w = {result.x[0]:.3f}'
    
        return w
    
    def varyingalpha(self):
        " solve the one shot Nash bargaining problem numerically for varying alpha values"
    
        val = self.val
        w_values = []  # Store w values for each alpha

        for alpha in val.alpha_vec:
            # a. Objective function
            obj = lambda w: -(((self.utility_1(w)-val.d1)**alpha)*((self.utility_2(w)-val.d2)**(1-alpha)))

            # b. initial guess and bounds
            bounds = [(val.d1, val.theta)]
            initial_guess = val.d1

            #. b. Maximize surplus
            result = optimize.minimize(obj, initial_guess, bounds=bounds, method='Nelder-Mead') 

            w = result.x[0]
            w_values.append(w)

        # Create a new figure
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)

        ax.plot(val.alpha_vec, w_values)
        ax.set_xlabel('Alpha')
        ax.set_ylabel('Wage')
        ax.set_title('Wage as a function of alpha')
        ax.grid(True)
    
        return fig
    
    def simulatewdistribution(self):
        sim = self.sim

        w_values = []  # Store w values for each individual
        
        for theta in sim.theta:
            # a. Objective function
            obj = lambda w: -(((self.utility_1(w)-sim.d1)**sim.alpha)*((theta-w-sim.d2)**(1-sim.alpha)))
            
            # b. initial guess and bounds
            bounds = [(sim.d1, theta)]
            initial_guess = sim.d1

            # Maximize surplus
            result = optimize.minimize(obj, initial_guess, bounds=bounds, method='Nelder-Mead') 

            w = result.x[0]
            w_values.append(w)

        # Plot the distribution of w
        plt.hist(w_values, bins=100)  # Adjust the number of bins as needed
        plt.xlabel('Wage')
        plt.ylabel('Frequency')
        plt.title('Distribution of Wages')
        plt.grid(True)
        plt.show()
    