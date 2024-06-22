from scipy import optimize
from types import SimpleNamespace
import sympy as sm
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display, clear_output
from ipywidgets import interact, FloatSlider, IntSlider, Button, Layout
import ipywidgets as widgets

class CareerChoiceClass:
    
    def __init__(self):
        """ setup model """

        par = self.par = SimpleNamespace()
        par.J = 3
        par.N = 10
        par.K = 10000

        par.F = np.arange(1,par.N+1)
        par.sigma = 2

        par.v = np.array([1,2,3])
        par.c = 1

    def simulation(self, do_print = True):
        """ Simulate and calculate expected utility and the average realised utility """

        par = self.par
        np.random.seed(2024)

        # Simulate epsilon values for each career track
        epsilon = np.random.normal(0, par.sigma, (par.J, par.K))

        # Calculate expected utility for each career track
        expected_utility = par.v + np.mean(epsilon, axis=1)

        # Calculate average realized utility for each career track
        realized_utility = par.v[:, np.newaxis] + epsilon

        average_realized_utility = np.mean(realized_utility, axis=1)

        if do_print:
            print('\nExpected utility for each career track:')
            for j in range(par.J):
                print(f'Career track {j + 1}: {expected_utility[j]:.2f}')

            print('\nAverage realized utility for each career track:')
            for j in range(par.J):
                print(f'Career track {j + 1}: {average_realized_utility[j]:.2f}')

    def newscenario(self):
        """ Visualize the share of graduates choosing each career, the average subjective expected utility of the graduates, and the average ex post realized utility given their choice """
        

        par = self.par
        np.random.seed(2024)

        # Initialize storage for results
        chosen_careers = np.zeros((par.N, par.K), dtype=int)
        subjective_expected_utilities = np.zeros((par.N, par.K))
        realized_utilities = np.zeros((par.N, par.K))

        for k in range(par.K):
            for i in range(par.N):
                Fi = par.F[i]

                # Draw epsilon values for friends and for each career track
                epsilon_friends = np.random.normal(0, par.sigma, (par.J, Fi))

                # Calculate prior expected utility for each career track
                temp = par.v[:, np.newaxis] + epsilon_friends
                prior_expected_utility = np.mean(temp, axis=1)

                # Draw J own noise terms
                epsilon_own = np.random.normal(0, par.sigma, par.J)

                # Choose the career track with the highest expected utility
                chosen_career = np.argmax(prior_expected_utility)
                chosen_careers[i, k] = chosen_career

                # Store the subjective expected utility and realized utility
                subjective_expected_utilities[i, k] = prior_expected_utility[chosen_career]
                realized_utilities[i, k] = par.v[chosen_career] + epsilon_own[chosen_career]
        
        # Calculate the share of graduates choosing each career for each graduate
        career_shares = np.zeros((par.N, par.J))
        for i in range(par.N):
            for j in range(par.J):
                career_shares[i, j] = np.mean(chosen_careers[i] == j)

        career_shares_percent = career_shares * 100

        # Calculate average subjective expected utility and average realized utility
        avg_subjective_expected_utility = np.mean(subjective_expected_utilities, axis=1)
        avg_realized_utility = np.mean(realized_utilities, axis=1)


        # Visualization
        plt.figure(figsize=(12, 6))

        # Stacked bar chart for career shares
        plt.bar(np.arange(1, par.N + 1), career_shares_percent[:, 0], label='Career 1', align='center', alpha=0.7)
        bottom = career_shares_percent[:, 0]
        for j in range(1, par.J):
            plt.bar(np.arange(1, par.N + 1), career_shares_percent[:, j], bottom=bottom, label=f'Career {j + 1}', align='center', alpha=0.7)
            bottom += career_shares_percent[:, j]

        plt.xlabel('Graduate')
        plt.ylabel('Share (%)')
        plt.title('Share of Graduates Choosing Each Career')
        plt.xticks(np.arange(1, par.N + 1))
        plt.legend(title='Career Tracks', loc='upper right')

        # Adjust layout
        plt.tight_layout()

        plt.figure(figsize=(12, 6))

        # Bar chart for subjective expected utility
        plt.subplot(1, 2, 1)
        plt.bar(np.arange(1, par.N + 1), avg_subjective_expected_utility, align='center', alpha=0.7)
        plt.xlabel('Graduate')
        plt.ylabel('Average Subjective Expected Utility')
        plt.title('Average Subjective Expected Utility for Each Graduate')
        plt.xticks(np.arange(1, par.N + 1))

        # Bar chart for realized utility
        plt.subplot(1, 2, 2)
        plt.bar(np.arange(1, par.N + 1), avg_realized_utility, align='center', alpha=0.7)
        plt.xlabel('Graduate')
        plt.ylabel('Average Realized Utility')
        plt.title('Average Realized Utility for Each Graduate')
        plt.xticks(np.arange(1, par.N + 1))

        # Adjust layout
        plt.tight_layout()

        # Show plot
        plt.show()

    
    def newscenario_with_switching(self):
        """ New scenario with career switching after first year """

        par = self.par
        np.random.seed(2024)

        # Initialize storage for results
        chosen_careers_first_year = np.zeros((par.N, par.K), dtype=int)
        subjective_expected_utilities_first_year = np.zeros((par.N, par.K))
        realized_utilities_first_year = np.zeros((par.N, par.K))

        chosen_careers_second_year = np.zeros((par.N, par.K), dtype=int)
        subjective_expected_utilities_second_year = np.zeros((par.N, par.K))
        realized_utilities_second_year = np.zeros((par.N, par.K))

        switch_count = np.zeros((par.N, par.J))  # Counting how many switch to each career

        for k in range(par.K):
            for i in range(par.N):
                Fi = par.F[i]  # Number of friends for graduate i

                # Draw epsilon values for friends and for each career track
                epsilon_friends = np.random.normal(0, par.sigma, (par.J, Fi))

                # Calculate prior expected utility for each career track in the first year
                temp = par.v[:, np.newaxis] + epsilon_friends
                prior_expected_utility_first_year = np.mean(temp, axis=1)

                # Draw own noise terms for the first year
                epsilon_own_first_year = np.random.normal(0, par.sigma, par.J)

                # Choose the career track with the highest expected utility for the first year
                chosen_career_first_year = np.argmax(prior_expected_utility_first_year)
                chosen_careers_first_year[i, k] = chosen_career_first_year

                # Store the subjective expected utility and realized utility for the first year
                subjective_expected_utilities_first_year[i, k] = prior_expected_utility_first_year[chosen_career_first_year]
                realized_utilities_first_year[i, k] = par.v[chosen_career_first_year] + epsilon_own_first_year[chosen_career_first_year]

                # Calculate the realized utility of chosen career in first year
                u_first_year = realized_utilities_first_year[i, k]

                # Calculate the priors for the second year with switching cost
                prior_expected_utility_second_year = prior_expected_utility_first_year.copy()
                prior_expected_utility_second_year[chosen_career_first_year] = u_first_year  # Set the chosen career to realized utility
                prior_expected_utility_second_year -= 1  # Apply switching cost

                # Choose the career track with the highest expected utility for the second year
                chosen_career_second_year = np.argmax(prior_expected_utility_second_year)
                chosen_careers_second_year[i, k] = chosen_career_second_year

                # Store the subjective expected utility and realized utility for the second year
                subjective_expected_utilities_second_year[i, k] = prior_expected_utility_second_year[chosen_career_second_year]
                realized_utilities_second_year[i, k] = par.v[chosen_career_second_year] + epsilon_own_first_year[chosen_career_second_year] - 1  # Adjust for switching cost

                # Count the number of graduates switching to each career
                if chosen_career_first_year != chosen_career_second_year:
                    switch_count[i, chosen_career_second_year] += 1

        # Calculate shares of graduates choosing each career in first year
        career_shares_first_year = np.zeros((par.N, par.J))
        for i in range(par.N):
            for j in range(par.J):
                career_shares_first_year[i, j] = np.mean(chosen_careers_first_year[i] == j)

        career_shares_percent_first_year = career_shares_first_year * 100

        # Calculate shares of graduates choosing each career in second year
        career_shares_second_year = np.zeros((par.N, par.J))
        for i in range(par.N):
            for j in range(par.J):
                career_shares_second_year[i, j] = np.mean(chosen_careers_second_year[i] == j)

        career_shares_percent_second_year = career_shares_second_year * 100

        # Calculate average subjective expected utility and average realized utility for first year
        avg_subjective_expected_utility_first_year = np.mean(subjective_expected_utilities_first_year, axis=1)
        avg_realized_utility_first_year = np.mean(realized_utilities_first_year, axis=1)

        # Calculate average subjective expected utility and average realized utility for second year
        avg_subjective_expected_utility_second_year = np.mean(subjective_expected_utilities_second_year, axis=1)
        avg_realized_utility_second_year = np.mean(realized_utilities_second_year, axis=1)

        # Calculate share of graduates that choose to switch careers in the second year, conditional on first year choice
        switch_shares = switch_count / np.sum(switch_count, axis=1, keepdims=True) * 100
        


