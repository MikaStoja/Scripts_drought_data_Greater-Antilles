import pandas as pd

# Load the file with data
file_path = 'SPI_CUBA.xlsx'

#file_path = 'SPI_JAMAICA.xlsx'

#file_path = 'SPI_LA_ESPAÑOLA.xlsx'

#file_path = 'SPI_PUERTO_RICO.xlsx'


output_file_path = 'CUBA_Drought_Episodes_Duration_Severity.xlsx'

#output_file_path = 'JAMAICA_Drought_Episodes_Duration_Severity.xlsx'

#output_file_path = 'LA_ESPAÑOLA_Drought_Episodes_Duration_Severity.xlsx'

#output_file_path = 'PUERTO_RICO_Drought_Episodes_Duration_Severity.xlsx'

# Names of the SPI columns to process
spi_columns = ['SPI1', 'SPI3', 'SPI6', 'SPI12', 'SPI18', 'SPI24']
threshold = -0.84

# Read the sheet containing the data
sheet_name = 'Hoja1'
df = pd.read_excel(file_path, sheet_name=sheet_name)

# Ensure the 'Date' column is in datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Dictionary to store results for each SPI
results = {}

for spi in spi_columns:
    if spi not in df.columns:
        print(f"Warning: {spi} is not in the data file. It will be skipped.")
        continue

    # Filter only the relevant columns
    spi_df = df[['Date', spi]].copy()

    # Rename columns for clarity
    spi_df.columns = ['Date', 'SPI']

    # Skip columns that contain only NaN or are empty
    if spi_df['SPI'].isna().all():
        print(f"Warning: {spi} only contains NaN values or is empty. It will be skipped.")
        continue

    # Remove rows with NaN in the SPI column
    spi_df.dropna(subset=['SPI'], inplace=True)

    # List to store drought episodes
    drought_episodes = []

    # Auxiliary variables
    in_drought = False
    start_date = None
    last_negative_date = None
    has_value_below_threshold = False

    # Identify drought episodes
    for index, row in spi_df.iterrows():
        spi_value = row['SPI']
        date = row['Date']

        if not in_drought:
            # Start a drought episode if a negative value is found
            if spi_value < 0:
                in_drought = True
                start_date = date
                last_negative_date = date
                has_value_below_threshold = spi_value < threshold  # Check if value meets the condition
        else:
            # Update the last negative date
            if spi_value < 0:
                last_negative_date = date
                if spi_value < threshold:
                    has_value_below_threshold = True
            # End the drought episode if a positive value is found
            elif spi_value >= 0:
                if has_value_below_threshold:
                    # Save the episode if it meets the condition
                    drought_episodes.append({'Start': start_date, 'End': last_negative_date})
                # Reset variables for the next episode
                in_drought = False
                has_value_below_threshold = False

    # Convert the episodes to a DataFrame
    drought_df = pd.DataFrame(drought_episodes)

    if not drought_df.empty:
        # Calculate the severity of each episode (sum of SPI values)
        severities = []
        for episode in drought_episodes:
            episode_data = spi_df[(spi_df['Date'] >= episode['Start']) & (spi_df['Date'] <= episode['End'])]
            total_severity = episode_data['SPI'].sum()
            severities.append(round(total_severity, 2))

        # Add severity column to the DataFrame
        drought_df['Severity'] = severities

        # Calculate the duration in months of each episode
        durations = []
        for episode in drought_episodes:
            episode_data = spi_df[(spi_df['Date'] >= episode['Start']) & (spi_df['Date'] <= episode['End'])]
            total_months = len(episode_data)
            durations.append(total_months)

        # Add duration column to the DataFrame
        drought_df['Duration'] = durations

        # Format the Start and End columns to show only year and month
        drought_df['Start'] = drought_df['Start'].dt.strftime('%Y-%m')
        drought_df['End'] = drought_df['End'].dt.strftime('%Y-%m')

    # Store results in the dictionary
    results[spi] = drought_df

# Save the results to an Excel file with separate sheets for each SPI
with pd.ExcelWriter(output_file_path) as writer:
    for spi, result_df in results.items():
        result_df.to_excel(writer, sheet_name=spi, index=False)

print(f"The results file has been saved as {output_file_path}")
