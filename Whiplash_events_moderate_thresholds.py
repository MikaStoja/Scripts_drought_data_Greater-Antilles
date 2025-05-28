import pandas as pd

# Load the SPI Excel file
df = pd.read_excel("SPI_CUBA.xlsx")  # Make sure the file is in the same directory or update the path
# df = pd.read_excel("SPI_JAMAICA.xlsx")
# df = pd.read_excel("SPI_LA_ESPAÑOLA.xlsx")
# df = pd.read_excel("SPI_PUERTO_RICO.xlsx")

# Rename columns for easier access
df.columns = ["Date", "CUBA", "JAMAICA", "HISPANIOLA", "PUERTO_RICO"]
df["Date"] = pd.to_datetime(df["Date"])

# Define thresholds
dry_threshold = -0.84
wet_threshold = 0.84

# Function to detect whiplash events for each island
def detect_whiplash(spi_series, dates, island_name):
    events = []
    for i in range(1, len(spi_series)):
        prev_spi = spi_series.iloc[i - 1]
        curr_spi = spi_series.iloc[i]
        date = dates.iloc[i]

        if prev_spi <= dry_threshold and curr_spi >= wet_threshold:
            events.append({
                "Date": date,
                "Island": island_name,
                "Type": "Dry-to-Wet",
                "SPI_prev": prev_spi,
                "SPI_curr": curr_spi,
                "Magnitude": round(abs(curr_spi - prev_spi), 2)
            })
        elif prev_spi >= wet_threshold and curr_spi <= dry_threshold:
            events.append({
                "Date": date,
                "Island": island_name,
                "Type": "Wet-to-Dry",
                "SPI_prev": prev_spi,
                "SPI_curr": curr_spi,
                "Magnitude": round(abs(curr_spi - prev_spi), 2)
            })
    return events

# Detect events for all islands
all_events = []
for island in ["CUBA", "JAMAICA", "HISPANIOLA", "PUERTO_RICO"]:
    all_events.extend(detect_whiplash(df[island], df["Date"], island))

# Create DataFrame with results
events_df = pd.DataFrame(all_events)
events_df = events_df[["Date", "Island", "Type", "Magnitude", "SPI_prev", "SPI_curr"]]

# Save as Excel file
events_df.to_excel("Whiplash_Events_Moderate_Conditions.xlsx", index=False)
