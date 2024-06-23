import numpy as np
import matplotlib.pyplot as plt

class PointAnalysis:
    def __init__(self, seed=2024):
        """Initialize the PointAnalysis class with random points and initial parameters"""
        
        self.rng = np.random.default_rng(seed)
        self.X = self.rng.uniform(size=(50, 2))
        self.y = self.rng.uniform(size=(2,))

        self.A = None
        self.B = None
        self.C = None
        self.D = None
        self.r_ABC = (np.nan, np.nan, np.nan)
        self.r_CDA = (np.nan, np.nan, np.nan)
        self.inside_ABC = False
        self.inside_CDA = False
        self.f = lambda x: x[0] * x[1]
        self.Y = [(0.2,0.2), (0.8,0.2), (0.8,0.8), (0.8,0.2), (0.5,0.5)]
    
    def find_point(self, y, condition):
        """Find the closest point in X that satisfies the given condition"""
        
        filtered_points = [point for point in self.X if condition(point, y)]
        
        if not filtered_points:
            return np.nan, np.nan
        
        distances = [np.linalg.norm(point - y) for point in filtered_points]
        
        return filtered_points[np.argmin(distances)]
    
    def compute_points(self, y):
        """Compute the points A, B, C, and D based on the given point y"""
        self.A = self.find_point(y, lambda point, y: point[0] > y[0] and point[1] > y[1])
        self.B = self.find_point(y, lambda point, y: point[0] > y[0] and point[1] < y[1])
        self.C = self.find_point(y, lambda point, y: point[0] < y[0] and point[1] < y[1])
        self.D = self.find_point(y, lambda point, y: point[0] < y[0] and point[1] > y[1])
    
    def barycentric_coordinates(self, A, B, C, y):
        """Compute the barycentric coordinates of point y with respect to triangle ABC"""
        denom = (B[1] - C[1]) * (A[0] - C[0]) + (C[0] - B[0]) * (A[1] - C[1])
        r1 = ((B[1] - C[1]) * (y[0] - C[0]) + (C[0] - B[0]) * (y[1] - C[1])) / denom
        r2 = ((C[1] - A[1]) * (y[0] - C[0]) + (A[0] - C[0]) * (y[1] - C[1])) / denom
        r3 = 1 - r1 - r2
        return r1, r2, r3
    
    def compute_barycentric_coordinates(self, y):
        """Compute the barycentric coordinates for triangles ABC and CDA"""
        if not np.isnan(self.A).any() and not np.isnan(self.B).any() and not np.isnan(self.C).any():
            self.r_ABC = self.barycentric_coordinates(self.A, self.B, self.C, y)
        else:
            self.r_ABC = (np.nan, np.nan, np.nan)

        if not np.isnan(self.C).any() and not np.isnan(self.D).any() and not np.isnan(self.A).any():
            self.r_CDA = self.barycentric_coordinates(self.C, self.D, self.A, y)
        else:
            self.r_CDA = (np.nan, np.nan, np.nan)

        self.inside_ABC = all(0 <= r <= 1 for r in self.r_ABC)
        self.inside_CDA = all(0 <= r <= 1 for r in self.r_CDA)
    
    def plot_question_1(self):
        """Plot the random points, the point y, and the triangles ABC and CDA"""
        
        self.compute_points(self.y)
        
        plt.figure(figsize=(8, 8))
        plt.scatter(self.X[:, 0], self.X[:, 1], label='Random Points in X')
        plt.scatter(self.y[0], self.y[1], color='red', label='Point y')
        
        if not np.isnan(self.A).any():
            plt.scatter(self.A[0], self.A[1], color='blue', label='Point A')
        if not np.isnan(self.B).any():
            plt.scatter(self.B[0], self.B[1], color='green', label='Point B')
        if not np.isnan(self.C).any():
            plt.scatter(self.C[0], self.C[1], color='purple', label='Point C')
        if not np.isnan(self.D).any():
            plt.scatter(self.D[0], self.D[1], color='orange', label='Point D')

        # Draw triangles ABC and CDA if points are valid
        if not np.isnan(self.A).any() and not np.isnan(self.B).any() and not np.isnan(self.C).any():
            plt.plot([self.A[0], self.B[0], self.C[0], self.A[0]], [self.A[1], self.B[1], self.C[1], self.A[1]], color='black', linestyle='-', linewidth=1, label='Triangle ABC')
        if not np.isnan(self.C).any() and not np.isnan(self.D).any() and not np.isnan(self.A).any():
            plt.plot([self.C[0], self.D[0], self.A[0], self.C[0]], [self.C[1], self.D[1], self.A[1], self.C[1]], color='brown', linestyle='-', linewidth=1, label='Triangle CDA')

        plt.xlabel('$x_1$')
        plt.ylabel('$x_2$')
        plt.legend()
        plt.title('Points and Triangles in Unit Square')
        plt.grid(True)
        plt.show()
    
    def question_2(self):
        """Compute and print the barycentric coordinates of point y with respect to triangles ABC and CDA"""
        
        self.compute_barycentric_coordinates(self.y)
        
        print(f"r_ABC: {self.r_ABC}")
        print(f"r_CDA: {self.r_CDA}")
        print(f"y is inside triangle ABC: {self.inside_ABC}")
        print(f"y is inside triangle CDA: {self.inside_CDA}")

    def approximate_f_y(self, y, f):
        """Approximate the value of f(y) using barycentric coordinates"""
        self.compute_points(y)
        self.compute_barycentric_coordinates(y)

        f_A = f(self.A)
        f_B = f(self.B)
        f_C = f(self.C)
        f_D = f(self.D)

        if self.inside_ABC:
            return self.r_ABC[0] * f_A + self.r_ABC[1] * f_B + self.r_ABC[2] * f_C
        elif self.inside_CDA:
            return self.r_CDA[0] * f_C + self.r_CDA[1] * f_D + self.r_CDA[2] * f_A
        else:
            return np.nan
    
    def question_3(self):
        """Compute and print the approximation of f(y) and compare it with the true value"""
        
        f_y_approx = self.approximate_f_y(self.y, self.f)
        f_y_true = self.f(self.y)
        
        print(f"Approximated f(y): {f_y_approx}")
        print(f"True f(y): {f_y_true}")
        print(f"Absolute error: {abs(f_y_approx - f_y_true)}")
    
    def question_4(self):
        """Repeat the approximation of f(y) for all points in the set Y and print the results"""
        
        results = [self.process_y(y, self.f) for y in self.Y]
        
        for i, (f_y_approx, f_y_true, error) in enumerate(results):
            print(f"Point Y[{i}]: {self.Y[i]}")
            print(f"  Approximated f(y): {f_y_approx}")
            print(f"  True f(y): {f_y_true}")
            print(f"  Absolute error: {error}")

    def process_y(self, y, f):
        """Process a given point y to compute the approximation and true value of f(y)"""
        
        self.y = np.array(y)
        self.compute_points(y)
        self.compute_barycentric_coordinates(y)
        
        f_y_approx = self.approximate_f_y(y, f)
        f_y_true = f(self.y)
        error = abs(f_y_approx - f_y_true)
        
        return f_y_approx, f_y_true, error
