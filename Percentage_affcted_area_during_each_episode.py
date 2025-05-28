import xarray as xr
import pandas as pd
import numpy as np

# Dictionary mapping SPI scales to corresponding NetCDF files  #change .nc for another island
spi_files = {
    'SPI1': 'spi1_MSWEP_final_01_JAMAICA.nc',
    'SPI3': 'spi3_MSWEP_final_01_JAMAICA.nc',
    'SPI6': 'spi6_MSWEP_final_01_JAMAICA.nc',
    'SPI12': 'spi12_MSWEP_final_01_JAMAICA.nc',
    'SPI18': 'spi18_MSWEP_final_01_JAMAICA.nc',
    'SPI24': 'spi24_MSWEP_final_01_JAMAICA.nc'
}

# Define only drought categories
spi_categories = {
    'Moderate Drought (MD)': (-1.28, -0.84),
    'Severe Drought (SD)': (-1.65, -1.28),
    'Extreme Drought (ED)': (-np.inf, -1.65)
}

# Path to the Excel file containing drought episode dates
excel_path = 'JAMAICA_Drought_Episodes_Results_f_MSWEP.xlsx'

# Start date of the NetCDF dataset
start_date = pd.to_datetime("1980-01-01")

# Output file
output_file = "Drought_Affected_Area_Percentage_Jamaica.xlsx"
writer = pd.ExcelWriter(output_file, engine='xlsxwriter')

# Process each SPI scale
for spi_name, nc_file in spi_files.items():
    print(f"Processing {spi_name}...")

    try:
        # Load NetCDF dataset and detect the SPI variable
        ds = xr.open_dataset(nc_file, decode_times=False)

        # Identify the SPI variable
        spi_var_name = None
        for var in ds.variables:
            if 'spi' in var.lower():
                spi_var_name = var
                break

        if spi_var_name is None:
            print(f"No SPI variable found in {nc_file}.")
            continue

        spi = ds[spi_var_name]
        times = pd.date_range(start=start_date, periods=ds.sizes['time'], freq='MS')

        # Identify the first valid time step within the first 25 time steps
        first_valid_time = next((i for i in range(min(25, spi.sizes['time'])) if not spi.isel(time=i).isnull().all()), None)

        if first_valid_time is None:
            print(f"All values in {spi_name} are NaN, check the NetCDF file.")
            continue

        # Use this time step to generate the land mask
        mask = ~np.isnan(spi.isel(time=first_valid_time).values)
        total_valid_points = np.count_nonzero(mask)

        if total_valid_points == 0:
            print(f"The mask for {spi_name} remains empty, check the NetCDF file.")
            continue

        # Read the corresponding sheet from the Excel file
        episodes = pd.read_excel(excel_path, sheet_name=spi_name)
        results = []

        for idx, row in episodes.iterrows():
            episode_number = idx + 1
            start = pd.to_datetime(row['Start'])
            end = pd.to_datetime(row['End'])

            # Identify time indices within the episode period
            time_indices = np.where((times >= start) & (times <= end))[0]

            # Skip episodes occurring before data availability
            if len(time_indices) == 0 or time_indices[0] < first_valid_time:
                print(f" - ⚠ Episode {episode_number} in {spi_name} occurs before data availability and will be skipped.")
                continue

            # Initialize lists for monthly percentage calculations
            monthly_percentages = {key: [] for key in spi_categories}

            # Compute affected area percentage for each month in the episode
            for i in time_indices:
                month_spi = spi.isel(time=i).values
                month_spi_masked = np.where(mask, month_spi, np.nan)

                for label, (lower, upper) in spi_categories.items():
                    condition = (month_spi_masked > lower) & (month_spi_masked <= upper)
                    count = np.count_nonzero(condition)
                    percentage = (count / total_valid_points) * 100 if total_valid_points > 0 else 0
                    monthly_percentages[label].append(percentage)

            # Compute the average affected area percentage per episode
            episode_percentages = {
                label: np.mean(values) if values else 0
                for label, values in monthly_percentages.items()
            }

            results.append({
                'Episode': episode_number,
                'Start': start.strftime('%Y-%m'),
                'End': end.strftime('%Y-%m'),
                **episode_percentages
            })

        # Save results to the corresponding sheet in the Excel file
        df_spi = pd.DataFrame(results)
        df_spi.to_excel(writer, sheet_name=spi_name, index=False)

    except Exception as e:
        print(f"Error processing {spi_name}: {e}")

# Save and close the Excel file
writer.close()
print(f"\n Excel file successfully generated: {output_file}")
