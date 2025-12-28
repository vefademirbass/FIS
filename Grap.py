import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz


def plot_variable(var_name, x_range, ranges, labels, filename):
    x = np.arange(x_range[0], x_range[1] + 0.1, 0.1)
    
    plt.figure(figsize=(8, 4))
    
    
    colors = ['b', 'g', 'r', 'c', 'm']
    for i, (label, abc) in enumerate(zip(labels, ranges)):
        y = fuzz.trimf(x, abc)
        plt.plot(x, y, linewidth=2, label=label, color=colors[i % len(colors)])
        plt.fill_between(x, y, alpha=0.1, color=colors[i % len(colors)])
    
    plt.title(f'Membership Functions for "{var_name}"')
    plt.xlabel(f'{var_name} Score')
    plt.ylabel('Membership Degree')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.show()


plot_variable(
    "Damage Severity", [0, 10], 
    [[0, 0, 5], [2, 5, 8], [5, 10, 10]], 
    ['Low', 'Medium', 'High'], 
    "damage_mf.png"
)


plot_variable(
    "Accessibility", [0, 10], 
    [[0, 0, 5], [2, 5, 8], [5, 10, 10]], 
    ['Poor', 'Moderate', 'Good'], 
    "accessibility_mf.png"
)


plot_variable(
    "Population Exposure", [0, 10], 
    [[0, 0, 5], [2, 5, 8], [5, 10, 10]], 
    ['Low', 'Medium', 'High'], 
    "population_mf.png"
)


plot_variable(
    "Priority Output", [0, 100],
    [[0, 0, 30], [20, 40, 60], [40, 60, 80], [60, 80, 90], [80, 100, 100]],
    ['Low', 'Medium', 'Med-High', 'High', 'Very High'],
    "priority_mf.png"
)