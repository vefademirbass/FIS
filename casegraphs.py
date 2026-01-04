import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

damage = ctrl.Antecedent(np.arange(0, 10.1, 0.1), 'damage')
access = ctrl.Antecedent(np.arange(0, 10.1, 0.1), 'access')
population = ctrl.Antecedent(np.arange(0, 10.1, 0.1), 'population')
priority = ctrl.Consequent(np.arange(0, 100.1, 1), 'priority')

damage['low'] = fuzz.trimf(damage.universe, [0, 0, 5])
damage['medium'] = fuzz.trimf(damage.universe, [2, 5, 8])
damage['high'] = fuzz.trimf(damage.universe, [5, 10, 10])

access['poor'] = fuzz.trimf(access.universe, [0, 0, 5])
access['moderate'] = fuzz.trimf(access.universe, [2, 5, 8])
access['good'] = fuzz.trimf(access.universe, [5, 10, 10])

population['low'] = fuzz.trimf(population.universe, [0, 0, 5])
population['medium'] = fuzz.trimf(population.universe, [2, 5, 8])
population['high'] = fuzz.trimf(population.universe, [5, 10, 10])

priority['low'] = fuzz.trimf(priority.universe, [0, 0, 30])
priority['medium'] = fuzz.trimf(priority.universe, [20, 40, 60])
priority['med_high'] = fuzz.trimf(priority.universe, [40, 60, 80])
priority['high'] = fuzz.trimf(priority.universe, [60, 80, 90])
priority['very_high'] = fuzz.trimf(priority.universe, [80, 100, 100])


rule1 = ctrl.Rule(damage['high'] & access['good'] & population['high'], priority['very_high'])
rule2 = ctrl.Rule(damage['high'] & access['poor'], priority['medium']) 
rule3 = ctrl.Rule(damage['low'] & access['good'], priority['low'])
rule4 = ctrl.Rule(damage['medium'] & population['high'], priority['high'])
rule5 = ctrl.Rule(damage['high'] & population['low'], priority['med_high'])
rule6 = ctrl.Rule(damage['medium'] & access['moderate'], priority['medium'])
rule7 = ctrl.Rule(damage['low'] & population['high'], priority['medium'])


priority_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7])
simulation = ctrl.ControlSystemSimulation(priority_ctrl)


def plot_3d_surface(input1_name, input2_name, fixed_input_name, fixed_value, filename):
    x_range = np.arange(0, 10.1, 0.5)
    y_range = np.arange(0, 10.1, 0.5)
    X, Y = np.meshgrid(x_range, y_range)
    Z = np.zeros_like(X)

    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            simulation.input[input1_name] = X[i, j]
            simulation.input[input2_name] = Y[i, j]
            simulation.input[fixed_input_name] = fixed_value # 3. değişkeni sabitliyoruz
            try:
                simulation.compute()
                Z[i, j] = simulation.output['priority']
            except:
                Z[i, j] = 0

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(X, Y, Z, cmap='viridis', linewidth=0, antialiased=True)
    
    ax.set_xlabel(input1_name.capitalize())
    ax.set_ylabel(input2_name.capitalize())
    ax.set_zlabel('Priority Output')
    ax.set_title(f'Surface Plot: {input1_name.capitalize()} vs {input2_name.capitalize()}')
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.savefig(filename)
    plt.show()


plot_3d_surface('damage', 'access', 'population', 5.0, 'surface_damage_access.png')


plot_3d_surface('damage', 'population', 'access', 5.0, 'surface_damage_pop.png')


plot_3d_surface('access', 'population', 'damage', 8.0, 'surface_access_pop.png')