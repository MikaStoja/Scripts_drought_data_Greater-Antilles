
import pandas as pd

# === DATA LOADING ===
df = pd.read_excel("SPI_CUBA.xlsx")  # Make sure the file is in the same directory or update the path
#df = pd.read_excel("SPI_JAMAICA.xlsx")  # Make sure the file is in the same directory or update the path
#df = pd.read_excel("SPI_LA_ESPAÑOLA.xlsx")  # Make sure the file is in the same directory or update the path
#df = pd.read_excel("SPI_PUERTO_RICO.xlsx")  # Make sure the file is in the same directory or update the path

df = df.select_dtypes(exclude=['datetime64[ns]'])  

# === PARAMETERS ===
threshold = -0.84
osi_results = {}

# === OSI CALCULATION ===
for column in df.columns:
    series = df[column].dropna().values
    onset_durations = []

    i = 0
    while i < len(series) - 1:
        if series[i] >= 0:
            j = i + 1
            duration = 0
            found = False
            while j < len(series) and series[j] < 0:
                duration += 1
                if series[j] <= threshold:
                    found = True
                    break
                j += 1
            if found:
                onset_durations.append(duration)
                i = j  # continue after the event
            else:
                i += 1
        else:
            i += 1

    avg_osi = sum(onset_durations) / len(onset_durations) if onset_durations else 0

    osi_results[column] = {
        "Avg_OSI": avg_osi,
        "Num_Onsets": len(onset_durations)
    }

# === DISPLAY RESULTS ===
osi_df = pd.DataFrame(osi_results).T
osi_df.index.name = "Island"
print(osi_df)
