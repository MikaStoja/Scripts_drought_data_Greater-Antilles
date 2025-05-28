import matplotlib.pyplot as plt
import pandas as pd
plt.rc('font', size=25)

# === Data ===
data = {
    'Date': ['Aug-93', 'Sep-93', 'Oct-93', 'Nov-93', 'Dec-93', 'Jan-94', 'Feb-94', 
             'Mar-94', 'Apr-94', 'May-94', 'Jun-94', 'Jul-94', 'Aug-94', 'Sep-94', 
             'Oct-94', 'Nov-94', 'Dec-94', 'Jan-95'],
    'SPI1': [-1.19, -0.23, -1.53, -0.43, -0.77, -0.43, -0.23, -0.74, -0.60, 
             -1.50, -0.94, -1.68, -1.54, -0.39, -0.08, -0.47, -0.30, -0.40],
    'Puerto Rico': [-0.01, -0.02, -0.03, -0.03, 0.00, -0.02, -0.01, 0.01, -0.01, 
                    -0.02, -0.02, 0.00, -0.01, -0.04, -0.02, 0.00, 0.00, 0.02],
    'NATL': [-0.58, 0.08, -0.90, -0.45, -0.43, -0.26, 0.17, 0.07, 0.49, 
                -1.35, -1.25, -0.79, -1.16, -2.09, -0.21, -0.14, -0.46, -0.01]
}

df = pd.DataFrame(data)

# === Create figure with dual y-axes ===
fig, ax1 = plt.subplots(figsize=(14, 8))

# Left axis - SPI1 and Oceanic contribution
ax1.plot(df['Date'], df['SPI1'], 'b-', linewidth=2.5, marker='o', markersize=4, 
         markerfacecolor='white', markeredgecolor='blue', markeredgewidth=1.5, label='SPI1')
ax1.plot(df['Date'], df['Oceanic'], '#34a2a9', linewidth=2, marker='o', markersize=4, 
         markerfacecolor='white', markeredgecolor='#34a2a9', markeredgewidth=1.5, label='NATL')
ax1.set_ylabel('SPI1 / NATL anomaly', fontsize=20)
ax1.set_xlabel('Month', fontsize=20)
ax1.set_ylim(-2.5, 1.0)  # Align to 0
ax1.grid(True, alpha=0.0)
ax1.tick_params(axis='both', labelsize=20)

# Right axis - Terrestrial contribution
ax2 = ax1.twinx()
ax2.plot(df['Date'], df['Terrestrial'], 'r--', linewidth=2.5, marker='o', markersize=4, 
         markerfacecolor='white', color='darkred', markeredgecolor='darkred', markeredgewidth=1.5, label='Puerto Rico')
ax2.set_ylabel('Puerto Rico anomaly', color='darkred', fontsize=20)
ax2.set_ylim(-0.05, 0.025)  # Align to 0
ax2.tick_params(axis='y', labelcolor='darkred', labelsize=20)

# Zero reference line
ax1.axhline(y=0, color='black', linestyle='-', alpha=0.7, linewidth=2)

# Combined legend
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, 
           loc='upper left', bbox_to_anchor=(0.02, 0.98), 
           frameon=True, fancybox=True, shadow=True, fontsize=15)

# Improved x-axis formatting
plt.setp(ax1.get_xticklabels(), rotation=45, ha='right', fontsize=20)
plt.title('Anomalies of (E - P) < 0 during the Most Severe Drought Episode over Puerto Rico', 
          fontsize=24, fontweight='bold', pad=20)

# Adjust layout
plt.subplots_adjust(bottom=0.15, right=0.85, left=0.1)
plt.savefig('Anomaly_Puerto_Rico.png', dpi=300, bbox_inches='tight')
plt.show()
