import pandas as pd

# === LOAD DATA ===
df = pd.read_excel("SPI_CUBA.xlsx")  # Make sure the file is in the same directory or update the path
# df = pd.read_excel("SPI_JAMAICA.xlsx")
# df = pd.read_excel("SPI_LA_ESPAÑOLA.xlsx")
# df = pd.read_excel("SPI_PUERTO_RICO.xlsx")

df = df.select_dtypes(exclude=['datetime64[ns]'])  #

# === DPI CALCULATION ===
dpi_results = {}

for column in df.columns:
    series = df[column].dropna().values
    in_event = False
    durations = []
    duration = 0
    reached_threshold = False

    for value in series:
        if not in_event:
            if value < 0:
                in_event = True
                duration = 1
                reached_threshold = value <= -0.84
        else:
            if value < 0:
                duration += 1
                if value <= -0.84:
                    reached_threshold = True
            else:
                if reached_threshold:
                    durations.append(duration)
                in_event = False
                duration = 0
                reached_threshold = False

    if in_event and reached_threshold:
        durations.append(duration)

    dpi = sum(durations) / len(durations) if durations else 0

    dpi_results[column] = {
        "DPI": dpi,
        "Num_events": len(durations),
        "Total_months_in_drought": sum(durations)
    }

# === CONVERT TO DATAFRAME AND DISPLAY ===
dpi_df = pd.DataFrame(dpi_results).T
dpi_df.index.name = "Island"

print(dpi_df)
