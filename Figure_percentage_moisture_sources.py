import matplotlib.pyplot as plt
import numpy as np
plt.rc('font', size=25)
# Data
islands = ['Cuba', 'Jamaica', 'La Española', 'Puerto Rico']
own_region = [10.17, 12.02, 2.99, 1.53]
natl = [89.83, 87.98, 97.01, 98.47]

# Create figure and axis
fig, ax = plt.subplots(figsize=(8, 5))

# Set width of bars and positions
bar_height = 0.35
y_pos = np.arange(len(islands))

# Create horizontal grouped bars
bars1 = ax.barh(y_pos - bar_height/2, own_region, bar_height, 
                label='Own region', color='#d63031', alpha=0.8)
bars2 = ax.barh(y_pos + bar_height/2, natl, bar_height,
                label='NATL', color='#0984e3', alpha=0.8)

# Add value labels on bars
for i, (own, natl_val) in enumerate(zip(own_region, natl)):
    ax.text(own + 1, i - bar_height/2, f'{own:.1f}%', 
            va='center', ha='left', fontsize=12)
    ax.text(natl_val + 1, i + bar_height/2, f'{natl_val:.1f}%', 
            va='center', ha='left', fontsize=12)

# Customize the plot
# ax.set_ylabel('Greater Antilles', fontsize=13, fontweight='bold')
# ax.set_xlabel('Percentage (%)', fontsize=13, fontweight='bold')
# # ax.set_title('Regional vs. North Atlantic Composition by Caribbean Island', 
#              fontsize=14, fontweight='bold', pad=20)

# Set y-axis
ax.set_yticks(y_pos)
ax.set_yticklabels(islands, fontsize=18)

# Set x-axis
ax.set_xlim(0, 105)
ax.set_xticks(np.arange(0, 101, 20))

# Add grid
ax.grid(True, alpha=0.0, linestyle='--', linewidth=0.5, axis='x')
ax.set_axisbelow(True)

# #Customize legend
# ax.legend(frameon=True, fancybox=True, 
#           shadow=True, fontsize=11)

# Remove top and right spines for cleaner look
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(0.5)
ax.spines['bottom'].set_linewidth(0.5)

# Adjust tick parameters
ax.tick_params(axis='both', which='major', labelsize=15, 
               length=4, width=0.5)

ax.invert_yaxis()

# Tight layout to prevent label cutoff
plt.tight_layout()

# Display the plot

#Optional: Save the figure in high resolution for publication
plt.savefig('caribbean_islands_composition_sin_leyenda.png', dpi=300, bbox_inches='tight', 
            facecolor='white', edgecolor='none')
plt.show()