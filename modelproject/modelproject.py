from scipy import optimize
from types import SimpleNamespace
import sympy as sm
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display, clear_output
from ipywidgets import interact, FloatSlider, IntSlider, Button, Layout
import ipywidgets as widgets

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
        val.alpha_vec = np.linspace(0,1,10)

        np.random.seed(100) 
        val.N = 10000
        val.theta_vec = np.random.normal(60, 10, val.N)
        val.m = 20


    def analyticalsolution(self):
        """ solve the Nash bargaining problem analytically """
    
        par = self.par

        # a. define utility 
        u1 = par.w
        u2 = par.theta - par.w

        # b. define the object
        objective = ((u1-par.d1)**par.alpha)*(u2)**(1-par.alpha)

        # c. find the solution as the wage where the differentiated objective equals zero (FOC)
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
        """ solve the Nash bargaining problem numerically"""
    
        val = self.val

        # a. objective function
        obj = lambda w: -(((self.utility_1(w)-val.d1)**val.alpha)*((self.utility_2(w)-val.d2)**(1-val.alpha)))

        # b. initial guess and bounds
        bounds = [(val.d1, val.theta)]
        initial_guess = val.d1

        # c. maximize surplus
        result = optimize.minimize(obj, initial_guess, bounds=bounds, method='Nelder-Mead') 

        w = result.x[0]
    
        return w
    
    def varyingalpha(self):
        """ solve the Nash bargaining problem numerically for varying alpha values """
    
        val = self.val
        w_values = []  # Store w values for each alpha

        for alpha in val.alpha_vec:
            val.alpha = alpha
            
            w = self.numericalsolution()
            w_values.append(w)
        
        # Create a new figure
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)

        ax.plot(val.alpha_vec, w_values)
        ax.set_xlabel('Alpha')
        ax.set_ylabel('Wage')
        ax.set_title('Wage as a function of alpha')
        ax.grid(True)
        plt.show()
    
    def simulatewdistribution(self):
        """ simulate wage distribution """

        val = self.val
        val.alpha = 1/3 #redefine the global value of alpha

        w_values = []  # Store w values for each individual
        
        for theta in val.theta_vec:
            # a. Objective function
            obj = lambda w: -(((self.utility_1(w)-val.d1)**val.alpha)*((theta-w-val.d2)**(1-val.alpha)))
            
            # b. initial guess and bounds
            bounds = [(val.d1, theta)]
            initial_guess = val.d1

            # c. maximize surplus
            result = optimize.minimize(obj, initial_guess, bounds=bounds, method='Nelder-Mead') 

            w = result.x[0]
            w_values.append(w)

        # Plot the distribution of w
        plt.hist(w_values, bins=100, range=(15, 40))  
        plt.xlabel('Wage')
        plt.ylabel('Frequency')
        plt.title('Distribution of Wages')
        plt.grid(alpha=0.3)
        plt.show()

    def minimumwage(self):
        """ simulate wage distribution with a minimum wage """

        val = self.val

        w_values = []  # Store w values for each individual
        
        for theta in val.theta_vec:
            if theta >= val.m:
                # a. Objective function
                obj = lambda w: -(((self.utility_1(w)-val.d1)**val.alpha)*((theta-w-val.d2)**(1-val.alpha)))
            
                # b. initial guess and bounds
                bounds = [(val.m, theta)]
                initial_guess = val.m

                # c. maximize surplus
                result = optimize.minimize(obj, initial_guess, bounds=bounds, method='Nelder-Mead') 

                w = result.x[0]
                w_values.append(w)

        # Plot the distribution of w
        plt.hist(w_values, bins=100, range=(15, 40)) 
        plt.xlabel('Wage')
        plt.ylabel('Frequency')
        plt.title('Distribution of Wages with a Minimum Wage')
        plt.grid(alpha=0.3)
        plt.show()


    def interactive_plot(self):
        """ Interactive plot for exploring Nash Bargaining Model """
        def update(change):
            clear_output(wait=True)
            display(alpha_slider, theta_slider, d1_slider, d2_slider, m_slider, update_button)
            self.val.alpha = alpha_slider.value
            self.val.theta = theta_slider.value
            self.val.d1 = d1_slider.value
            self.val.d2 = d2_slider.value
            self.val.m = m_slider.value
            wage = self.numericalsolution()
            print(f"Calculated wage: {wage}")

            # Simulate distribution of wages
            self.minimumwage()

        # Customize slider width and description width
        slider_layout = Layout(width='600px', margin='0px 0px 0px 20px')  # Adjust the left margin as needed
        description_width = 'initial'  # This setting helps to avoid cutting off the descriptions

        alpha_slider = widgets.FloatSlider(
        value=1/3, min=0, max=1, step=0.01,
        description='Alpha: Bargaining power of the worker',
        style={'description_width': description_width},
          layout=slider_layout
        )
        theta_slider = widgets.IntSlider(
        value=60, min=40, max=80, step=1,
        description='Theta: Productivity of the worker',
        style={'description_width': description_width},
        layout=slider_layout
        )
        d1_slider = widgets.IntSlider(
        value=10, min=0, max=20, step=1,
        description='d1: Minimum acceptable conditions',
        style={'description_width': description_width},
        layout=slider_layout
        )
        d2_slider = widgets.IntSlider(
        value=0, min=0, max=10, step=1,
        description='d2: Minimum acceptable conditions',
        style={'description_width': description_width},
        layout=slider_layout
        )
        m_slider = widgets.IntSlider(
        value=20, min=15, max=30, step=1,
        description='Minimum Wage: Minimum wage constraint on the bargaining outcome',
        style={'description_width': description_width},
        layout=slider_layout
        )

        # Button to trigger the update
        update_button = Button(description='Update Results')
        update_button.on_click(update)
        
        # Display widgets
        display(alpha_slider, theta_slider, d1_slider, d2_slider, m_slider, update_button)

