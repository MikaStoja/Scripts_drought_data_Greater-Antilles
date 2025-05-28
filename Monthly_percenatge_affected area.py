import xarray as xr
import pandas as pd
import numpy as np

# Path to the NetCDF file
file_path = 'spi1_CUBA.nc.nc' #change .nc for another scale and island

# Open the dataset without decoding time
ds = xr.open_dataset(file_path, decode_times=False)

# Convert time values into actual dates
start_date = pd.to_datetime("1980-01-01")
times = pd.date_range(start=start_date, periods=ds.dims['time'], freq='MS')

# Select the SPI variable
data = ds['spi']

# Define SPI thresholds and corresponding categories
bins = [-np.inf, -1.65, -1.28, -0.84]
labels = ['Extremely dry', 'Severely dry', 'Moderately dry']

# Initialize list to store results
results = []

# Loop through each month and calculate the drought category percentages
for idx, time in enumerate(times):
    monthly_data = data.isel(time=idx)

    # Flatten the array and remove NaN values
    flat_data = monthly_data.values.flatten()
    flat_data = flat_data[~np.isnan(flat_data)]

    # Categorize the values using bins
    categories = pd.cut(flat_data, bins=bins, labels=labels)

    # Calculate total and category counts
    total_count = len(flat_data)
    category_counts = categories.value_counts().to_dict()

    # Store results for each category
    for category in labels:
        count = category_counts.get(category, 0)
        percentage = (count / total_count) * 100 if total_count > 0 else 0
        results.append({
            'Month': time.strftime('%Y-%m'),
            'Category': category,
            'Percentage': percentage
        })

# Convert results to DataFrame
df = pd.DataFrame(results)

# Save to CSV using semicolon as separator
output_path = 'SPI1_monthly_percentages_of_affected_area_by_moderate_severe_extreme_conditions_CUBA.csv'
df.to_csv(output_path, index=False, sep=';')

print(f"CSV file saved at: {output_path}")