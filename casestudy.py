import numpy as np
import matplotlib.pyplot as plt

def fuzzy_centroid_visualization():
    
    x = np.linspace(0, 100, 1000)

    
    y_very_high = np.zeros_like(x)
    
   
    mask = (x >= 80) & (x <= 100)
    y_very_high[mask] = (x[mask] - 80) / 20
    
   
    cut_level = 0.6
    y_cut = np.minimum(y_very_high, cut_level)

   
    numerator = np.sum(x * y_cut)
    denominator = np.sum(y_cut)
    
    if denominator == 0:
        centroid = 0
    else:
        centroid = numerator / denominator

   
    plt.figure(figsize=(10, 6))

    
    plt.plot(x, y_very_high, 'm--', alpha=0.3, label='Orginal Very-High Area')

  
    plt.plot(x, y_cut, color='magenta', linewidth=2, label=f'Under {cut_level})')
    plt.fill_between(x, 0, y_cut, color='magenta', alpha=0.2)

 
    plt.vlines(centroid, 0, cut_level, colors='black', linestyles='solid', linewidth=2, label=f'Centroid: {centroid:.2f}')
    
 
    plt.xlabel('Priority Output Score')
    plt.ylabel('Membership Degree')
    plt.ylim(0, 1.1)
    plt.xlim(0, 100)
    plt.grid(True, alpha=0.3)
    plt.legend(loc='upper left')

    
    plt.text(centroid - 15, 0.3, f'X = {centroid:.2f}', fontsize=12, fontweight='bold', color='black')

    plt.show()
    

if __name__ == "__main__":
    fuzzy_centroid_visualization()