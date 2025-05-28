import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

plt.rcParams.update({'font.size': 15})

# Correlation data between SPI calculated with MSWEP and ERA5 Land for each island
islands = ["Cuba", "Jamaica", "Puerto Rico", "La Española"]
timescales = ["SPI1", "SPI3", "SPI6", "SPI12", "SPI18", "SPI24"]

correlations = {
    "Cuba": [0.82, 0.78, 0.72, 0.73, 0.76, 0.76],
    "Jamaica": [0.74, 0.72, 0.71, 0.71, 0.76, 0.80],
    "Puerto Rico": [0.82, 0.81, 0.79, 0.79, 0.83, 0.87],
    "La Española": [0.85, 0.80, 0.77, 0.78, 0.82, 0.85]
}

# Convert data into a DataFrame
df_corr = pd.DataFrame(correlations, index=timescales)

# Create heatmap figure with scale from 0 to 1 and red color palette
plt.figure(figsize=(12, 6))
sns.heatmap(df_corr, annot=True, cmap="Reds", linewidths=0.5, vmin=0.4, vmax=1, cbar_kws={'label': 'Correlation'})

# Plot configuration
plt.xlabel("Greater Antilles")
plt.ylabel("SPI Timescale")
# plt.title("MSWEP vs. ERA5 Land")
plt.title("SPI Timescales (MSWEP vs. ERA5 Land)")

# Save and show the figure
plt.savefig('correlation_MSWEP_vs_ERA5_Land_SPI_time_series.pdf', format='pdf', dpi=300)
plt.show()
