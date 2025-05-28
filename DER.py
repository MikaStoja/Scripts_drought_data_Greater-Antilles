import pandas as pd

# === DATA LOADING ===
df = pd.read_excel("SPI_CUBA.xlsx")  # Make sure the file is in the same directory or update the path
#df = pd.read_excel("SPI_JAMAICA.xlsx")  # Make sure the file is in the same directory or update the path
#df = pd.read_excel("SPI_LA_ESPAÑOLA.xlsx")  # Make sure the file is in the same directory or update the path
#df = pd.read_excel("SPI_PUERTO_RICO.xlsx")  # Make sure the file is in the same directory or update the path

df = df.select_dtypes(exclude=['datetime64[ns]'])  

# === PARAMETERS ===
threshold = -0.84
ror_results = {}

# === ROR CALCULATION ===
for column in df.columns:
    series = df[column].dropna().values
    i = 0
    rors = []

    while i < len(series) - 1:
        if series[i] >= 0:
            j = i + 1
            onset_duration = 0
            reached_threshold = False

            while j < len(series) and series[j] < 0:
                onset_duration += 1
                if series[j] <= threshold:
                    reached_threshold = True
                    break
                j += 1

            if reached_threshold:
                k = j
                while k < len(series) and series[k] < 0:
                    k += 1
                recovery_duration = k - j if k < len(series) else 0

                if onset_duration > 0:
                    ror = recovery_duration / onset_duration
                    rors.append(ror)
                i = k
            else:
                i += 1
        else:
            i += 1

    avg_ror = sum(rors) / len(rors) if rors else 0
    ror_results[column] = {
        "Avg_ROR": avg_ror,
        "Num_events": len(rors)
    }

# === RESULTS AS DATAFRAME ===
ror_df = pd.DataFrame(ror_results).T
ror_df.index.name = "Island"
print(ror_df)