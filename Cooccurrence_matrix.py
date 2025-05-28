import pandas as pd

# Load the original file
df = pd.read_excel("SPI_CUBA.xlsx")  # Make sure the file is in the same directory or update the path
# df = pd.read_excel("SPI_JAMAICA.xlsx")
# df = pd.read_excel("SPI_LA_ESPAÑOLA.xlsx")
# df = pd.read_excel("SPI_PUERTO_RICO.xlsx")

# Create binary version: 1 if SPI ≤ -0.84, 0 otherwise
binary_df = df.copy()
binary_df.iloc[:, 1:] = (df.iloc[:, 1:] <= -0.84).astype(int)

# Calculate co-occurrences (ensure integer columns)
cooccurrence_df = pd.DataFrame()
cooccurrence_df["Date"] = df["Unnamed: 0"]
cooccurrence_df["CUBA & JAMAICA"] = (binary_df["SPI12_CUBA"].astype(int) & binary_df["SPI12_JAMAICA"].astype(int))
cooccurrence_df["CUBA & LA_ESPAÑOLA"] = (binary_df["SPI12_CUBA"].astype(int) & binary_df["SPI12_LA_ESPAÑOLA"].astype(int))
cooccurrence_df["CUBA & PUERTO_RICO"] = (binary_df["SPI12_CUBA"].astype(int) & binary_df["SPI12_PUERTO_RICO"].astype(int))

# Save to Excel
cooccurrence_df.to_excel("Co_occurrence_Matrix.xlsx", index=False)