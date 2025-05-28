import matplotlib.pyplot as plt
import numpy as np

# === SPI-1 Data ===
labels = ['DPI', 'OSI', 'DER']
num_vars = len(labels)

# Actual SPI-1 values
data = {
    'Cuba': [3.35, 1.92, 1.93],
    'Jamaica': [3.37, 1.53, 2.36],
    'La Española': [2.92, 1.59, 1.82],
    'Puerto Rico': [3.24, 1.63, 1.96]
}

# # Actual SPI-12 values
# data = {
#     'Cuba': [14.14, 4.07, 3.6],
#     'Jamaica': [27.75, 6.50, 3.69],
#     'La Española': [23.3, 4.33, 5.23],
#     'Puerto Rico': [19.83, 6.63, 3.5]
# }

colors = {
    'Cuba': 'blue',
    'Jamaica': 'grey',
    'La Española': 'green',
    'Puerto Rico': 'red'
}

# Radar chart angles
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
angles += angles[:1]  # close the radar chart

# Prepare the figure
fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True), dpi=300)

# Plot each island
for name, values in data.items():
    values += values[:1]  # close the shape
    ax.plot(angles, values, label=name, color=colors[name], linewidth=2)
    ax.fill(angles, values, alpha=0.25, color=colors[name])

# Circular layout settings
ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)
ax.set_xticks(angles[:-1])
ax.set_xticklabels(labels, fontsize=16, fontweight='normal')

# Radial axis configuration
ax.set_ylim(0, 4)
yticks = np.arange(0, 4.5, 0.5)
ax.set_yticks(yticks)
ax.set_yticklabels([])  # Hide default radial labels
ax.yaxis.grid(True, color='lightgray', linestyle='-', linewidth=0.7)

# Custom radial labels
for ytick in yticks:
    label = str(int(ytick)) if ytick.is_integer() else str(ytick)
    ax.text(np.radians(30), ytick, label, ha='left', va='center', fontsize=10, fontweight='normal')

# Title and legend
plt.title('SPI-1: DPI, OSI, DER', fontsize=15, pad=20, fontweight='normal')
plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=12)

plt.tight_layout()
plt.savefig("SPI1.png", dpi=300)
#plt.savefig("SPI12.png", dpi=300)
plt.show()

